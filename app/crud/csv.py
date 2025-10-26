from sqlalchemy.orm import Session
from sqlalchemy import Table, Integer, Float, Boolean, DateTime, MetaData
from app.models.csv import Csv
from app.schemas.csv import CsvUpdate, CsvCreate
from app.core.database import engine_csv
from dateutil.parser import parse


def get_csvs(db: Session):
    return db.query(Csv).all()


def get_csv(db: Session, csv_id: int):
    return db.query(Csv).filter(Csv.id == csv_id).first()


def create_csv(db: Session, csv: CsvCreate):
    db_csv = Csv(**csv.dict())
    db.add(db_csv)
    db.commit()
    db.refresh(db_csv)
    return db_csv


def create_csv_table(details: Csv, data: dict, columns: dict):
    try:
        metadata = MetaData()
        csv_table = Table(
            f"csv_{details.id}",
            metadata,
            *columns
        )
        metadata.create_all(engine_csv)
        with Session(engine_csv) as session:
            insert_data = []
            for row in data:
                row_data = {}
                for col in columns:
                    value = row.get(col.name)
                    if value is None or value == "":
                        row_data[col.name] = None
                    else:
                        # Use the SQLAlchemy type to cast
                        col_type = type(col.type)
                        if col_type == Integer:
                            row_data[col.name] = int(value)
                        elif col_type == Float:
                            row_data[col.name] = float(value)
                        elif col_type == DateTime:
                            row_data[col.name] = parse(value)
                        else:  # String or unknown
                            row_data[col.name] = value
                insert_data.append(row_data)
            session.execute(csv_table.insert(), insert_data)
            session.commit()

        return csv_table
    except Exception as e:
        print(str(e))
        return False


def update_csv(db: Session, csv_id: int, csv: CsvUpdate):
    db_csv = get_csv(db, csv_id)
    if not db_csv:
        return None
    db_csv.name = csv.name
    db_csv.file_name = csv.file_name
    db_csv.description = csv.description
    db_csv.user_id = csv.user_id
    db_csv.columns = csv.columns
    db.commit()
    db.refresh(db_csv)
    return db_csv


def delete_csv(db: Session, csv_id: int):
    db_csv = get_csv(db, csv_id)
    if not db_csv:
        return None
    db.delete(db_csv)
    db.commit()
    return db_csv
