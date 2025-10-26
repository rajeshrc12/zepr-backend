from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.csv import Csv, CsvCreate
from app.crud.csv import create_csv, create_csv_table
from app.utils.csv import parse_csv, create_columns


router = APIRouter(prefix="/csv", tags=["Csv"])


@router.post("/", response_model=Csv)
async def add_csv(
        name: str = Form(...),
        description: str = Form(...),
        user_id: int = Form(...),
        file: UploadFile = File(...),
        db: Session = Depends(get_db)):
    """Create a new csv"""
    # Populate CsvCreate schema
    csv_data = await parse_csv(file)
    csv_columns, csv_columns_info = create_columns(csv_data)
    csv_create = CsvCreate(
        name=name,
        description=description,
        file_name=file.filename,
        user_id=user_id,
        columns=csv_columns_info)
    csv_details = create_csv(db, csv_create)
    result = create_csv_table(csv_details, csv_data, csv_columns)
    return csv_details
