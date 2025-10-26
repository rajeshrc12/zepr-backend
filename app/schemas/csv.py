from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Dict, Optional


class CsvBase(BaseModel):
    name: str
    file_name: str
    description: str
    columns: Optional[List[Dict[str, str]]] = None
    user_id: int


class CsvCreate(CsvBase):
    pass


class CsvUpdate(CsvBase):
    pass


class Csv(CsvBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
