from datetime import datetime

from database_app import Base, DataBase
from fastapi import Depends

from sqlalchemy import (
    BINARY,
    CHAR,
    Column,
    DateTime,
    Integer,
    String,
    delete,
    insert,
    select,
    update,
    ForeignKey,
)
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    mail = Column(String(50), unique=True)
    password = Column(CHAR(128))
    sign_date = Column(DateTime, default=datetime.now())


class File(Base):
    __tablename__ = "file_permit"

    id = Column(Integer, ForeignKey("user.id"), index=True, primary_key=True)
    file = Column(BINARY)
    size = Column(Integer)
    unit = Column(String(2))
    # id 는 user 테이블의 id를 참조합니다.
    # user = relationship("User", back_populates="file_permit")
