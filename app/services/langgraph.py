from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel
import json
from app.core.database import SessionCSV, SessionLocal
from app.services.openai import llm
from app.schemas.csv import Csv
from sqlalchemy import text
from app.schemas.message import MessageCreate
from app.models.message import Message

# Define chat state


class ChatState(TypedDict):
    chat_id: str
    message: str
    csv: Csv
    query: str
    content: str
    sql: str
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


# Define the chat node logic


def query_analyzer(state: ChatState):
    try:

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

        Your output must be a one of below JSON object with no code block, no extra text, and no markdown like below:
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
        return {"query": response_json["type"]}

    except Exception as e:
        print("query_analyzer", str(e))
        return {"query": ""}


def query_decision(state: ChatState):
    if (state["query"] == "normal"):
        return "normal_query"
    if (state["query"] == "analysis"):
        return "analysis_query"


def normal_query(state: ChatState):
    table_name = state["csv"]["name"]
    table_description = state["csv"]["description"]
    columns = state["csv"]["columns"]

    schema_text = "\n".join(
        [f"- {col['name']} ({col['type']})" for col in columns])

    prompt = f"""
    You are an AI Data Analyst.

    You have access to the following dataset:

    Table Name: {table_name}
    Table description: {table_description}
    Schema:
    {schema_text}

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
    return {"content": response_json["answer"]}


def analysis_query(state: ChatState):
    table_name = "csv_"+str(state["csv"]["id"])
    columns = state["csv"]["columns"]
    schema_text = "\n".join(
        [f"- {col['name']} ({col['type']})" for col in columns])
    prompt = f"""
    You are an SQL Query Generator. Your task is to generate SQL queries based on the user's request.
    
    SQL Table Name: {table_name}
    Schema:
    {schema_text}

    Instruction:
    - Generate only one SQL query.
    - Ignore any mentions of chart types, visualizations, or other non-SQL instructions. Focus only on generating correct SQL queries.
    - Use double quotes for table and column names exactly as in the schema.
    - Match data types correctly in WHERE clauses; handle nullable columns.
    - Never reference columns not in the schema.
    - Typecast columns appropriately based on the data types defined in the schema when performing operations or comparisons.
    - Never reference columns not in the schema.
    - Always return Top 5 results using ORDER BY + LIMIT 5.
    - Arrange columns: first = categorical, last = numerical, others in between.
    - Do not include explanations, comments, or any extra text in SQL output.
    - The query must be PostgreSQL compatible (avoid SQLite or MySQL-specific functions).
    - Output must be sql query.

    Output Format:
    Return your response as a JSON object with an "answer" key containing sql.

    Example output
    {{
        "answer":"SELECT "Country", COUNT(*) AS customer_count FROM "csv_cmewh96du000dt9xothtzer2u" GROUP BY "Country" ORDER BY customer_count DESC LIMIT 5;"
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
    print(response_json["answer"])
    return {"sql": response_json["answer"]}


def generate_table(state: dict):
    """Execute raw SQL query using engine_csv session"""
    db_csv = SessionCSV()
    try:
        query = state["sql"]

        try:
            result = db_csv.execute(text(query))
        except Exception:
            # Retry once if connection invalidated
            db_csv.rollback()
            db_csv.close()
            db_csv = SessionCSV()
            result = db_csv.execute(text(query))

        columns = result.keys()
        rows = result.fetchall()
        return {"table": [dict(zip(columns, row)) for row in rows]}

    except Exception as e:
        print(f"❌ Error while executing query: {e}")
        return {"table": []}

    finally:
        db_csv.close()


def generate_chart(state: ChatState):
    prompt = f"""
You are a Chart Config Generator. Your task is to analyze the given data and generate a suitable chart configuration object from the available chart types below.

Instructions:
1.If the user explicitly requests a chart type from the available options, always use that.
2.If the user does not specify a chart type, or requests a chart type not in the available options, select the most suitable chart based on the structure of the data.
3.Only generate chart types from the available options; do not create or suggest any others.

Available chart types:
1.Bar Chart
- x_axis: must be a categorical value
- y_axis: must be a numerical value
- Example output: {{"type":"bar","x_axis":"key","y_axis":"key"}}

2.Line Chart
- x_axis: must be a categorical value
- y_axis: must be a numerical value
- Example output: {{"type":"line","x_axis":"key","y_axis":"key"}}

2.Pie Chart
- x_axis: must be a categorical value
- y_axis: must be a numerical value
- Example output: {{"type":"pie","x_axis":"key","y_axis":"key"}}

"""
    structured_llm = llm.bind_tools(
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


def save_data(state: ChatState):
    print(state)
    db = SessionLocal()
    human_message = MessageCreate(
        content=state["message"],
        chat_id=state["chat_id"],
        type="human"
    )
    ai_message = MessageCreate(
        content=state["content"],
        chat_id=state["chat_id"],
        sql=state["sql"],
        table=state["table"],
        chart=state["chart"],
        summary=state["summary"],
        type="ai"
    )
    try:
        # Convert both Pydantic models to dicts
        human_data = human_message.model_dump(exclude_unset=True)
        ai_data = ai_message.model_dump(exclude_unset=True)

        # Create SQLAlchemy ORM objects
        db_human = Message(**human_data)
        db_ai = Message(**ai_data)

        # Add both to session
        db.add_all([db_human, db_ai])
        db.commit()

        # Refresh to get DB-generated fields (like id, created_at)
        db.refresh(db_human)
        db.refresh(db_ai)

        return {}

    except Exception as e:
        db.rollback()
        print(str(e))

    finally:
        db.close()


# Build the graph
graph = StateGraph(ChatState)
graph.add_node("query_analyzer", query_analyzer)
graph.add_node("normal_query", normal_query)
graph.add_node("analysis_query", analysis_query)
graph.add_node("generate_table", generate_table)
graph.add_node("generate_chart", generate_chart)
graph.add_node("generate_summary", generate_summary)
graph.add_node("save_data", save_data)

graph.add_edge(START, "query_analyzer")
graph.add_conditional_edges("query_analyzer", query_decision, {
    "normal_query": "normal_query",
    "analysis_query": "analysis_query",
})
graph.add_edge("normal_query", "save_data")
graph.add_edge("save_data", END)


graph.add_edge("analysis_query", "generate_table")
graph.add_edge("generate_table", "generate_chart")
graph.add_edge("generate_chart", "generate_summary")
graph.add_edge("generate_summary", "save_data")
graph.add_edge("save_data", END)

# Compile chatbot
chatbot = graph.compile()
