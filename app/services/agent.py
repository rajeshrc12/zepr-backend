from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from app.utils.prompt import get_data_analyst_prompt
from langchain_core.messages import HumanMessage, SystemMessage
from app.services.openai import llm
import json
from app.core.database import SessionLocal
from app.schemas.message import MessageCreate
from app.models.message import Message
from app.services.python_sandbox import execute_code
from app.services.gcp import generate_signed_url
from pathlib import Path


class ChatState(TypedDict):
    chat_id: int
    user_query: str
    user_id: int
    csv_id: int
    csv_columns: list[str]
    csv_name: str
    response: dict
    output: list


class CodeGenerationSchema(BaseModel):
    type: str
    content: str


def code_generation(state: ChatState):
    system_prompt = get_data_analyst_prompt(
        state["csv_name"], state["csv_columns"])
    structured_llm = llm.bind_tools(
        [],
        response_format=CodeGenerationSchema,
        strict=True,
    )
    messages = [SystemMessage(content=system_prompt),
                HumanMessage(content=state["user_query"])]

    response = structured_llm.invoke(messages)
    try:
        response_json = json.loads(response.content)
    except:
        response_json = {"type": False, "content": False}

    print("code_generation", response.content)
    return {"response": response_json}


def code_execution(state: ChatState):
    if (state["response"]["type"] == "code"):
        code = state["response"]["content"]
        csv_url = generate_signed_url(state["user_id"], state["csv_id"])
        code_with_url = code.replace(state["csv_name"], csv_url)
        output = execute_code(code_with_url)
        print("output", output)
        return {"output": output}


def save_data(state: ChatState):
    print(state)
    db = SessionLocal()
    human_message = MessageCreate(
        content=state["user_query"],
        chat_id=state["chat_id"],
        type="human"
    )
    ai_message = MessageCreate(
        content=state["response"]["content"],
        chat_id=state["chat_id"],
        type="ai",
        summary=json.dumps(state["output"])
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
graph.add_node("code_generation", code_generation)
graph.add_node("code_execution", code_execution)
graph.add_node("save_data", save_data)

graph.add_edge(START, "code_generation")
graph.add_edge("code_generation", "code_execution")
graph.add_edge("code_execution", "save_data")
graph.add_edge("save_data", END)

# Compile chatbot
chatbot = graph.compile()
