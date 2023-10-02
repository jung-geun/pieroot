import json
import logging
import os
from typing import IO, List

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, HTMLResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount("/assets", StaticFiles(directory="../frontend/dist/assets"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("logs/router_info.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


async def save_upload_file_tmp(file: IO):
    try:
        if not os.path.exists("./tmp"):
            os.makedirs("./tmp")

        file_path = os.path.join("./tmp/", file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

    except Exception as e:
        file_path = {"error": e}

    finally:
        return file_path


@app.get("/")
def index() -> FileResponse:
    """
    # Index Page Display API
    Index Page를 출력하는 API

    Returns:
        FileResponse: Index Page
    """

    return FileResponse("../frontend/dist/index.html")


@app.get("/api/hello")
def hello() -> str:
    """
    # Hello World API
    API 서버에 정상적으로 접속이 가능한지 확인을 위한 API

    Returns:
        str: Hello World 메시지를 json 형태로 반환
    """

    data = {"message": "Hello World"}
    data_json = json.dumps(data).encode("utf-8")
    return data_json


@app.post("/api/file/info")
async def post_file_info(files: List[bytes] = File(...)) -> str:
    """
    # File 정보 출력 API

    Args:
        files (List[bytes]): 정보 출력에 필요한 파일 리스트

    Returns:
        str: 파일 정보를 json 형태로 반환
    """
    data = {}
    try:
        for index, file in enumerate(files):
            data[index] = {"len": len(file)}

    except Exception as e:
        print(e)
        data = {"error": "file info error"}

    finally:
        data_json = json.dumps(data).encode("utf-8")

        return data_json


@app.post("/api/file/upload")
async def post_file_upload(request: Request, files: List[UploadFile] = File(...)):
    """
    # File 업로드 API
    파일 업로드 및 저장된 파일의 정보를 반환

    Args:
        request (Request): Request 객체
        files (List[UploadFile], optional): 파일의 객체. Defaults to File(...).

    Returns:
        HTMLResponse: 파일 업로드 결과를 출력하는 HTML 페이지 반환
    """

    try:
        count = len(files)
        if count > 10:
            raise HTTPException(status_code=400, detail="File count is too large")

        for index, file in enumerate(files):
            # 파일 사이즈 10MB 제한
            file_size = file.file.tell()
            if file_size > 50 * 1024 * 1024:
                raise HTTPException(status_code=400, detail="File size is too large")

            file_path = await save_upload_file_tmp(file)

        html_content = f"""
        <script>
        alert("총 {count} 개의 파일이 업로드가 완료되었습니다.");
        history.back();
        </script>
        """

    except HTTPException as e:
        logger.info(f"HTTP Exception > {e}")
        html_content = f"""
        <script>
        alert("파일 사이즈가 너무 큽니다. (50MB 이하)");
        history.back();
        </script>
        """

    except Exception as e:
        logger.warning(f"Exception > {e}")
        html_content = f"""
        <script>
        alert("파일 업로드 중 오류가 발생하였습니다.");
        history.back();
        </script>
        """

    finally:
        return HTMLResponse(content=html_content, status_code=200)


@app.get("/api/file/list")
async def get_file_list() -> str:
    """
    # File 리스트 출력 API

    Returns:
        str: 파일 리스트를 json 형태로 반환
    """
    try:
        file_list = os.listdir("./tmp")
        data = {"file_list": file_list}

    except Exception as e:
        logger.warning(f"Exception > {e}")
        data = {"error": "file list error"}

    finally:
        data_json = json.dumps(data).encode("utf-8")

        return data_json


@app.get("/api/file/download/{file_name}")
async def get_file_download(request: Request, file_name: str):
    try:
        file_exist = os.path.exists(f"./tmp/{file_name}")
        if not file_exist:
            raise HTTPException(status_code=400, detail="File is not exist")

        return FileResponse(f"./tmp/{file_name}", filename=file_name)

    except HTTPException as e:
        logger.info(f"HTTP Exception > {e}")
        logger.info(f"request_url > {request.url}")
        logger.info(f"request_headers > {request.headers}")

        html_content = f"""
        <script>
        alert("파일이 존재하지 않습니다.");
        history.back();
        </script>
        """

        return HTMLResponse(content=html_content, status_code=200)

    except Exception as e:
        logger.warning(f"Exception > {e}")
        logger.info(f"request_url > {request.url}")
        logger.info(f"request_headers > {request.headers}")

        html_content = f"""
        <script>
        alert("파일 다운로드 중 오류가 발생하였습니다.");
        history.back();
        </script>
        """

        return HTMLResponse(content=html_content, status_code=200)
