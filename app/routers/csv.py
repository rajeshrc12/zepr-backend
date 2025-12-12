from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.csv import Csv, CsvCreate
from app.crud.csv import create_csv, get_csvs
from app.core.dependencies import get_current_user
from app.services.gcp import upload_csv
import pandas as pd

router = APIRouter(
    prefix="/csv", tags=["Csv"])


@router.post("/")
def add_csv(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)):
    """Create a new csv"""
    # Read CSV into pandas
    df = pd.read_csv(file.file)

    # Extract columns in array/list format
    column_list = df.columns.tolist()

    # Reset file pointer so upload function can read it again
    file.file.seek(0)
    print(column_list)
    csv_create = CsvCreate(
        name=file.filename,
        description=file.filename,
        file_name=file.filename,
        columns=column_list,   # ← assign list of column names
        user_id=user_id
    )
    csv_details = create_csv(db, csv_create)
    dest_name = f"csv_uploads/{user_id}/{csv_details.id}.csv"

    # Step 3 — Upload CSV to GCS
    upload_result = upload_csv(file, dest_name)
    return {
        "csv": csv_details,
        "upload": upload_result,
    }


@router.get("/", response_model=list[Csv])
def read_connections(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve all connections"""
    return get_csvs(db, user_id)
