from contextlib import asynccontextmanager

import typer
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from api.v1 import api_router
from core.config import settings
from services.etcd import EtcdClient
from services.mongodb import MongoDB

cli = typer.Typer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    async with MongoDB() as mongo:
        with EtcdClient() as etcd:
            await mongo.test_connection()
            etcd.test_connection()
            yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# 注册 v1 版本的所有路由
app.include_router(api_router, prefix=settings.API_V1_STR)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，生产环境建议设置具体的源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 headers
)


@app.get("/")
async def root():
    return {"message": "Welcome to Cron API"}


@app.get("/ping", response_class=PlainTextResponse)
async def pingpong():
    return "pong"


@cli.command()
def run_app(dotenv_path: str = "d:/.env", host: str = "0.0.0.0", port: int = 8000):
    load_dotenv(dotenv_path)
    settings.reload()
    uvicorn.run("cron_api.main:app", host=host, port=port, reload=False)
