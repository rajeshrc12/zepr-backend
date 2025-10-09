from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, AgentExecutor

# Load API key
load_dotenv()

# Initialize LLM (Gemini 2.5 Flash)
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="google/gemini-2.5-flash",
)


@tool
def get_weather(location: str, date: Optional[str] = None) -> str:
    """Get the current or forecasted weather for a given location and optional date."""
    today = datetime.now().strftime("%Y-%m-%d")

    if date and date != today:
        return f"Weather forecast for {location} on {date}: Partly cloudy, 22°C."
    if "london" in location.lower():
        return "Rainy in London, 16°C."
    return f"Clear skies in {location}, 20°C."


@tool
def calculate_travel_time(origin: str, destination: str, mode: str = "driving") -> str:
    """Calculate estimated travel time between origin and destination using a specific mode."""
    base_times = {"driving": 30, "walking": 120, "transit": 45, "cycling": 60}
    if mode not in base_times:
        mode = "driving"
    time = base_times[mode] + hash(f"{origin}-{destination}") % 100

    hours = time // 60
    minutes = time % 60
    if hours:
        return f"Travel from {origin} to {destination} by {mode}: {hours}h {minutes}m."
    return f"Travel from {origin} to {destination} by {mode}: {minutes} minutes."


system_prompt = """You are a helpful travel and weather assistant. 
Use the tools provided to respond to user queries accurately and kindly."""
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])


tools = [get_weather, calculate_travel_time]
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)


def ask_agent(query):
    response = agent_executor.invoke({"input": query})
    return response["output"]


if __name__ == "__main__":
    print("Welcome to your Travel & Weather Assistant!")
    while True:
        user_input = input("Ask something: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        try:
            print("Assistant:", ask_agent(user_input))
        except Exception as e:
            print("Error:", e)
