from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# Load API key
load_dotenv()

# Initialize LLM (Gemini 2.5 Flash)
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="google/gemini-2.5-flash",
)


@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b."""
    return a * b


llm_with_tools = llm.bind_tools([multiply])

history = []

while True:
    query = input(">")
    history.append(HumanMessage(query))
    response = llm_with_tools.invoke(history)
    history.append(response)
    if (response.tool_calls):
        tool_result = multiply.invoke(response.tool_calls[0])
        history.append(tool_result)
        response_tool = llm_with_tools.invoke(history)
        print(response_tool.content)
        history.append(response_tool)
        continue
    print(response.content)
