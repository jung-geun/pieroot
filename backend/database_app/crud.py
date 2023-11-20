from argon2.exceptions import VerifyMismatchError
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from datetime import datetime
from . import models, schemas


def encrypt_password(password, time):
    """
    패스워드를 암호화합니다.

    Args:
        password (str): 암호화할 패스워드
        time (str): 계정의 생성 시간, salt로 사용됩니다.

    Returns:
        dict: {"cmd": "success", "hash_passwd": hash_passwd}
            ? {"cmd": "error", "msg": "비밀번호 암호화 중 오류가 발생했습니다."}
    """
    try:
        ph = PasswordHasher()
        hash_passwd = ph.hash(
            password=password.encode("utf-8"),
            salt=time.strftime("%Y-%m-%d %H:%M:%S").encode("utf-8"),
        )

        return {"cmd": "success", "hash_passwd": hash_passwd}

    except Exception as e:
        # print("Exception > ", e)
        return {"cmd": "error", "msg": "비밀번호 암호화 중 오류가 발생했습니다."}


def hash_check(password, hash_password):
    try:
        ph = PasswordHasher()
        if not ph.verify(hash_password, password.encode("utf-8")):
            return {"cmd": "error", "msg": "비밀번호가 일치하지 않습니다."}
        else:
            return {"cmd": "success", "msg": "비밀번호가 일치합니다."}
    except VerifyMismatchError as e:
        return {"cmd": "error", "msg": "비밀번호가 일치하지 않습니다."}


def get_user(db: Session, mail: str):
    return db.query(models.User).filter(models.User.mail == mail).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """유저 생성

    Args:
        db (Session): _description_
        user (schemas): _description_

    Returns:
        _type_: _description_
    """
    # 유저 생성
    register_date = datetime.now()

    # print(register_date)
    hash_passwd = encrypt_password(user.password, register_date)
    if hash_passwd["cmd"] == "error":
        return {"cmd": "error", "msg": hash_passwd["msg"]}
    db_user = models.User(
        mail=user.mail, password=hash_passwd["hash_passwd"], sign_date=register_date
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    result = {"cmd": "success", "msg": "유저 생성에 성공했습니다."}
    return result


def authenticate_user(db: Session, mail: str, password: str):
    user = get_user(db, mail=mail)

    if not user:
        return {"cmd": "error", "msg": "해당 유저가 존재하지 않습니다."}
    result = hash_check(password, user.password)
    if result["cmd"] == "error":
        return {"cmd": "error", "msg": "비밀번호가 일치하지 않습니다."}
    else:
        return {"cmd": "success", "msg": "로그인에 성공했습니다."}


def get_file_permit(db: Session, id: int):
    file_permit = db.query(models.File).filter(models.File.id == id).first()
    return file_permit
