import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import IO, Annotated, List

from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    File,
    HTTPException,
    Request,
    Response,
    UploadFile,
)
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session
from starlette.responses import FileResponse, HTMLResponse, JSONResponse

from . import crud, models, schemas
from .database import DataBase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("logs/router_user_info.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


with open("./env.json", "r") as f:
    SECRET = json.load(f)["SECRET_KEY"]

ALGORITHM = "HS256"


models.Base.metadata.create_all(bind=DataBase().get_engine())

router = APIRouter(
    prefix="/users",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

credentials_exception = HTTPException(
    status_code=401,
    detail="Unauthorized",
    headers={"WWW-Authenticate": "Bearer"},
)


# Dependency
def get_db():
    """DB 세션을 생성하는 함수

    Yields:
        Session: DB 세션
    """
    db = DataBase().get_session()
    try:
        yield db
    finally:
        db.close()


def create_access_token(fingerprint: str, username: str, expires_delta: datetime):
    """access_token을 생성하는 함수

    Args:
        username (str): 유저의 이름
        expires_delta (datetime): 토큰의 만료 시간

    Returns:
        dict: access_token
    """
    data = {
        "sub": fingerprint,
        "name": username,
        "exp": datetime.utcnow() + expires_delta,
    }
    access_token = jwt.encode(data, SECRET, algorithm=ALGORITHM)
    return access_token


def get_current_user(token: str = Depends(oauth2_scheme)):
    """토큰을 확인하는 함수

    Args:
        token (str, optional): 유저의 토큰. Defaults to Depends(oauth2_scheme).

    Raises:
        credentials_exception: Unauthorized

    Returns:
        str: 유저의 이름
    """
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        fingerprint: str = payload.get("sub")
        username: str = payload.get("name")

        if username is None:
            raise credentials_exception
        return (fingerprint, username)
    except JWTError:
        logger.info(f"JWTError: token decode error")
        raise credentials_exception


def get_device_fingerprint(request: Request):
    """유저의 디바이스 정보를 확인하는 함수
    유저의 디바이스 정보를 확인하고, sha256으로 암호화하여 반환합니다.

    Args:
        request (Request): Request 객체

    Returns:
        str: 유저의 디바이스 정보
    """
    try:
        user_agent = request.headers.get("User-Agent", "")
        device_type = request.headers.get("Device-Type", "Unknown")
        operating_system = request.headers.get("Operating-System", "Unknown")
        screen_resolution = request.headers.get("Screen-Resolution", "Unknown")
        browser_settings = request.headers.get("Browser-Settings", "Unknown")
        language_preferences = request.headers.get("Accept-Language", "Unknown")
        timezone = request.headers.get("Timezone", "Unknown")

        device_fingerprint = {
            "user_agent": user_agent,
            "device_type": device_type,
            "operating_system": operating_system,
            "screen_resolution": screen_resolution,
            "browser_settings": browser_settings,
            "language_preferences": language_preferences,
            "timezone": timezone,
        }

        fingerprint = hashlib.sha256(
            json.dumps(device_fingerprint).encode()
        ).hexdigest()

        return fingerprint
    except:
        return None


@router.post("/create")
def create_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """회원가입을 하는 API

    Args:
        form_data (OAuth2PasswordRequestForm, optional): 유저 로그인 form. Defaults to Depends().
        db (Session, optional): db session. Defaults to Depends(get_db).

    Raises:
        HTTPException:

    Returns:
        _type_: _description_
    """
    try:
        mail = form_data.username
        password = form_data.password

        user = schemas.UserCreate(mail=mail, password=password)

        result = crud.create_user(db, user)

        if result["cmd"] == "error":
            raise HTTPException(
                status_code=402,
                detail=result["msg"],
            )
        else:
            return JSONResponse({"detail": "회원가입이 완료되었습니다."}, status_code=200)

    except InvalidCredentialsException:
        logger.error(f"InvalidCredentialsException: {mail}")
        raise credentials_exception


@router.post("/token")
def token_login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """로그인을 하는 API

    Args:
        form_data (OAuth2PasswordRequestForm, optional): 로그인 폼. Defaults to Depends().

    Raises:
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        JSONResponse: _description_
    """
    try:
        if not form_data.username:
            logger.info(f"InvalidCredentialsException: mail > {form_data.username}")
            raise HTTPException(
                status_code=401,
                detail="mail을 입력해주세요.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not form_data.password:
            logger.info(f"InvalidCredentialsException: password > ####")
            raise HTTPException(
                status_code=401,
                detail="비밀번호를 입력해주세요.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        mail = form_data.username
        password = form_data.password

        result = crud.authenticate_user(db, mail, password)

        if result["cmd"] == "error":
            logger.info(f"InvalidCredentialsException: {mail}")
            raise HTTPException(
                status_code=401,
                detail="아이디 또는 비밀번호가 일치하지 않습니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            request_fingerprint = get_device_fingerprint(request)
            access_token_expires = timedelta(minutes=30)
            access_token = create_access_token(
                request_fingerprint,
                mail,
                access_token_expires,
            )

            response = JSONResponse(
                {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "username": mail,
                },
                status_code=200,
            )

            refresh_expires = timedelta(days=30)
            refresh_token = create_access_token(
                request_fingerprint,
                mail,
                refresh_expires,
            )
            response.set_cookie(
                key="access_token",  # 쿠키의 이름을 access_token으로 합니다.
                value=f"Bearer {refresh_token}",  # access_token을 쿠키에 저장합니다.
                httponly=True,  # javascript에서 쿠키를 접근할 수 없습니다.
                secure=True,  # https에서만 쿠키를 전송합니다.
                samesite="lax",  # csrf 공격 방지
                expires=refresh_expires,  # 30분 뒤에 쿠키가 만료됩니다.
            )

            return response

    except InvalidCredentialsException:
        logger.info(f"InvalidCredentialsException: {mail}")
        raise credentials_exception


@router.delete("/token")
def token_delete():
    """로그아웃을 하는 API
    토큰을 삭제합니다.
    """

    response = JSONResponse({"detail": "로그아웃이 완료되었습니다."}, status_code=200)
    response.delete_cookie("access_token")
    return response


@router.get("/token")
def token_get(token: str = Depends(oauth2_scheme)):
    """나의 토큰을 확인하는 API
    토큰 정보를 확인합니다.
    """
    try:
        payload = get_current_user(token)
        username = payload[1]
        if username is None:
            logger.info(f"InvalidCredentialsException: {username}")
            raise credentials_exception
        else:
            return JSONResponse({"username": username}, status_code=200)
    except:
        logger.info(f"InvalidCredentialsException: {username}")
        raise credentials_exception


@router.patch("/token")
def token_refresh(
    request: Request,
):
    """토큰을 갱신하는 API
    쿠키에 저장된 정보를 바탕으로 토큰을 갱신합니다.
    """
    try:
        refresh_token = request.cookies.get("access_token").split(" ")[1]

        payload = get_current_user(refresh_token)
        store_fingerprint = payload[0]
        username = payload[1]
        request_fingerprint = get_device_fingerprint(request)

        if store_fingerprint != request_fingerprint:
            logger.info(f"InvalidCredentialsException: {username}")
            raise credentials_exception

        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            request_fingerprint,
            username,
            access_token_expires,
        )

        response = JSONResponse(
            {
                "access_token": access_token,
                "token_type": "bearer",
                "username": username,
            },
            status_code=200,
        )

        refresh_expires = timedelta(days=30)
        refresh_token = create_access_token(
            request_fingerprint,
            username,
            refresh_expires,
        )
        response.set_cookie(
            key="access_token",  # 쿠키의 이름을 access_token으로 합니다.
            value=f"Bearer {refresh_token}",  # access_token을 쿠키에 저장합니다.
            httponly=True,  # javascript에서 쿠키를 접근할 수 없습니다.
            secure=True,  # https에서만 쿠키를 전송합니다.
            samesite="lax",  # csrf 공격 방지
            expires=refresh_expires,  # 30분 뒤에 쿠키가 만료됩니다.
        )

        return response

    except JWTError:
        logger.info(f"token refresh error")
        raise credentials_exception
    except:
        logger.info("token refresh error")
        raise credentials_exception
