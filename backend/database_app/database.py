import json

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

env = {}


def init_env(env_path="./env.json"):
    global env

    env = json.load(open(env_path))

    protocol = env["protocol"]
    server_ip = env["server_ip"]
    server_port = env["server_port"]
    user = env["user"]
    password = env["password"]
    database = env["database"]
    charset = env["charset"]

    global SQLALCHEMY_DATABASE_URL

    SQLALCHEMY_DATABASE_URL = f"{protocol}://{user}:{password}@{server_ip}:{server_port}/{database}?charset={charset}"


init_env()

Base = declarative_base()


class DataBase:
    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

    def get_session(self):
        SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        session = SessionMaker()
        return session

    def get_connection(self):
        return self.engine.connect()

    def get_engine(self):
        return self.engine
