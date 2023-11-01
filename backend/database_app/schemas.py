from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    mail: str


class UserCreate(UserBase):
    mail: str
    password: str


class UserLogin(BaseModel):
    mail: str
    password: str


class User(BaseModel):
    id: int
    mail: str
    sign_date: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    mail: str


class TokenData(BaseModel):
    mail: Optional[str] = None


# 파일 업로드 권한 - 파일 업로드 권한을 가진 유저의 id를 저장합니다.
class FilePermit(BaseModel):
    id: int
    file: bool

    class Config:
        from_attributes = True


# 파일 업로드 권한 추가 - 파일 업로드 권한을 추가합니다. (기존에 권한이 없는 경우)
class FilePermitAdd(BaseModel):
    id: int
    file: bool

    class Config:
        from_attributes = True


# 파일 업로드 권한 삭제 - 파일 업로드 권한을 삭제합니다. (기존에 권한이 있는 경우)
class FilePermitDelete(BaseModel):
    id: int
    file: bool

    class Config:
        from_attributes = True
