# Lib import
import FinanceDataReader as fdr
from typing import List
import aiomysql
import os
import numpy as np
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from fastapi.responses import FileResponse

# Project import
from backend.db.connection import get_pool
from backend.models.user import UserSearchUseEmail
from backend.services.user_service import find_user_by_email, user_email_to_id
from backend.models.stock import (
    StockInfoResponse,
    SearchFavoriteCompany,
    CreateFavoriteCompany,
    DeleteFavoriteCompany,
    ViewChart
)


def search_company(name: str) -> List[StockInfoResponse]:
    krx_stocks = fdr.StockListing("KRX")
    company_info = krx_stocks[
        krx_stocks["Name"].str.contains(name, case=False, na=False)
    ]

    if company_info.empty:
        return {"status": "error", "message": "company not found"}

    result = [
        StockInfoResponse(code=row["Code"], name=row["Name"], market=row["Market"])
        for _, row in company_info.iterrows()
    ]

    return result


async def search_user_favorite_company(
    user_email: str,
) -> List[SearchFavoriteCompany]:
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            user_response = await find_user_by_email(user_email)

            await cur.execute(
                "SELECT * FROM user_favorite_companies WHERE user_id = %s",
                (user_response.id,),
            )
            favorite_rows = await cur.fetchall()

            favorite_companies = [SearchFavoriteCompany(**row) for row in favorite_rows]

            return favorite_companies


async def delete_favorite_company(delete_info: DeleteFavoriteCompany):
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT * FROM user_favorite_companies WHERE user_id = %s AND company_name = %s",
                (delete_info.user_id, delete_info.company_name),
            )

            delete_tf = await cur.fetchall()
            if not delete_tf:
                return {"status": "error", "message": "fail find favorite company"}

            await cur.execute(
                "DELETE FROM user_favorite_companies WHERE user_id = %s AND company_name = %s",
                (delete_info.user_id, delete_info.company_name),
            )
            await conn.commit()
            return {"status": "success"}


async def create_favorite_company(user_id: str, create_info: List[CreateFavoriteCompany]):
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            for i in create_info:
                await cur.execute(
                    "SELECT * FROM user_favorite_companies WHERE user_id = %s AND company_name = %s",
                    (user_id, i.company_name),
                )

                delete_tf = await cur.fetchall()
                if delete_tf:
                    return {"status": "error", "message": "already exist company list"}

                await cur.execute(
                    "INSERT INTO user_favorite_companies (user_id, company_name, industry_period, base_price) VALUES (%s, %s, 2, 50000)",
                    (user_id, i.company_name),
                )
            await conn.commit()
            return {"status": "success"}


async def stock_monitoring(user_email: UserSearchUseEmail) -> List[ViewChart]:
    viewChartLists = await find_user_favorite_company_stock_info(user_email)

    if viewChartLists != []:
        return viewChartLists
    else:
        return {"status": "error", "message": "no chart for user"}


async def find_user_favorite_company_stock_info(user_email: UserSearchUseEmail) -> List[ViewChart]:
    user_favorite_company_list = await search_user_favorite_company(user_email)
    user_id = await user_email_to_id(user_email)
    user_favorite_company_stock_info_list = []
    view_charts = []

    for company in user_favorite_company_list:
        for idx in search_company(company.company_name):
            user_favorite_company_stock_info_list.append(idx)

    for company in user_favorite_company_stock_info_list:
        temp = view_chart(user_id, company.code, company.name)
        if temp != "":
            view_charts.append(temp)

    return view_charts

def view_chart(user_id, company_code, company_name) -> ViewChart:
    today = datetime.today().strftime("%Y-%m-%d")
    two_year_ago = (datetime.today() - timedelta(days=730)).strftime("%Y-%m-%d")

    # 주식 데이터 가져오기
    df = fdr.DataReader(company_code, start=two_year_ago, end=today)

    # 이동 평균선 계산
    df["SMA_30"] = df["Close"].rolling(window=30).mean()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()
    df["SMA_200"] = df["Close"].rolling(window=200).mean()

    # 데드 크로스 여부 (50일선 < 200일선)
    df["Dead_Cross"] = df["SMA_50"] < df["SMA_200"]

    # 오늘자(최신 날짜) 데드 크로스 여부 확인
    today_dead_cross = df["Dead_Cross"].iloc[-1]

    # 그래프 시각화
    plt.figure(figsize=(14, 7))

    # 실제 주가는 실선, SMA는 점선으로 표시
    plt.plot(
        df.index,
        df["Close"],
        label="Daily Closing Price",
        color="dodgerblue",
        alpha=0.6,
        linewidth=2,
    )
    plt.plot(
        df.index,
        df["SMA_30"],
        label="30-Day SMA",
        color="red",
        linestyle="--",
        alpha=0.9,
    )
    plt.plot(
        df.index,
        df["SMA_50"],
        label="50-Day SMA",
        color="limegreen",
        linestyle="--",
        alpha=0.9,
    )
    plt.plot(
        df.index,
        df["SMA_200"],
        label="200-Day SMA",
        color="orange",
        linestyle="--",
        alpha=0.9,
    )

    # 데드 크로스 포인트 색상 및 스타일 변경 (아이콘 크기 조정)
    dead_cross_dates = df.index[df["Dead_Cross"]]
    plt.scatter(
        dead_cross_dates,
        df.loc[dead_cross_dates, "Close"],
        color="crimson",
        marker="v",
        label="Dead Cross",
        alpha=1,
        s=25,
    )

    # 최신 날짜 데드 크로스 여부 출력
    if today_dead_cross:
        plt.title(f"{company_code} - Dead Cross O")
    else:
        plt.title(f"{company_code} - Dead Cross X")

    # 그래프 세부 설정
    plt.xticks(df.index[::14], rotation=45)
    plt.yticks(
        np.arange(
            df["Close"].min(),
            df["Close"].max() + (df["Close"].max() * 0.05),
            df["Close"].max() * 0.05,
        )
    )
    plt.xlabel("Date")
    plt.ylabel("Closing Price (KRW)")
    plt.legend()
    plt.grid(True)

    # 그래프 저장
    output_dir = f"../stock_chart/{user_id}"
    os.makedirs(output_dir, exist_ok=True)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend/
    output_dir = os.path.join(BASE_DIR, "stock_chart", str(user_id), str(today))
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, f"{company_name}.png")

    plt.savefig(save_path)
    plt.close()

    static_path = '/' + str(user_id) + '/' + str(today) + '/' + f"{company_name}.png"

    if os.path.exists(save_path):
        print(f"✅ 그래프 저장 완료: {save_path}")
        return ViewChart(
            company_name=company_name,
            save_path=static_path
        )
    else:
        print(f"❌ 저장 실패: {save_path}")
        return ""
