import aiomysql
from fastapi import FastAPI

async def connect_to_mysql(app: FastAPI):
    global db_pool
    try:  
      app.state.pool = await aiomysql.create_pool(
          host="localhost",
          port=3306,
          user="root",
          password="",
          db="stock_db",
          autocommit=True
      )
      db_pool = app.state.pool
    except Exception as e:
        print("DB connection fail")

async def disconnect_from_mysql(app: FastAPI):
    app.state.pool.close()
    await app.state.pool.wait_closed()

def get_pool():
    return db_pool