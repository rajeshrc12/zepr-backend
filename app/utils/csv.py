from sqlalchemy import Integer, String, Float, Column, DateTime
from dateutil.parser import parse
from fastapi import File
import csv
from io import StringIO


def detect_type(value):
    if value is None or value == "":
        return String
    try:
        int(value)
        return Integer
    except ValueError:
        pass
    try:
        float(value)
        return Float
    except ValueError:
        pass
    try:
        parse(value)
        return DateTime
    except (ValueError, OverflowError):
        pass
    return String


async def parse_csv(file: File):
    try:
        contents = await file.read()
        decoded = contents.decode("utf-8")
        reader = csv.DictReader(StringIO(decoded))
        data = [row for row in reader]
        return data
    except:
        return []


def create_columns(data: list[dict], sample_size=10):
    """
    Create SQLAlchemy columns and an array of {name, type} objects from CSV data.
    Only inspects the first `sample_size` rows for type detection.
    """
    columns = []
    columns_info = []  # Array of {name, type}

    if not data:
        return columns, columns_info

    # Only consider first `sample_size` rows
    sample_rows = data[:sample_size]

    for key in data[0].keys():
        # Take the first non-empty value in the sample rows
        sample_value = next(
            (row[key] for row in sample_rows if row[key] not in [None, ""]),
            ""
        )
        col_type = detect_type(sample_value)
        columns.append(Column(key, col_type))
        columns_info.append(
            {"name": key, "type": col_type.__name__})  # type as string

    return columns, columns_info
