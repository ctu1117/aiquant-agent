from config.fund_mapping import FUND_MAPPING
def generate_advice(
    ranking,
    money,
    risk
):
    best_sector = ranking[0]["sector"]
    best_change = ranking[0]["avg_change"]
    funds=FUND_MAPPING.get(
       best_sector,
       []
    )

    if risk=="low":
       sector_money = money * 0.7
       cash_money = money * 0.3
       expected="5%-8%"
    elif risk=="medium":
       sector_money = money * 0.7
       cash_money = money * 0.3
       expected="8%-15%"
    else:
       sector_money = money * 0.7
       cash_money = money * 0.3
       expected="15%-25%"

    if best_sector == "AI算力":
        return f"""

风险等级：
{risk}

当前最强板块：
{best_sector}

总资金：
{money}元

建议投入：
{sector_money:.0f}元

保留现金：
{cash_money:.0f}元

推荐基金:
{funds}

预期收益：
{expected}
"""

    elif best_sector == "半导体":
        return f"""

风险等级：
{risk}

当前最强板块：
{best_sector}

总资金：
{money}元

建议投入：
{sector_money:.0f}元

保留现金：
{cash_money:.0f}元

推荐基金：
{funds}

预期收益：
{expected}
"""

    else:

     return f"""
风险等级：{risk}
当前最强板块：{best_sector}
平均涨幅：{best_change}%

市场暂无明显主线。

建议：

50% ETF
50% 现金

等待新的机会。
"""