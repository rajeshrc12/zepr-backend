from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chart import Chart, ChartUpdate, ChartBase, ChartCreate
from app.schemas.message import MessageCreate
from app.crud.chart import create_chart, get_charts, get_chart, update_chart, delete_chart
from app.crud.message import create_message
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/chart", tags=["Chart"])


@router.post("/", response_model=Chart)
def add_chart(chart: ChartBase, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new chart"""
    chart_create = ChartCreate(
        **chart.model_dump(),
        user_id=user_id
    )
    return create_chart(db, chart_create)


@router.get("/", response_model=list[Chart])
def read_charts(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve all charts"""
    return get_charts(db, user_id)


@router.get("/{chart_id}", response_model=Chart)
def read_chart(chart_id: int, db: Session = Depends(get_db)):
    """Retrieve a single chart by ID"""
    db_chart = get_chart(db, chart_id)
    if not db_chart:
        raise HTTPException(status_code=404, detail="Chart not found")
    return db_chart


@router.put("/{chart_id}", response_model=Chart)
def modify_chart(chart_id: int, chart: ChartUpdate, db: Session = Depends(get_db)):
    """Update an existing chart"""
    db_chart = update_chart(db, chart_id, chart)
    if not db_chart:
        raise HTTPException(status_code=404, detail="Chart not found")
    return db_chart


@router.delete("/{chart_id}", response_model=Chart)
def remove_chart(chart_id: int, db: Session = Depends(get_db)):
    """Delete a chart by ID"""
    db_chart = delete_chart(db, chart_id)
    if not db_chart:
        raise HTTPException(status_code=404, detail="Chart not found")
    return db_chart
