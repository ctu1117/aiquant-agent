from openai import OpenAI
from settings import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, LLM_TEMPERATURE, LLM_MODEL

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

请按照以下格式输出：

【新闻总结】
用100字以内总结新闻核心内容。

【市场情绪】
只能选择：
利好
中性
利空

【情绪评分】
1~10分

【投资启示】
一句话说明对投资者意味着什么。
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
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

    return response.choices[0].message.content
