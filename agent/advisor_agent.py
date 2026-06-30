from openai import OpenAI
from settings import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, LLM_MODEL, LLM_TEMPERATURE
from config.fund_mapping import FUND_MAPPING

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL
)

# ======================
# 风险配置
# ======================

ALLOCATION = {
    "low":    (0.5, 0.5, "5%-8%"),
    "medium": (0.7, 0.3, "8%-15%"),
    "high":   (0.9, 0.1, "15%-25%"),
}

RISK_LABEL = {
    "low":    "低风险（稳健型）",
    "medium": "中风险（平衡型）",
    "high":   "高风险（进取型）",
}

SIGNAL_LABEL = {
    "BUY":  "买入 📈",
    "HOLD": "持有 ➡️",
    "SELL": "卖出 📉",
}


def _build_prompt(
    market: dict,
    decision: dict,
    news: dict,
    money: float,
    risk: str,
    invest_money: float,
    cash_money: float,
    expected: str,
    funds: list[str],
) -> str:
    """构建发送给 DeepSeek 的 Prompt。"""

    symbol          = market.get("symbol", "未知标的")
    price           = market.get("price", 0)
    change          = market.get("change", 0)
    market_score    = market.get("score", int(round(change * 10 + 50)))

    signal          = decision.get("signal", "HOLD")
    confidence      = decision.get("confidence", 0)
    reasons         = decision.get("reasons", [])
    reasons_text    = "\n".join(f"  - {r}" for r in reasons) if reasons else "  - 暂无"

    news_summary    = news.get("summary", "暂无新闻")
    news_sentiment  = news.get("sentiment", "neutral")
    news_score      = news.get("score", 5)
    news_advice     = news.get("advice", "")

    funds_text      = "、".join(funds) if funds else "暂无匹配基金"
    risk_label      = RISK_LABEL.get(risk, risk)
    signal_label    = SIGNAL_LABEL.get(signal, signal)

    prompt = f"""
你是一名专业的 基金投资顾问，擅长全球市场与行业趋势分析。
请根据以下量化系统输出的结构化数据，生成一份专业、清晰、有说服力的中文投资建议报告。

=== 标的信息 ===
标的代码：{symbol}
当前价格：{price}
今日涨跌：{change:+.2f}%
市场评分：{market_score}/100

=== 量化决策 ===
AI 信号：{signal_label}
置信度：{confidence}%
决策依据：
{reasons_text}

=== 新闻情绪 ===
情绪倾向：{news_sentiment}（评分 {news_score}/10）
新闻摘要：{news_summary}
投资启示：{news_advice}

=== 用户资产 ===
总可用资金：{money:.0f} 元
风险偏好：{risk_label}
建议投资金额：{invest_money:.0f} 元（{int(invest_money / money * 100)}%）
建议现金保留：{cash_money:.0f} 元（{int(cash_money / money * 100)}%）
预期年化收益：{expected}
推荐基金：{funds_text}

=== 输出要求 ===
请按以下结构输出报告（使用 Markdown 格式，中文）：

1. **市场概况与热点分析**（3-4 句）
2. **技术面解读**（结合 AI 信号和决策依据，2-3 句）
3. **新闻情绪解读**（结合新闻摘要，2-3 句）
4. **仓位建议**（明确说明投资金额、现金保留、推荐基金及理由）
5. **风险提示**（针对当前信号和市场状态，2-3 条）
6. **未来展望**（短期 1 周、中期 1 个月，各一句）

语气专业但易于普通投资者理解，避免过度承诺收益，适当提示风险。
"""
    return prompt


def generate_advice(
    market: dict,
    decision: dict,
    money: float,
    risk: str,
    news: dict | None = None,
) -> str:
    """
    调用 DeepSeek LLM 生成投资建议报告。

    Args:
        market:   market_agent 返回的市场数据
        decision: strategy_agent 返回的决策结果
        money:    用户可用资金（元）
        risk:     风险等级（low / medium / high）
        news:     news_summary_agent 返回的新闻摘要（可选）

    Returns:
        格式化的投资建议报告字符串
    """

    if news is None:
        news = {}

    # ---- 仓位计算 ----
    invest_ratio, cash_ratio, expected = ALLOCATION.get(risk, ALLOCATION["medium"])
    invest_money = money * invest_ratio
    cash_money   = money * cash_ratio

    # ---- 基金匹配 ----
    best_sector = market.get("best_sector", market.get("symbol", ""))
    funds = FUND_MAPPING.get(best_sector, [])

    # ---- 构建 Prompt ----
    prompt = _build_prompt(
        market       = market,
        decision     = decision,
        news         = news,
        money        = money,
        risk         = risk,
        invest_money = invest_money,
        cash_money   = cash_money,
        expected     = expected,
        funds        = funds,
    )

    # ---- 调用 DeepSeek ----
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "你是一名拥有 CFA 资质的专业 QDII 基金投资顾问，"
                        "擅长量化信号解读、全球市场分析和个人资产配置建议。"
                        "输出内容专业、有逻辑、有温度，适合普通散户阅读。"
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=LLM_TEMPERATURE,
        )

        llm_report = response.choices[0].message.content

    except Exception as e:
        # LLM 调用失败时降级为模板报告
        print(f"[advisor_agent] DeepSeek 调用失败，降级为模板报告: {e}")
        llm_report = _fallback_report(market, decision, invest_money, cash_money, expected, funds, risk)

    # ---- 拼接报告头 ----
    signal       = decision.get("signal", "HOLD")
    confidence   = decision.get("confidence", 0)
    signal_label = SIGNAL_LABEL.get(signal, signal)
    risk_label   = RISK_LABEL.get(risk, risk)
    symbol       = market.get("symbol", "未知")

    header = f"""
╔══════════════════════════════════════╗
║         AI 智能投资建议报告          ║
╚══════════════════════════════════════╝

标的：{symbol}　｜　信号：{signal_label}　｜　置信度：{confidence}%
风险偏好：{risk_label}
建议投资：{invest_money:.0f} 元　｜　保留现金：{cash_money:.0f} 元
推荐基金：{"、".join(funds) if funds else "暂无"}
预期收益：{expected}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

    return header + llm_report


def _fallback_report(
    market: dict,
    decision: dict,
    invest_money: float,
    cash_money: float,
    expected: str,
    funds: list[str],
    risk: str,
) -> str:
    """LLM 不可用时的降级模板报告。"""

    signal   = decision.get("signal", "HOLD")
    reasons  = decision.get("reasons", [])

    report = f"""
## 市场概况

当前标的 {market.get('symbol', '未知')} 今日涨跌幅为 {market.get('change', 0):+.2f}%。

## 量化决策

AI 综合技术面、市场面信号，给出 **{signal}** 建议。

主要依据：
"""
    for idx, reason in enumerate(reasons, 1):
        report += f"\n{idx}. {reason}"

    report += f"""

## 仓位建议

建议投入 **{invest_money:.0f} 元**，保留现金 **{cash_money:.0f} 元**。

推荐关注基金：{"、".join(funds) if funds else "暂无"}

预期收益区间：{expected}

## 风险提示

1. 市场存在不确定性，过往业绩不代表未来收益。
2. 请结合个人实际情况合理配置仓位。
3. 投资有风险，入市需谨慎。
"""
    return report