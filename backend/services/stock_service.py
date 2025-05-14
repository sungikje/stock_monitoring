# Lib import
import FinanceDataReader as fdr
from typing import List, Union
import aiomysql
import os
import numpy as np
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import shutil


# Project import
from backend.db.connection import get_pool
from backend.models.user import UserSearchUseEmail
from backend.services.user_service import find_user_by_email
from backend.models.stock import (
    StockInfoResponse,
    SearchFavoriteCompany,
    CompanyInfo,
    UpdateIndustryInfo,
    ViewChart,
)
from backend.config.env import BASE_DIR, STOCK_CHART_PATH
from backend.config.logging import log_call


# Search Company use Company's name, In this case search everything if contains company's name
@log_call
def search_company(name: str) -> Union[List[StockInfoResponse], dict]:
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


# Search Company use Company's name, but only search same company's name
@log_call
def search_company_not_use_contains(name: str) -> StockInfoResponse:
    krx_stocks = fdr.StockListing("KRX")
    company_info = krx_stocks[krx_stocks["Name"] == name]

    if company_info.empty:
        raise ValueError(f"'{name}'에 해당하는 회사를 찾을 수 없습니다.")

    company_info = company_info.iloc[0]

    return StockInfoResponse(
        code=company_info["Code"], name=company_info["Name"], market=company_info["Market"],
    )


@log_call
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


@log_call
async def delete_favorite_company(user_id: str, company_info: CompanyInfo):
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "DELETE FROM user_favorite_companies WHERE user_id = %s AND company_name = %s",
                (user_id, company_info.company_name),
            )

            delete_tf = await cur.fetchall()
            if not delete_tf:
                return {"status": "error", "message": "fail find favorite company"}

            await cur.execute(
                "DELETE FROM user_favorite_companies WHERE user_id = %s AND company_name = %s",
                (user_id, company_info.company_name),
            )
            await conn.commit()
            return {"status": "success"}


@log_call
async def create_favorite_company(user_id: str, create_info_list: List[CompanyInfo]):
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            for company_info in create_info_list:
                await cur.execute(
                    "SELECT * FROM user_favorite_companies WHERE user_id = %s AND company_name = %s",
                    (user_id, company_info.company_name),
                )

                delete_tf = await cur.fetchall()
                if delete_tf:
                    return {"status": "error", "message": "already exist company list"}

                await cur.execute(
                    "INSERT INTO user_favorite_companies (user_id, company_name, industry_period, base_price) VALUES (%s, %s, 2, 50000)",
                    (user_id, company_info.company_name),
                )
            await conn.commit()
            return {"status": "success"}


@log_call
async def update_favorite_company_industry_period(
    user_email: UserSearchUseEmail, update_info: UpdateIndustryInfo
):
    user_response = await find_user_by_email(user_email)
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "UPDATE user_favorite_companies SET industry_period = %s WHERE user_id = %s AND company_name = %s",
                (
                    update_info.industry_period,
                    user_response.id,
                    update_info.company_name,
                ),
            )
            await conn.commit()
            return {"status": "success"}


@log_call
async def get_view_chart(user_email: UserSearchUseEmail) -> List[ViewChart]:
    today = datetime.today().strftime("%Y-%m-%d")
    user = await find_user_by_email(user_email)
    chart_path = os.path.join(BASE_DIR, STOCK_CHART_PATH, today, str(user.id))

    chart_list: List[ViewChart] = []

    if not os.path.exists(chart_path):
        return chart_list 

    for file in os.listdir(chart_path):
        real_file_path = os.path.join(BASE_DIR, STOCK_CHART_PATH, today, str(user.id), file)
        if os.path.isfile(real_file_path):
            name, _ = os.path.splitext(file)
            static_file_path = f"/{STOCK_CHART_PATH}/{today}/{user.id}/{file}"
            chart = ViewChart(company_name=name, save_path=static_file_path)
            chart_list.append(chart)

    return chart_list


@log_call
async def find_user_favorite_company_stock_info(
    user_email: UserSearchUseEmail,
) -> List[ViewChart]:
    user_favorite_company_list = await search_user_favorite_company(user_email)
    user_info = await find_user_by_email(user_email)
    view_charts = []

    for company_info in user_favorite_company_list:
        # need company code
        company_other_info = search_company_not_use_contains(company_info.company_name)
        temp = view_chart(
            user_info.id,
            company_other_info.code,
            company_info.company_name,
            company_info.industry_period,
        )
        if temp != "":
            view_charts.append(temp)

    return view_charts


@log_call
def is_today_chart_exist() -> bool:
    today = datetime.today().strftime("%Y-%m-%d")
    path_to_check = os.path.join(BASE_DIR, STOCK_CHART_PATH, today)

    if os.path.exists(path_to_check):
        return True
    else:
        return False


@log_call
async def make_stock_charts():
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT DISTINCT user_id FROM user_favorite_companies")
            user_list = await cur.fetchall()
    
    for user in user_list:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    "SELECT * FROM user_favorite_companies WHERE user_id = %s",
                    (user['user_id'])
                    )
        user_favorite_company_info = await cur.fetchall()

        # View Chart Param
        for vcp in user_favorite_company_info:
            company_info = search_company_not_use_contains(vcp['company_name'])
            await view_chart(vcp['user_id'], company_info.code, vcp['company_name'], vcp['industry_period'])

@log_call
def clean_stock_charts():
    base_path = os.path.join(BASE_DIR, STOCK_CHART_PATH)
    cutoff = datetime.today() - timedelta(days=7)

    for day_folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, day_folder)
        try:
            folder_date = datetime.strptime(day_folder, "%Y-%m-%d")
            if folder_date < cutoff:
                shutil.rmtree(folder_path)
        except ValueError:
            continue

@log_call
async def view_chart(user_id, company_code, company_name, industry_period):
    today = datetime.today().strftime("%Y-%m-%d")
    period = industry_period * 365
    two_year_ago = (datetime.today() - timedelta(days=period)).strftime("%Y-%m-%d")

    # 주식 데이터 가져오기
    df = fdr.DataReader(company_code, start=two_year_ago, end=today)

    # 이동 평균선 계산
    if industry_period == 1:
        df["SMA_short"] = df["Close"].rolling(window=20).mean()
        df["SMA_long"] = df["Close"].rolling(window=50).mean()
    elif industry_period == 2:
        df["SMA_short"] = df["Close"].rolling(window=50).mean()
        df["SMA_long"] = df["Close"].rolling(window=200).mean()

    # 데드 크로스 여부 (short < long)
    df["Dead_Cross"] = df["SMA_short"] < df["SMA_long"]

    # 오늘자(최신 날짜) 데드 크로스 여부 확인
    today_dead_cross = df["Dead_Cross"].iloc[-1]
    
    # 그래프 시각화
    plt.figure(figsize=(14, 7))

    # 실제 주가는 실선, SMA는 점선으로 표시
    plt.plot(
        df.index,
        df["Close"],
        label="Daily Closing Price",
        color="black",
        alpha=0.6,
        linewidth=2,
    )
    plt.plot(
        df.index,
        df["SMA_short"],
        label="short SMA",
        color="limegreen",
        linestyle="--",
        alpha=0.9,
    )
    plt.plot(
        df.index,
        df["SMA_long"],
        label="long SMA",
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

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chart_path = os.path.join(BASE_DIR, STOCK_CHART_PATH)
    os.makedirs(chart_path, exist_ok=True)

    output_dir = os.path.join(BASE_DIR, STOCK_CHART_PATH, str(today), str(user_id))
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(BASE_DIR, STOCK_CHART_PATH, str(today), str(user_id), f"{company_name}.png")

    plt.savefig(save_path)
    plt.close()
