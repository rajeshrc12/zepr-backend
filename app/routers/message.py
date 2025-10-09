from fastapi import APIRouter
from app.core.prompts import data_analyst
router = APIRouter(prefix="/message")


@router.post("/")
def create_new_message(message: str):
    print(message, data_analyst("", "", "", ""))
    return message
