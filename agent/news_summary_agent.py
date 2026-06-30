from openai import OpenAI
from settings import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, LLM_TEMPERATURE, LLM_MODEL
import json

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL
)

def summarize_news(news):
    if not news:
        return {
            "summary": "暂无相关新闻",
            "sentiment": "neutral",
            "score": 5
        }

    news_text = ""

    for item in news[:10]:
        news_text += f"""
标题:
{item['title']}

摘要:
{item['summary']}

来源:
{item['source']}

"""

    prompt = f"""
你是一名华尔街资深科技行业分析师。

以下是最近的财经新闻：

{news_text}

请仅返回 JSON，不要输出任何解释，不要使用 Markdown，不要使用 ```json。

格式如下：

{{
    "summary":"100字以内总结",
    "sentiment":"bullish 或 neutral 或 bearish",
    "score":8,
    "advice":"一句投资启示"
}}

要求：

1.summary不超过100字
2.sentiment只能是：
- bullish
- neutral
- bearish
3.score只能是1~10整数
4.返回合法JSON
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是一名专业证券研究员"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return json.loads(response.choices[0].message.content)
