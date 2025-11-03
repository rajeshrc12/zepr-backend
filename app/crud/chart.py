from sqlalchemy.orm import Session
from app.models.chart import Chart
from app.schemas.chart import ChartUpdate, ChartCreate
from sqlalchemy import desc


def get_charts(db: Session, user_id: int):
    return (
        db.query(Chart)
        .filter(Chart.user_id == user_id)
        .order_by(desc(Chart.created_at))
        .limit(10)
        .all()
    )


def get_chart(db: Session, chart_id: int):
    return db.query(Chart).filter(Chart.id == chart_id).first()


def create_chart(db: Session, chart: ChartCreate):
    db_chart = Chart(**chart.model_dump())
    db.add(db_chart)
    db.commit()
    db.refresh(db_chart)
    return db_chart


def update_chart(db: Session, chart_id: int, chart: ChartUpdate):
    db_chart = get_chart(db, chart_id)
    if not db_chart:
        return None
    db_chart.name = chart.name
    db_chart.sql = chart.sql
    db_chart.table = chart.table
    db_chart.config = chart.config
    db_chart.summary = chart.summary
    db.commit()
    db.refresh(db_chart)
    return db_chart


def delete_chart(db: Session, chart_id: int):
    db_chart = get_chart(db, chart_id)
    if not db_chart:
        return None
    db.delete(db_chart)
    db.commit()
    return db_chart
