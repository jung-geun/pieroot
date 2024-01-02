import json

from fastapi.responses import RedirectResponse

from database_app import DataBaseApp, init_env
from fastapi import Depends, FastAPI
from file_app import file_router
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

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
    allow_methods=["*"],
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

@app.exception_handler(404)
async def custom_404_handler(request, exc):
    return RedirectResponse("/#/404")

@app.exception_handler(405)
async def custom_405_handler(request, exc):
    return RedirectResponse("/")