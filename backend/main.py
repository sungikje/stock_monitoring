# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.endpoints import stock_endpoint  # 직접 만든 엔드포인트 import

app = FastAPI(
    title="Stock Analysis API",
    description="주식 그래프와 기업 분석 정보를 제공하는 API입니다.",
    version="1.0.0"
)

# CORS 설정 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock_endpoint.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀"}