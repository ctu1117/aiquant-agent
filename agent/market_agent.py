import time
import finnhub
from dotenv import load_dotenv
import os
load_dotenv()

client=finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

# 本地缓存
_cache = {}

def get_market_data(symbol):

    # 如果已经获取过，直接返回
    if symbol in _cache:
        return _cache[symbol]

    for i in range(3):

        try:

            data = client.quote(symbol)

            current = data["c"]
            previous = data["pc"]

            if previous == 0:
                change = 0
            else:
                change = (
                    current - previous
                ) / previous * 100

            result = {
                "symbol": symbol,
                "price": current,
                "change": round(change, 2)
            }#返回当前价格和涨跌幅

            # 写入缓存
            _cache[symbol] = result

            return result

        except Exception as e:

            print(
                f"{symbol} 第{i+1}次请求失败: {e}"
            )

            time.sleep(2)

    print(f"{symbol} 获取失败")

    return {
        "symbol": symbol,
        "price": 0,
        "change": 0
    }