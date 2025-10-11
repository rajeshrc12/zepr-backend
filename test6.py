from typing_extensions import TypedDict
from typing import Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from app.core.prompts import get_data_analyst_prompt
from pydantic import BaseModel
import json
# Load API key
load_dotenv()

# Define chat state


class ChatState(TypedDict):
    message: str
    query_type: str
    normal_query: str
    analysis_query: str
    table: str


class QueryAnalyzerOutputSchema(BaseModel):
    type: str


class NormalQueryOutputSchema(BaseModel):
    answer: str


# Initialize LLM (Gemini 2.5 Flash via OpenRouter)
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="google/gemini-2.5-flash-lite",
)

# Define the chat node logic


def query_analyzer(state: ChatState):
    prompt = f"""
    You are a Query Analyzer.
    Your task is to classify the user's query into one of the following types based on its intent:

    1.type: "normal"
    - The user is greeting (e.g., “hi”, “hello”).
    - The user is asking about table details such as table name, description, or column names.
    - Any other irrelevant query

    2.type: "analysis"
    - The user is asking for analytical insights or data queries.
    - Examples include requests like:
    - Show top 5 records
    - Generate a chart for this data
    - Give me analysis based on table columns

    Your output must be a one of below JSON object in the following format:
    {{
    "type": "normal"
    }}
    OR
    {{
    "type": "analysis"
    }}

    """
    structured_llm = llm.bind_tools(
        [],
        response_format=QueryAnalyzerOutputSchema,
        strict=True,
    )
    messages = [SystemMessage(content=prompt),
                HumanMessage(content=state["message"])]

    response = structured_llm.invoke(messages)
    response_json = json.loads(response.content)
    return {"query_type": response_json["type"]}


def query_decision(state: ChatState):
    if (state["query_type"] == "normal"):
        return "normal_query"
    if (state["query_type"] == "analysis"):
        return "analysis_query"


def normal_query(state: ChatState):
    prompt = f"""
    You are an AI Data Analyst.

    You have access to the following dataset:

    Table Name: Netflix
    Table description: This contains all show details about netflix
    Schema:
    - UserID (TEXT)
    - ShowTitle (TEXT)
    - Genre (TEXT)
    - WatchDate (TIMESTAMP)

    Your task is to respond to user greetings (e.g., “hi”, “hello”) and answer any queries related to the dataset, such as:
    Providing the table name and description
    Provide available columns based on user query.
    only respond to table related queries.
    Provide data in object with "answer" key and your response in value

    Output Format:
    Return your response as a JSON object with an "answer" key containing your message.

    Example output
    {{
        "answer":"Hi, how are you ?"
    }}
    """
    structured_llm = llm.bind_tools(
        [],
        response_format=NormalQueryOutputSchema,
        strict=True,
    )
    messages = [SystemMessage(content=prompt),
                HumanMessage(content=state["message"])]

    response = structured_llm.invoke(messages)
    response_json = json.loads(response.content)
    return {"normal_query": response_json["answer"]}


def analysis_query(state: ChatState):
    prompt = f"""
    You are an SQL Query Generator. Your task is to generate SQL queries based on the user's request.
    
    SQL Table Name: csv_cmewh96du000dt9xothtzer2u
    Schema:
    - UserID (TEXT)
    - ShowTitle (TEXT)
    - Genre (TEXT)
    - WatchDate (TIMESTAMP)

    Instruction:
    - Generate only one SQL query.
    - Ignore any mentions of chart types, visualizations, or other non-SQL instructions. Focus only on generating correct SQL queries.
    - Use double quotes for table and column names exactly as in the schema.
    - Match data types correctly in WHERE clauses; handle nullable columns.
    - Never reference columns not in the schema.
    - Always return Top 5 results using ORDER BY + LIMIT 5.
    - Arrange columns: first = categorical, last = numerical, others in between.
    - Do not include explanations, comments, or any extra text in SQL output.
    - Output must be sql query.

    Output Format:
    Return your response as a JSON object with an "answer" key containing sql.

    Example output
    {{
        "answer":"SELECT \"Country\", COUNT(*) AS customer_count FROM \"csv_cmewh96du000dt9xothtzer2u\" GROUP BY \"Country\" ORDER BY customer_count DESC LIMIT 5;"
    }}
    """
    structured_llm = llm.bind_tools(
        [],
        response_format=NormalQueryOutputSchema,
        strict=True,
    )
    messages = [SystemMessage(content=prompt),
                HumanMessage(content=state["message"])]

    response = structured_llm.invoke(messages)
    response_json = json.loads(response.content)
    return {"analysis_query": response_json["answer"]}


def generate_table(state: ChatState):
    return {"table": "[]"}


# Build the graph
graph = StateGraph(ChatState)
graph.add_node("query_analyzer", query_analyzer)
graph.add_node("normal_query", normal_query)
graph.add_node("analysis_query", analysis_query)
graph.add_node("generate_table", generate_table)

graph.add_edge(START, "query_analyzer")
graph.add_conditional_edges("query_analyzer", query_decision, {
    "normal_query": "normal_query",
    "analysis_query": "analysis_query",
})
graph.add_edge("normal_query", END)
graph.add_edge("analysis_query", "generate_table")
graph.add_edge("generate_table", END)

# Compile chatbot
chatbot = graph.compile()


# Start interactive loop
while True:
    query = input("> ")
    print("AI:", end=" ", flush=True)

    # Stream the model response
    event = chatbot.invoke({
        "message": query,
        "query_type": "",
        "normal_query": "",
        "analysis_query": "",
    })
    print(event)
