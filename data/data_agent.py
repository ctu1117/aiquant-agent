# data/data_agent.py

import time
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
from polygon import RESTClient

from settings import POLYGON_API_KEY
from strategy.rsi import calculate_rsi

# ===========================
# 初始化
# ===========================

if not POLYGON_API_KEY:
    raise ValueError("POLYGON_API_KEY is not set")

client = RESTClient(api_key=POLYGON_API_KEY)

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)


# ===========================
# 下载数据
# ===========================

def _download_from_polygon(symbol: str, days: int):

    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    for retry in range(5):
        try:
            aggs = client.get_aggs(
                ticker=symbol,
                multiplier=1,
                timespan="day",
                from_=str(start_date),
                to=str(end_date),
                limit=50000
            )

            time.sleep(1)     # 免费API限速
            return aggs

        except Exception as e:

            # Polygon限流
            if "429" in str(e):

                wait = (retry + 1) * 5

                print(f"⚠️ 请求过快，等待 {wait}s 后重试...")

                time.sleep(wait)

                continue

            raise

    raise RuntimeError("Polygon连续请求失败，请稍后再试。")


# ===========================
# 计算指标
# ===========================

def _calculate_indicators(df: pd.DataFrame):

    df = df.sort_values("Date").reset_index(drop=True)

    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA60"] = df["Close"].rolling(60).mean()

    df["RSI"] = calculate_rsi(df)

    return df


# ===========================
# 对外接口
# ===========================

def load_data(symbol: str, days: int, use_cache=True) -> pd.DataFrame:

    cache_file = CACHE_DIR / f"{symbol}_{days}.csv"

    # -------------------------
    # 优先读取缓存
    # -------------------------
    if use_cache and cache_file.exists():

        print(f"📂 读取缓存：{symbol}")

        df = pd.read_csv(cache_file)

        df["Date"] = pd.to_datetime(df["Date"])

        return df

    # -------------------------
    # 下载数据
    # -------------------------
    print(f"⬇️ 下载数据：{symbol}")

    aggs = _download_from_polygon(symbol, days)

    if len(aggs) == 0:
        raise ValueError(f"{symbol} 未获取到任何数据")

    df = pd.DataFrame([{
        "Date": pd.to_datetime(a.timestamp, unit="ms"),
        "Open": a.open,
        "High": a.high,
        "Low": a.low,
        "Close": a.close,
        "Volume": a.volume,
    } for a in aggs])

    # -------------------------
    # 技术指标
    # -------------------------
    df = _calculate_indicators(df)

    # -------------------------
    # 保存缓存
    # -------------------------
    df.to_csv(cache_file, index=False)

    print(f"💾 已缓存：{cache_file}")

    return df