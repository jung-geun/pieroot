from fastapi import FastAPI

from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

app = FastAPI()
app.mount("/assets", StaticFiles(directory="../frontend/dist/assets"))
app.mount("/css", StaticFiles(directory="../frontend/dist/css"))

origins = [
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return FileResponse("../frontend/dist/index.html")


@app.get("/hello")
def hello():
    return {"message": "Hello World"}
