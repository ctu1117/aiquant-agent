import os
from dotenv import load_dotenv

load_dotenv()

# Finnhub API Key
FINNHUB_API_KEY = os.environ.get("FINNHUB_API_KEY")

# DeepSeek API Key
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# LLM 配置
LLM_TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", "0.3"))
LLM_MODEL = os.environ.get("LLM_MODEL", "deepseek-chat")

POLYGON_API_KEY = os.environ.get("POLYGON_API_KEY")