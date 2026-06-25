from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def generate_llm_report(
    ranking,
    money,
    risk,
    news
):

    prompt = f"""
例举当前板块排名和走势：
{ranking}

相关新闻：
{news}

用户资金：
{money}元

风险等级：
{risk}

请以专业投资顾问身份：

1. 结合{news}和{ranking}分析当前市场热点
2. 结合{ranking}给出投资建议
3. 结合{money}给出仓位建议
4. 给出风险提示
5. 给出未来展望

输出格式清晰专业。
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role":"system",
                "content":"你是一名专业QDII基金投资顾问，擅长分析全球市场和行业趋势，给出精准投资建议"
            },
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content