from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.csv import Csv, CsvCreate
from app.crud.csv import create_csv, create_csv_table, get_csvs
from app.utils.csv import parse_csv, create_columns
from app.core.dependencies import get_current_user
import json

router = APIRouter(
    prefix="/csv", tags=["Csv"])


@router.post("/", response_model=Csv)
async def add_csv(
        data: str = Form(...),
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)):
    """Create a new csv"""
    data_dict = json.loads(data)
    name = data_dict.get("name")
    description = data_dict.get("description")
    csv_data = await parse_csv(file)
    csv_columns, csv_columns_info = create_columns(csv_data)
    csv_create = CsvCreate(
        name=name,
        description=description,
        file_name=file.filename,
        user_id=user_id,
        columns=csv_columns_info)
    csv_details = create_csv(db, csv_create)
    create_csv_table(csv_details, csv_data, csv_columns)
    return csv_details


@router.get("/", response_model=list[Csv])
def read_connections(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve all connections"""
    return get_csvs(db, user_id)
