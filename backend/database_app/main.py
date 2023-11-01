import json
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

with open("./env.json", "r") as f:
    SECRET = json.load(f)["SECRET_KEY"]

ALGORITHM = "HS256"


models.Base.metadata.create_all(bind=DataBase().get_engine())

router = APIRouter(
    prefix="/users",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


# Dependency
def get_db():
    db = DataBase().get_session()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    mail = form_data.username
    password = form_data.password

    user = schemas.UserCreate(mail=mail, password=password)

    result = crud.create_user(db, user)

    if result["cmd"] == "error":
        raise HTTPException(
            status_code=400,
            detail=result["msg"],
        )
    else:
        return JSONResponse({"detail": "회원가입이 완료되었습니다."}, status_code=200)


def create_access_token(username: str, expires_delta: datetime):
    data = {"sub": username, "exp": expires_delta}
    access_token = jwt.encode(data, SECRET, algorithm=ALGORITHM)
    return access_token


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="로그인이 필요합니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception


@router.post("/login")
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    if not form_data.username:
        raise HTTPException(
            status_code=401,
            detail="mail을 입력해주세요.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not form_data.password:
        raise HTTPException(
            status_code=401,
            detail="비밀번호를 입력해주세요.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    mail = form_data.username
    password = form_data.password

    result = crud.authenticate_user(db, mail, password)

    if result["cmd"] == "error":
        raise HTTPException(
            status_code=401,
            detail="아이디 또는 비밀번호가 일치하지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        cookie_expires = timedelta(minutes=30)
        access_token_expires = datetime.utcnow() + cookie_expires
        access_token = create_access_token(mail, access_token_expires)

        return JSONResponse(
            {"access_token": access_token, "token_type": "bearer", "username": mail},
            status_code=200,
        )


@router.get("/me")
def get_me(request: Request):
    try:
        token = request.headers["Authorization"].split(" ")[1]

        username = get_current_user(token)

        if username is None:
            raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
        else:
            return JSONResponse({"username": username}, status_code=200)
    except:
        return JSONResponse({"username": None}, status_code=200)


@router.post("/refresh")
def refresh_token(request: Request):
    try:
        token = request.headers["Authorization"].split(" ")[1]
        username = get_current_user(token)

        cookie_expires = timedelta(minutes=30)
        access_token_expires = datetime.utcnow() + cookie_expires
        access_token = create_access_token(
            username,
            access_token_expires,
        )
        return JSONResponse(
            {
                "access_token": access_token,
                "token_type": "bearer",
                "username": username,
            },
            status_code=200,
        )
    except JWTError:
        return JSONResponse({"username": None}, status_code=200)
    except ExpiredSignatureError:
        return JSONResponse({"username": None}, status_code=200)
