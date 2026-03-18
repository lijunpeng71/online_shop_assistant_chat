from langchain_openai import ChatOpenAI

from app.utils.env_util import ACCTRUE_LLM_BASE_URL, ACCTRUE_LLM_API_KEY, ACCTRUE_LLM_DEFAULT_MODEL

# chat模型
chat_llm_model = ChatOpenAI(base_url=ACCTRUE_LLM_BASE_URL,
                            api_key=ACCTRUE_LLM_API_KEY,
                            model=ACCTRUE_LLM_DEFAULT_MODEL)
