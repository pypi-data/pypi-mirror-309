import os

import typer
from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine, text

from crypto.grid_strategy import (
    grid_sync_close,
    grid_sync_open,
    strategy_sync_close,
    strategy_sync_open,
)

app = typer.Typer()


def get_database_engine(env_path: str) -> Engine:
    """创建数据库引擎"""
    load_dotenv(env_path)
    host = os.getenv("UNI_CLI_MYSQL_HOST")
    port = os.getenv("UNI_CLI_MYSQL_PORT")
    user = os.getenv("UNI_CLI_MYSQL_USER")
    password = os.getenv("UNI_CLI_MYSQL_PASSWORD")
    database = os.getenv("UNI_CLI_MYSQL_DATABASE")

    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as e:
        print(f"数据库连接失败: {str(e)}")
        raise

    return engine


@app.command()
def grid(env_path: str = "d:/.env", csv_path: str = "d:/github/txnj/data/grid_0.csv"):
    """同步mysql中grid数据到csv文件"""
    engine = get_database_engine(env_path)
    grid_sync_close(engine, csv_path)
    grid_sync_open(engine, csv_path)


@app.command()
def strategy(
    env_path: str = "d:/.env", csv_path: str = "d:/github/txnj/data/strategy_0.csv"
):
    """同步mysql中strategy数据到csv文件"""
    engine = get_database_engine(env_path)
    strategy_sync_close(engine, csv_path)
    strategy_sync_open(engine, csv_path)
