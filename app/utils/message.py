from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from app.schemas.message import MessageCreate


def serialize_messages(chat_id: str, messages: list[BaseMessage]) -> list[MessageCreate]:
    """
    Convert LangChain message objects (SystemMessage, HumanMessage, AIMessage)
    into a list of dicts for easy JSON/database storage.
    """
    result = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            msg_type = "human"
        elif isinstance(msg, AIMessage):
            msg_type = "ai"
        elif isinstance(msg, SystemMessage):
            msg_type = "system"
        else:
            msg_type = "unknown"

        result.append({
            "type": msg_type,
            "content": msg.content,
            "chat_id": chat_id
        })
    return result


def deserialize_messages(data: list[dict]) -> list[BaseMessage]:
    """
    Convert a list of dicts (with 'type' and 'content') back into
    LangChain message objects.
    """
    messages = []
    for item in data:
        msg_type = item.get("type")
        content = item.get("content", "")

        if msg_type == "human":
            messages.append(HumanMessage(content=content))
        elif msg_type == "ai":
            messages.append(AIMessage(content=content))
        elif msg_type == "system":
            messages.append(SystemMessage(content=content))
        else:
            raise ValueError(f"Unknown message type: {msg_type}")
    return messages
