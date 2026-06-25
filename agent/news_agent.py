import finnhub
import time
from datetime import date, timedelta
from dotenv import load_dotenv
import os
load_dotenv()

client=finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))
# 本地缓存

_news_cache = {}

def get_news(
    symbol,
    days=7,
    limit=15
):
    cache_key = f"{symbol}_{days}"

    if cache_key in _news_cache:
        return _news_cache[cache_key]

    today = date.today()
    start_date = today - timedelta(days=days)

    for i in range(3):
        try:
            news = client.company_news(
                symbol,
                _from=str(start_date),
                to=str(today)
            )
            news = sorted(
                news,
                key=lambda x: x["datetime"],
                reverse=True
            )
            results = []
            for item in news[:limit]:
                results.append({
                    "title": item["headline"],
                    "summary": item["summary"],
                    "source": item["source"],
                    "url": item["url"],
                    "time": item["datetime"]
                })
            _news_cache[cache_key] = results
            return results
        except Exception as e:
            print(f"{symbol} 新闻获取失败 第{i+1}次")
            print(e)
            time.sleep(2)
    return []
