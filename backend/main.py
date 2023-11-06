import json
import logging
import os
from typing import IO, Annotated, List

from database_app import DataBaseApp, init_env
from fastapi import Depends, FastAPI, File, Form, Request, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from file_app import file_router
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

# logger setting
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("logs/router_info.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# env setting
with open("./env.json", "r") as f:
    SECRET = json.load(f)["SECRET_KEY"]

ALGORITHM = "HS256"

init_env("./env.json")

# route
app = FastAPI()

app.include_router(DataBaseApp, tags=["database"])
app.include_router(file_router, tags=["file"])

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory="../frontend/dist/assets"))


@app.get("/")
def index():
    """
    # Index Page Display API
    Index Page를 출력하는 API

    Returns:
        FileResponse: Index Page
    """

    return FileResponse("../frontend/dist/index.html")
