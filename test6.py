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
import psycopg2
from app.core.config import settings

# Load API key
load_dotenv()

# Define chat state


class ChatState(TypedDict):
    message: str
    query_type: str
    normal_query: str
    analysis_query: str
    table: dict
    chart: str
    summary: str


class QueryAnalyzerOutputSchema(BaseModel):
    type: str


class NormalQueryOutputSchema(BaseModel):
    answer: str


class ChartOutputSchema(BaseModel):
    type: str
    x_axis: str
    y_axis: str


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
    
    SQL Table Name: csv_68dec8555b894d5461518a71
    Schema:
    - UserID (TEXT)
    - ShowTitle (TEXT)
    - Genre (TEXT)
    - Language (TEXT)
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
    sql_llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        model="google/gemini-2.5-flash",
    )
    structured_llm = sql_llm.bind_tools(
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
    try:
        # Connect using connection string
        connection = psycopg2.connect(settings.DATABASE_CSV_URL)
        cursor = connection.cursor()

        # Your SQL query
        query = state["analysis_query"]
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Get column names
        columns = [desc[0] for desc in cursor.description]

        # Convert to array of objects
        results = [dict(zip(columns, row)) for row in rows]

        return {"table": results}

    except Exception as e:
        print("Error:", e)
        return {"table": []}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def generate_chart(state: ChatState):
    prompt = f"""
You are a Chart Config Generator. Your task is to analyze the given data and generate a suitable chart configuration object from the available chart types below.

Instructions:
1.If the user explicitly requests a chart type from the available options, always use that.
2.If the user does not specify a chart type, or requests a chart type not in the available options, select the most suitable chart based on the structure of the data.
3.Only generate chart types from the available options; do not create or suggest any others.

Available chart types:
1. Bar Chart
- x_axis: must be a categorical value
- y_axis: must be a numerical value
- Example output: {{"type":"bar","x_axis":"key","y_axis":"key"}}

2. Line Chart
- x_axis: must be a categorical value
- y_axis: must be a numerical value
- Example output: {{"type":"line","x_axis":"key","y_axis":"key"}}

3. Category Chart
- Use when all keys have categorical values
- You can choose key with repetitive values as x_axis
- Example output: {{"type":"category","x_axis":"key","y_axis":""}}
"""
    chart_llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        model="google/gemini-2.5-flash",
    )
    structured_llm = chart_llm.bind_tools(
        [],
        response_format=ChartOutputSchema,
        strict=True,
    )
    user_message = f"""                             
Data:
{json.dumps(state["table"], indent=5)}

User query:
{state["message"]}
"""
    messages = [SystemMessage(content=prompt),
                HumanMessage(content=user_message)]

    response = structured_llm.invoke(messages)
    response_json = json.loads(response.content)

    return {"chart": response_json}


def generate_summary(state: ChatState):
    prompt = f"""
You are given a user query and a dataset (array of objects).

Your task is to:
- Carefully analyze the dataset in the context of the user query.
- Generate a clear, concise, and insightful answer that directly addresses the query.
- Present the results in a well-structured summary using bullet points or other Markdown formatting where appropriate.
- Include contextual insights, comparisons, or trends to make the explanation more meaningful.
- Use proper Markdown formatting (headings, bold or numbering)
- Give response in short paragraph, dont give long answers.
"""

    user_message = f"""
user query:
{state["message"]}

data:
{json.dumps(state["table"], indent=5)}
"""
    messages = [SystemMessage(content=prompt),
                HumanMessage(content=user_message)]

    response = llm.invoke(messages)
    return {"summary": response.content}


# Build the graph
graph = StateGraph(ChatState)
graph.add_node("query_analyzer", query_analyzer)
graph.add_node("normal_query", normal_query)
graph.add_node("analysis_query", analysis_query)
graph.add_node("generate_table", generate_table)
graph.add_node("generate_chart", generate_chart)
graph.add_node("generate_summary", generate_summary)

graph.add_edge(START, "query_analyzer")
graph.add_conditional_edges("query_analyzer", query_decision, {
    "normal_query": "normal_query",
    "analysis_query": "analysis_query",
})
graph.add_edge("normal_query", END)
graph.add_edge("analysis_query", "generate_table")
graph.add_edge("generate_table", "generate_chart")
graph.add_edge("generate_chart", "generate_summary")
graph.add_edge("generate_summary", END)

# Compile chatbot
chatbot = graph.compile()


# Start interactive loop
while True:
    query = input("> ")

    try:
        # Stream the model response
        event = chatbot.invoke({
            "message": query,
            "query_type": "",
            "normal_query": "",
            "analysis_query": "",
            "table": [],
            "chart": {},
            "summary": "",
        })

        print(json.dumps(event, indent=5))
    except Exception as e:
        print(str(e))
