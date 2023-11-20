import json
import os
import unicodedata
from typing import IO, Annotated, List
from urllib.parse import quote
import re
from database_app import (
    DataBaseApp,
    User,
    crud,
    get_current_user,
    get_db,
    oauth2_scheme,
)
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from natsort import natsorted
from sqlalchemy.orm import Session
import logging

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


async def save_upload_file_tmp(file: IO, path: str = "./tmp/", max_size: int = 1024):
    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        file_name = file.filename

        file_name_nfc = unicodedata.normalize("NFC", file_name)

        file_name_encode = file_name_nfc.replace(" ", "_")

        file_path = os.path.join(path, file_name_encode)
        file_tmp = await file.read()
        file_size = len(file_tmp)

        if file_size > max_size:
            raise HTTPException(status_code=400, detail="File size is too large")

        if os.path.exists(file_path):
            raise HTTPException(status_code=400, detail="File is already exist")

        with open(file_path, "wb") as f:
            f.write(file_tmp)
        file_path = {"cmd": "success", "detail": file_path}
    except Exception as e:
        file_path = {"cmd": "error", "detail": e}

    finally:
        return file_path


@file_router.post("/upload")
async def post_file_upload(
    files: List[UploadFile] = File(...),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    # File 업로드 API
    파일 업로드 및 저장된 파일의 정보를 반환

    Args:
        request (Request): Request 객체
        files (List[UploadFile], optional): 파일의 객체. Defaults to File(...).

    Returns:
        str: 파일 업로드 결과를 json 형태로 반환
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if not files:
            raise HTTPException(status_code=400, detail="File is not exist")

        username = get_current_user(token)

        if username is None:
            raise credentials_exception

        user = crud.get_user(db, username)

        file_permit = crud.get_file_permit(db, user.id)

        if not file_permit.file or file_permit.file == 0:
            raise HTTPException(status_code=400, detail="File permission denied")

        if user is None:
            raise credentials_exception

        upload_path = f"../drive/{user.mail}"
        count = len(files)
        if count > 10:
            raise HTTPException(status_code=400, detail="File count is too large")

        file_max_size = file_permit.size
        if file_permit.unit == "KB":
            file_max_size *= 1024
        elif file_permit.unit == "MB":
            file_max_size *= 1024 * 1024
        elif file_permit.unit == "GB":
            file_max_size *= 1024 * 1024 * 1024

        for index, file in enumerate(files):
            result = await save_upload_file_tmp(
                file, upload_path, max_size=file_max_size
            )

            if result["cmd"] == "error":
                count -= 1

        data = {"detail": f"{count} 개의 파일 업로드에 성공했습니다."}

    except JWTError:
        raise credentials_exception

    return data


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
            raise HTTPException(status_code=402, detail="검색 결과가 없습니다.")
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
    token: str = Depends(oauth2_scheme),
):
    """
    # File 리스트 출력 API

    Returns:
        str: 파일 리스트를 json 형태로 반환
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = get_current_user(token)

        if username is None:
            raise credentials_exception

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
            file_size = (
                f"{file_size_tmp} B"
                if file_size_tmp < 1024
                else f"{round(file_size_tmp/1024,2)} KB"
                if file_size_tmp < 1024 * 1024
                else f"{round(file_size_tmp/(1024*1024),2)} MB"
                if file_size_tmp < 1024 * 1024 * 1024
                else f"{round(file_size_tmp/(1024*1024*1024),2)} GB"
            )

            file_name = file.replace("_", " ")

            file_info.append({"name": file_name, "size": file_size})

        if not file_list:
            raise HTTPException(status_code=400, detail="아직 업로드한 파일이 없습니다.")

        return {"file_list": file_info, "file_count": file_count}

    except JWTError:
        raise credentials_exception


@file_router.get("/download")
def get_file_download(
    file_name: str,
    request: Request,
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = get_current_user(token)

        if username is None:
            raise credentials_exception

        file_name = file_name.replace(" ", "_")

        download_path = os.path.join("../drive", username, file_name)

        file_exist = os.path.exists(download_path)
        if not file_exist:
            raise HTTPException(status_code=400, detail="File is not exist")

        headers = request.headers.get("User-Agent")

        if "MSIE" in headers or "Trident" in headers:
            file_name = quote(file_name)
        elif "Chrome" in headers:
            file_name = file_name.encode("UTF-8").decode("ISO-8859-1")
        elif "Opera" in headers:
            file_name = quote(file_name)
        elif "Firefox" in headers:
            file_name = quote(file_name)
        else:
            file_name = quote(file_name)

        return FileResponse(
            download_path,
            filename=file_name,
        )

    except JWTError:
        raise credentials_exception


@file_router.delete("/delete")
def delete_file(
    file_name: str,
    token: str = Depends(oauth2_scheme),
):
    credits_exception = HTTPException(
        status_code=401,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = get_current_user(token)

        file_name_encode = file_name.replace(" ", "_")

        file_path = f"../drive/{username}/{file_name_encode}"

        if not os.path.exists(file_path):
            raise HTTPException(status_code=400, detail="File is not exist")

        os.remove(file_path)

        return {"detail": "File delete success"}

    except JWTError:
        raise credits_exception


@file_router.get("/public")
def get_file_download_public(
    file_name: str,
):
    print(file_name)
    if file_name == "favicon.ico":
        return FileResponse("./favicon.ico")
    if file_name == "robots.txt":
        return FileResponse("./robots.txt")

    file_path = f"../drive/public/{file_name}"
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=file_name)
    else:
        raise HTTPException(status_code=400, detail="File is not exist")
