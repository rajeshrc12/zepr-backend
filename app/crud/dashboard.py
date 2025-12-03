from sqlalchemy.orm import Session
from app.models.dashboard import Dashboard
from app.schemas.dashboard import DashboardUpdate, DashboardCreate
from sqlalchemy import desc


def get_dashboards(db: Session, user_id: int):
    return (
        db.query(Dashboard)
        .filter(Dashboard.user_id == user_id)
        .order_by(desc(Dashboard.created_at))
        .limit(10)
        .all()
    )


def get_dashboard(db: Session, dashboard_id: int):
    return db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()


def create_dashboard(db: Session, dashboard: DashboardCreate):
    db_dashboard = Dashboard(**dashboard.dict())
    db.add(db_dashboard)
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard


def update_dashboard(db: Session, dashboard_id: int, dashboard: DashboardUpdate):
    db_dashboard = get_dashboard(db, dashboard_id)
    if not db_dashboard:
        return None
    db_dashboard.name = dashboard.name
    db_dashboard.description = dashboard.type
    db_dashboard.structure = dashboard.user_id
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard


def delete_dashboard(db: Session, dashboard_id: int):
    db_dashboard = get_dashboard(db, dashboard_id)
    if not db_dashboard:
        return None
    db.delete(db_dashboard)
    db.commit()
    return db_dashboard
