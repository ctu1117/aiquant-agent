def make_decision(
    technical,
    market,
    news
):

    score = 0

    reasons = []

    # =====================
    # 技术面
    # =====================

    if technical["trend"] == "UP":

        score += 30

        reasons.append("均线多头趋势")

    if technical["rsi_signal"] == "NORMAL":

        score += 20

        reasons.append("RSI健康")

    if technical["ma_signal"] == "BUY":

        score += 20

        reasons.append("均线金叉")

    # =====================
    # 板块
    # =====================

    market_score = market.get("score", 0)
    if market_score >= 80:
        score += 20
        reasons.append("热门板块")

    # =====================
    # 新闻
    # =====================

    sentiment = news.get("sentiment", "").lower()
    if sentiment in ["利好", "bullish"]:
        score += 10
        reasons.append("新闻利好")

    # =====================
    # 最终决策
    # =====================

    if score >= 70:
        signal = "BUY"
    elif score >= 45:
        signal = "HOLD"
    else:
        signal = "SELL"

    return {
        "signal": signal,
        "score": score,
        "confidence": int(min(max(score, 0), 100)),
        "reasons": reasons
    }