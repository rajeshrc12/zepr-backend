from langchain_openai import ChatOpenAI
from app.core.config import settings

llm = ChatOpenAI(
    base_url=settings.OPENAI_BASE_URL,
    model=settings.OPENAI_BASE_MODEL,
)
