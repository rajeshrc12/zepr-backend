from pydantic import BaseModel, ConfigDict
from datetime import datetime


class DashboardBase(BaseModel):
    name: str
    description: str
    structure: list[dict]


class DashboardCreate(DashboardBase):
    user_id: str
    pass


class DashboardUpdate(DashboardBase):
    pass


class Dashboard(DashboardBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
