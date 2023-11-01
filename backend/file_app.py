from database_app import DataBaseApp, User, crud, get_db, init_env, oauth2_scheme
from fastapi import APIRouter, Depends, HTTPException, Request, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import IO, Annotated, List
import json
import os

# env setting
with open("./env.json", "r") as f:
    SECRET = json.load(f)["SECRET_KEY"]

ALGORITHM = "HS256"

file_router = APIRouter(
    prefix="/api/file",
    tags=["file"],
    responses={404: {"description": "Not found"}},
)


async def save_upload_file_tmp(file: IO, path: str = "./tmp/"):
    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        file_path = os.path.join(path, file.filename)

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
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = request.headers["Authorization"].split(" ")[1]
        if not files:
            raise HTTPException(status_code=400, detail="File is not exist")
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])

        username = payload.get("sub")

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
                logger.warning(f"Exception > {result['detail']}")

        data = {"detail": f"{count} 개의 파일 업로드에 성공했습니다."}

    except JWTError:
        raise credentials_exception

    return data


@file_router.get("/list")
async def get_file_list(
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
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        file_path = f"./tmp/{username}"

        file_list = os.listdir(file_path)
        return {"file_list": file_list}

    except JWTError:
        raise credentials_exception
    except Exception as e:
        logger.warning(f"Exception > {e}")
        return {"error": "file list error"}


@file_router.get("/download/{file_name}")
async def get_file_download(
    file_name: str,
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        download_path = f"./tmp/{username}/{file_name}"
        file_exist = os.path.exists(download_path)
        if not file_exist:
            raise HTTPException(status_code=400, detail="File is not exist")

        return FileResponse(download_path, filename=file_name)

    except JWTError:
        raise credentials_exception
