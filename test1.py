from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()

# Initialize the LLM (Gemini 2.5 Flash via OpenRouter)
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="google/gemini-2.5-flash",  # ✅ Latest Gemini model on OpenRouter
)

messages = [
    ("system", "You are AI Data analyst"),
]

while True:
    query = input(">")
    messages.append(("human", query))
    response = llm.invoke(messages)
    messages.append(("ai", response.content))
    print(messages)
