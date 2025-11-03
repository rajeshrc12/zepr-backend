from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ChartBase(BaseModel):
    name: str
    sql: str
    table: list[dict]
    config: dict
    summary: str


class ChartCreate(ChartBase):
    user_id: int
    pass


class ChartUpdate(ChartBase):
    pass


class Chart(ChartBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
