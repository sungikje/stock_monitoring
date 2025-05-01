# backend/main.py

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

from backend.api.endpoints import stock_endpoint, user_endpoint
from backend.db.connection import connect_to_mysql, disconnect_from_mysql
from backend.config.middlewares import TokenMiddleware
from backend.config.scheduler import start_scheduler, stop_scheduler
from backend.config.env import BASE_DIR
from backend.services.stock_service import is_today_chart_exist, make_stock_charts, clean_stock_charts

# if a lot of user? multiprocessing.Pool? Celery async work queue?
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mysql(app)
    start_scheduler()

    clean_stock_charts()
    if not is_today_chart_exist():
        await make_stock_charts()
    
    yield
    await disconnect_from_mysql(app)
    stop_scheduler()


app = FastAPI(
    title="Stock Analysis API",
    description="주식 그래프와 기업 분석 정보를 제공하는 API입니다.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TokenMiddleware)

app.include_router(stock_endpoint.router, prefix="/api")
app.include_router(user_endpoint.router, prefix="/api")

# Chart File access
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR)),  # <-- 여기 주목
    name="static"
)

@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀"}