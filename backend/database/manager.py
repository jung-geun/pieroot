from datetime import datetime
from hashlib import sha256

from database import SQLCONN
from sqlalchemy import (
    BIGINT,
    BINARY,
    INT,
    TEXT,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    delete,
    insert,
    select,
    text,
    update,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    mail = Column(String(40), unique=True)
    pwd = Column(LargeBinary(255))
    sign_date = Column(DateTime, default=datetime.now())

    CONN = SQLCONN()

    def __init__(self) -> None:
        pass

    def select_user_list(self):
        try:
            stmt = select(User)

            with self.CONN.get_connection() as conn:
                result = conn.execute(stmt).fetchall()

            data = {"cmd": "success", "user_list": []}

            for row in result:
                id, mail, pwd, sign_date = row
                data["user_list"].append(
                    {
                        "id": id,
                        "mail": mail,
                        "pwd": "####",  # "pwd": pwd,
                        "sign_date": sign_date.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

        except Exception as e:
            print("Exception > ", e)
            data = {
                "cmd": "error",
                "msg": "select_user_list() Exception > " + str(e),
            }

        finally:
            return data

    def select_user(self, mail):
        try:
            stmt = select(User).where(User.mail == mail)

            with self.CONN.get_connection() as conn:
                result = conn.execute(stmt).fetchall()

            data = {"cmd": "success"}

            id, mail, pwd, sign_date = result[0]

            data["user"] = {
                "id": id,
                "mail": mail,
                "pwd": "####",  # "pwd": pwd,
                "sign_date": sign_date.strftime("%Y-%m-%d %H:%M:%S"),
            }

        except Exception as e:
            print("Exception > ", e)
            data = {"cmd": "error", "msg": "select_user() Exception > " + str(e)}

        finally:
            return data

    def __exist_mail__(self, mail):
        try:
            stmt = select(User).where(User.mail == mail)

            with self.CONN.get_connection() as conn:
                result = conn.execute(stmt).fetchall()

            if len(result) > 0:
                return True
            else:
                return False

        except Exception as e:
            print("Exception > ", e)
            return None

    def __encrypt_password__(self, password, time):
        tmp_passwd = password + time
        hash_passwd = sha256(tmp_passwd.encode("utf-8")).hexdigest().encode("utf-8")
        return hash_passwd

    def insert_user(self, mail, password) -> bool:
        try:
            if self.exist_mail(mail):
                print("이미 존재하는 메일입니다.")
                return False

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            hash_passwd = self.__encrypt_password(password, date)
            tmp_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

            stmt = insert(User).values(mail=mail, pwd=hash_passwd, sign_date=tmp_date)

            with self.CONN.get_connection() as conn:
                conn.execute(stmt)

                conn.commit()

            print("회원가입 완료")
            return True

        except Exception as e:
            print("Exception > ", e)
            return False

    def select_user(self):
        try:
            pass

        except Exception as e:
            print("Exception > ", e)
            return None


if __name__ == "__main__":
    manager = User()
    print(manager.select_user_list())
    # manager.insert_user("test@example.com", "test1234")
