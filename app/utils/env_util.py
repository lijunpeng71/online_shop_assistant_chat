import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

ACCTRUE_LLM_BASE_URL = os.getenv("ACCTRUE_LLM_BASE_URL")
ACCTRUE_LLM_API_KEY = os.getenv("ACCTRUE_LLM_API_KEY")
ACCTRUE_LLM_DEFAULT_MODEL = os.getenv("ACCTRUE_LLM_DEFAULT_MODEL")
