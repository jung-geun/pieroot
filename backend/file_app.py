import json
import os
from typing import IO, Annotated, List

from database_app import (
    DataBaseApp,
    User,
    crud,
    get_db,
    init_env,
    oauth2_scheme,
    get_current_user,
)
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session


file_router = APIRouter(
    prefix="/api/file",
    tags=["file"],
    responses={404: {"description": "Not found"}},
)


async def save_upload_file_tmp(file: IO, path: str = "./tmp/"):
    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        file_name_encode = file.filename.replace(" ", "_")

        file_path = os.path.join(path, file_name_encode)

        if os.path.exists(file_path):
            raise HTTPException(status_code=400, detail="File is already exist")

        with open(file_path, "wb") as f:
            f.write(await file.read())
        file_path = {"cmd": "success", "detail": file_path}
    except Exception as e:
        file_path = {"cmd": "error", "detail": e}

    finally:
        return file_path


@file_router.post("/upload")
async def post_file_upload(
    request: Request,
    token: str = Depends(oauth2_scheme),
    files: List[UploadFile] = File(...),
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
        # token = request.headers["Authorization"].split(" ")[1]
        if not files:
            raise HTTPException(status_code=400, detail="File is not exist")

        username = get_current_user(token)

        if username is None:
            raise credentials_exception

        user = crud.get_user(db, username)

        file_permit = crud.get_file_permit(db, user.id)

        if not file_permit.file:
            raise HTTPException(status_code=400, detail="File permission denied")

        if user is None:
            raise credentials_exception

        upload_path = f"./tmp/{user.mail}"
        count = len(files)
        if count > 10:
            raise HTTPException(status_code=400, detail="File count is too large")

        for index, file in enumerate(files):
            # 파일 사이즈 10MB 제한
            file_size = file.file.tell()
            if file_size > 500 * 1024 * 1024:
                raise HTTPException(status_code=400, detail="File size is too large")

            result = await save_upload_file_tmp(file, upload_path)

            if result["cmd"] == "error":
                count -= 1

        data = {"detail": f"{count} 개의 파일 업로드에 성공했습니다."}

    except JWTError:
        raise credentials_exception

    return data


@file_router.get("/list")
def get_file_list(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
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

        file_path = f"./tmp/{username}"

        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)

        file_list = os.listdir(file_path)

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

        return {"file_list": file_info}

    except JWTError:
        raise credentials_exception


@file_router.get("/download/{file_name}")
def get_file_download(
    file_name: str,
    request: Request,
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        access_token = request.cookies.get("access_token").split(" ")[1]

        username = get_current_user(access_token)

        if username is None:
            raise credentials_exception

        file_name_encode = file_name.replace(" ", "_")

        download_path = f"./tmp/{username}/{file_name_encode}"

        file_exist = os.path.exists(download_path)

        if not file_exist:
            raise HTTPException(status_code=400, detail="File is not exist")

        return FileResponse(download_path, filename=file_name)

    except JWTError:
        raise credentials_exception


# @file_router.get("/download/")
# def get_
