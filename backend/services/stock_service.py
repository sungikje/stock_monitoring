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
from backend.models.stock import (
    StockInfoResponse,
    SearchFavoriteCompany,
    CompanyInfo,
    UpdateIndustryInfo,
    ViewChart,
)
from backend.config.env import BASE_DIR, STOCK_GRAPH_PATH
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
async def search_user_interesting_company() -> List[SearchFavoriteCompany]:
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM user_interesting_companies_alone_table")
            favorite_rows = await cur.fetchall()

            favorite_companies = [SearchFavoriteCompany(**row) for row in favorite_rows]

            return favorite_companies


@log_call
async def delete_interesting_company(user_id: str, company_info: CompanyInfo):
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT * FROM user_interesting_companies_alone_table WHERE company_name = %s",
                (company_info.company_name),
            )

            delete_tf = await cur.fetchall()
            if not delete_tf:
                return {"status": "error", "message": "fail find favorite company"}

            await cur.execute(
                "DELETE FROM user_interesting_companies_alone_table WHERE company_name = %s",
                (company_info.company_name),
            )
            await conn.commit()
            return {"status": "success"}


@log_call
async def create_interesting_company(user_id: str, create_info_list: List[CompanyInfo]):
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            for company_info in create_info_list:
                await cur.execute(
                    "SELECT * FROM user_interesting_companies_alone_table WHERE company_name = %s",
                    (company_info.company_name),
                )

                delete_tf = await cur.fetchall()
                if delete_tf:
                    return {"status": "error", "message": "already exist company list"}

                await cur.execute(
                    "INSERT INTO user_interesting_companies_alone_table (company_name, industry_period) VALUES (%s, 2)",
                    (company_info.company_name),
                )
            await conn.commit()
            return {"status": "success"}


@log_call
async def update_interesting_company_industry_period(
    update_info: UpdateIndustryInfo
):
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "UPDATE user_interesting_companies_alone_table SET industry_period = %s WHERE company_name = %s",
                (
                    update_info.industry_period,
                    update_info.company_name,
                ),
            )
            await conn.commit()
            return {"status": "success"}

@log_call
async def create_stock_moniotring_graph():
    today = datetime.today().strftime("%Y-%m-%d")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_path = os.path.join(BASE_DIR, STOCK_GRAPH_PATH, str(today))

    file_names = []
    try:
        file_names = os.listdir(save_path)
        file_names = [name.replace(".png", "") for name in file_names]
        print("file name:", file_names)
    except FileNotFoundError:
        print(f"오류: '{save_path}' 경로를 찾을 수 없습니다.")
    except NotADirectoryError:
        print(f"오류: '{save_path}'은(는) 디렉토리가 아닙니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

    search_favorite_companies = await search_user_interesting_company()
    favorite_company_list = []
    for company_info in search_favorite_companies:
        favorite_company_list.append(company_info.company_name)
    print("favorite company list: ", favorite_company_list)

    for name in file_names:
        favorite_company_list.remove(name)

    if len(favorite_company_list) != 0:
        await create_stock_graphs()
    else:
        print("already exist")
        return {"status": "error", "message": "already exist"}


@log_call
async def get_view_graph() -> List[ViewChart]:
    today = datetime.today().strftime("%Y-%m-%d")
    graph_path = os.path.join(BASE_DIR, STOCK_GRAPH_PATH, today)

    graph_list: List[ViewChart] = []

    if not os.path.exists(graph_path):
        return graph_list 

    for file in os.listdir(graph_path):
        real_file_path = os.path.join(BASE_DIR, STOCK_GRAPH_PATH, today, file)
        if os.path.isfile(real_file_path):
            name, _ = os.path.splitext(file)
            static_file_path = f"/{STOCK_GRAPH_PATH}/{today}/{file}"
            graph = ViewChart(company_name=name, save_path=static_file_path)
            graph_list.append(graph)

    return graph_list


@log_call
async def find_user_favorite_company_stock_info() -> List[ViewChart]:
    user_interesting_company_list = await search_user_interesting_company()
    view_graphs = []

    for company_info in user_interesting_company_list:
        # need company code
        company_other_info = search_company_not_use_contains(company_info.company_name)
        temp = view_graph(
            company_other_info.code,
            company_info.company_name,
            company_info.industry_period,
        )
        if temp != "":
            view_graphs.append(temp)

    return view_graphs


@log_call
def is_today_graph_exist() -> bool:
    today = datetime.today().strftime("%Y-%m-%d")
    path_to_check = os.path.join(BASE_DIR, STOCK_GRAPH_PATH, today)

    if os.path.exists(path_to_check):
        return True
    else:
        return False


@log_call
async def create_stock_graphs():
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM user_interesting_companies_alone_table")
    user_favorite_company_info = await cur.fetchall()

    # View Chart Param
    for vcp in user_favorite_company_info:
        company_info = search_company_not_use_contains(vcp['company_name'])
        await view_graph(company_info.code, vcp['company_name'], vcp['industry_period'])


@log_call
def clean_stock_graphs():
    base_path = os.path.join(BASE_DIR, STOCK_GRAPH_PATH)
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
async def view_graph(company_code, company_name, industry_period):
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
    graph_path = os.path.join(BASE_DIR, STOCK_GRAPH_PATH)
    os.makedirs(graph_path, exist_ok=True)

    output_dir = os.path.join(BASE_DIR, STOCK_GRAPH_PATH, str(today))
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(BASE_DIR, STOCK_GRAPH_PATH, str(today), f"{company_name}.png")

    plt.savefig(save_path)
    plt.close()