# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.endpoints import stock_endpoint, user_endpoint
from backend.db.connection import connect_to_mysql, disconnect_from_mysql

app = FastAPI(
    title="Stock Analysis API",
    description="주식 그래프와 기업 분석 정보를 제공하는 API입니다.",
    version="1.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock_endpoint.router, prefix="/api")
app.include_router(user_endpoint.router, prefix="/api")


@app.on_event("startup")
async def startup():
    await connect_to_mysql(app)


@app.on_event("shutdown")
async def shutdown():
    await disconnect_from_mysql(app)


@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀"}
