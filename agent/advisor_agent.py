from config.fund_mapping import FUND_MAPPING

def generate_advice(
    market: dict,
    decision: dict,
    money: float,
    risk: str
):

    best_sector = market.get("best_sector", market.get("symbol", "未知"))
    score = market.get("score", int(round(market.get("change", 0) * 10 + 50)))

    signal = decision.get("signal", "HOLD")
    confidence = decision.get("confidence", int(round(decision.get("score", 0))))
    reasons = decision.get("reasons", [])

    funds = FUND_MAPPING.get(best_sector, [])

    # ======================
    # 风险配置
    # ======================

    allocation = {

        "low": (0.5, 0.5, "5%-8%"),

        "medium": (0.7, 0.3, "8%-15%"),

        "high": (0.9, 0.1, "15%-25%")

    }

    invest_ratio, cash_ratio, expected = allocation.get(
        risk,
        allocation["medium"]
    )

    invest_money = money * invest_ratio
    cash_money = money * cash_ratio

    # ======================
    # 生成建议
    # ======================

    report = f"""
=============================
AI 投资建议
=============================

风险等级：
{risk}

当前最强板块：
{best_sector}

板块评分：
{score}/100

AI决策：
{signal}

决策置信度：
{confidence}%

投资金额：
{invest_money:.0f} 元

现金保留：
{cash_money:.0f} 元

推荐基金：
{", ".join(funds) if funds else "暂无"}

预计收益：
{expected}

推荐理由：
"""

    for idx, reason in enumerate(reasons, 1):

        report += f"\n{idx}. {reason}"

    return report