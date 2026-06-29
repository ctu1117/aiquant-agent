from agent.market_agent import get_market_data
from .analyze_data import SECTORS

def analyze_analyze():

    results = []
    for sector, symbols in SECTORS.items():#遍历每个行业和对应的股票列表
  
        total = 0

        for symbol in symbols:

            data = get_market_data(symbol)

            total += data["change"]

        avg_change = total / len(symbols)

        results.append({
            "sector": sector,
            "avg_change": round(avg_change, 2)
        })
        # 对结果按照平均涨跌幅进行排序，降序排列
    results.sort(
        key=lambda x:x["avg_change"],
        reverse=True
)
    return results