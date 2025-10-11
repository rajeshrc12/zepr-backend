from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage

# Load API key
load_dotenv()


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="google/gemini-2.5-flash",
)


def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


# Build the graph
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Compile chatbot
chatbot = graph.compile()

# Initialize conversation
state = {
    "messages": [SystemMessage(content="You are AI Data Analyst. Talk naturally and help with data insights.")]
}

# Chat loop
while True:
    query = input("> ")
    if query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    if query.lower() in ["list"]:
        print(state["messages"])
        continue
    # Add user input
    state["messages"].append(HumanMessage(content=query))

    # Get model response
    result = chatbot.invoke(state)
    ai_reply = result["messages"][-1].content

    # Display
    print(ai_reply)

    # Update state for next turn
    state["messages"].append(AIMessage(content=ai_reply))
