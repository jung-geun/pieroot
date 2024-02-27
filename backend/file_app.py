import json
import logging
import os
import re
import unicodedata
from typing import IO, Annotated, Dict, List
from urllib.parse import quote

from database_app import crud, get_current_user, get_db
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from natsort import natsorted
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("logs/router_file_info.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

file_router = APIRouter(
    prefix="/file",
    tags=["file"],
    responses={404: {"description": "Not found"}},
)

credentials_exception = HTTPException(
    status_code=401,
    detail="Unauthorized",
    headers={"WWW-Authenticate": "Bearer"},
)


websocket_list: Dict[str, WebSocket] = {}


@file_router.websocket("/ws/upload/{token}")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
    db: Session = Depends(get_db),
):
    await websocket.accept()

    try:
        payload = get_current_user(token)

        await websocket.send_json({"cmd": "start"})

        username = payload["username"]

        user = crud.get_user(db, username)

        if user is None:
            raise credentials_exception

        file_permit = crud.get_file_permit(db, user.id)

        if not file_permit.file or file_permit.file == 0:
            raise Exception("File permission denied")

        upload_path = os.path.join("../drive", user.mail)

        file_max_size = file_permit.size

        file_info = await websocket.receive_json()

        if file_permit.unit == "KB":
            file_max_size *= 1024
        elif file_permit.unit == "MB":
            file_max_size *= 1024 * 1024
        elif file_permit.unit == "GB":
            file_max_size *= 1024 * 1024 * 1024

        if file_info["cmd"] != "start":
            raise Exception("File upload error")

        file_name = file_info["detail"]["name"]
        file_size = file_info["detail"]["size"]
        # chunk_size = file_info["detail"]["chunk_size"]

        if file_size > file_max_size:
            await websocket.send_json(
                {"cmd": "error", "detail": "File size is too large"}
            )
            raise Exception("File size is too large")

        file_name_nfc = unicodedata.normalize("NFC", file_name)

        file_name_encode = file_name_nfc.replace(" ", "_")

        file_path = os.path.join(upload_path, file_name_encode)

        count = 0
        while os.path.exists(file_path):
            count += 1
            file_name_tmp, file_extension = os.path.splitext(file_name_encode)
            file_name_tmp = file_name_tmp + f"_({count})" + file_extension
            file_path = os.path.join(upload_path, file_name_tmp)

        await save_file(websocket, file_path)

        await websocket.send_json({"cmd": "EOF", "detail": "success"})

        await websocket.close()

    except WebSocketDisconnect:
        logger.info("websocket_endpoint > WebSocketDisconnect")
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        logger.info("websocket_endpoint > " + str(e))
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        await websocket.send_json({"cmd": "error", "detail": f"{e}"})
        await websocket.close()


async def save_file(websocket: WebSocket, file_path: str):
    chunk_size = 0
    with open(file_path, "wb") as f:
        while True:
            data = await websocket.receive_bytes()

            if data == b"EOF":
                await websocket.send_json({"cmd": "EOF", "detail": "ack"})
                break

            f.write(data)
            chunk_size += len(data)

            await websocket.send_json({"cmd": "update", "detail": f"len {chunk_size}"})


def file_sort(path, start, end, sort, order, search):
    file_list_tmp = natsorted(
        os.listdir(path), reverse=False if sort == "asc" else True
    )

    if search != "":
        try:
            re.compile(search)
        except re.error:
            raise HTTPException(status_code=402, detail="검색어가 잘못되었습니다.")

        file_list = [file for file in file_list_tmp if re.search(search, file)]

        if not file_list:
            raise HTTPException(status_code=404, detail="검색 결과가 없습니다.")
    else:
        file_list = file_list_tmp

    if order == "name":
        file_list = file_list[start:end]
    elif order == "size":
        file_list = sorted(
            file_list,
            key=lambda x: os.path.getsize(f"{path}/{x}"),
            reverse=False if sort == "asc" else True,
        )[start:end]

    return file_list


@file_router.get("/list")
def get_file_list(
    start: int = 0,
    end: int = 10,
    sort: str = "asc",
    order: str = "name",
    search: str = "",
    payload: dict = Depends(get_current_user),
):
    """
    # File 리스트 출력 API

    Returns:
        str: 파일 리스트를 json 형태로 반환
    """

    try:
        username = payload["username"]

        file_path = f"../drive/{username}"

        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)

        file_count = len(os.listdir(file_path))
        file_list = file_sort(file_path, start, end, sort, order, search)
        if search != "":
            file_count = len(file_list)

        file_info = []
        for index, file in enumerate(file_list):
            file_size_tmp = os.path.getsize(f"{file_path}/{file}")

            if file_size_tmp < 1024:
                file_size = f"{file_size_tmp} B"
            elif file_size_tmp < 1024 * 1024:
                file_size = f"{round(file_size_tmp/1024,1)} KB"
            elif file_size_tmp < 1024 * 1024 * 1024:
                file_size = f"{round(file_size_tmp/(1024*1024),1)} MB"
            else:
                file_size = f"{round(file_size_tmp/(1024*1024*1024),1)} GB"

            file_name = file.replace("_", " ")

            file_info.append({"name": file_name, "size": file_size})

        if not file_list:
            raise HTTPException(
                status_code=411, detail="아직 업로드한 파일이 없습니다."
            )

        return {"file_list": file_info, "file_count": file_count}

    except JWTError:
        logger.info("file list > JWTError")
        raise credentials_exception


@file_router.get("/download", response_class=FileResponse)
async def get_file_download(
    file_name: str,
    request: Request,
    payload: dict = Depends(get_current_user),
):
    try:
        username = payload["username"]

        file_name = file_name.replace(" ", "_")

        download_path = os.path.join("../drive", username, file_name)

        file_exist = os.path.exists(download_path)

        if not file_exist:
            raise HTTPException(status_code=400, detail="File is not exist")

        # headers = request.headers.get("User-Agent")

        # if "MSIE" in headers or "Trident" in headers:
        #     file_name = quote(file_name)
        # elif "Chrome" in headers:
        #     file_name = file_name.encode("UTF-8").decode("ISO-8859-1")
        # elif "Opera" in headers:
        #     file_name = quote(file_name)
        # elif "Firefox" in headers:
        #     file_name = quote(file_name)
        # else:
        #     file_name = quote(file_name)

        return download_path

    except JWTError:
        raise credentials_exception


@file_router.get("/public/{file_name}")
async def get_file_download_public(
    file_name: str,
):
    if file_name == "favicon.ico":
        return FileResponse("./favicon.ico")
    if file_name == "robots.txt":
        return FileResponse("./robots.txt")

    file_path = f"../drive/public/{file_name}"
    if os.path.exists(file_path):
        return StreamingResponse(
            open(file_path, mode="rb"),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={file_name}"},
        )
    else:
        raise HTTPException(status_code=400, detail="File is not exist")


@file_router.delete("/delete")
def delete_file(
    file_name: str,
    payload: dict = Depends(get_current_user),
):
    credits_exception = HTTPException(
        status_code=401,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = payload["username"]

        file_name_encode = file_name.replace(" ", "_")

        file_path = f"../drive/{username}/{file_name_encode}"

        if not os.path.exists(file_path):
            raise HTTPException(status_code=400, detail="File is not exist")

        os.remove(file_path)

        return {"detail": "File delete success"}

    except JWTError:
        raise credits_exception
