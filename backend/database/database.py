import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

env = json.load(open("/home/pieroot/web/backend/database/env.json"))

prptocol = env["protocol"]
server_ip = env["server_ip"]
server_port = env["server_port"]
user = env["user"]
password = env["password"]
database = env["database"]
charset = env["charset"]

SQLALCHEMY_DATABASE_URL = f"{prptocol}://{user}:{password}@{server_ip}:{server_port}/{database}?charset={charset}"


class SQLCONN:
    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

    def get_session(self):
        SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        session = SessionMaker()
        return session

    def get_connection(self):
        return self.engine.connect()
