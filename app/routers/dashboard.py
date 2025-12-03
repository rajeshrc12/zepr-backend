from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.dashboard import Dashboard, DashboardUpdate, DashboardBase, DashboardCreate
from app.crud.dashboard import create_dashboard, get_dashboards, get_dashboard, update_dashboard, delete_dashboard
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.post("/", response_model=Dashboard)
def add_dashboard(dashboard: DashboardBase, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new dashboard"""
    dashboard_create = DashboardCreate(
        name=dashboard.name,
        description=dashboard.description,
        structure=dashboard.structure,
        user_id=user_id
    )
    return create_dashboard(db, dashboard_create)


@router.get("/", response_model=list[Dashboard])
def read_dashboards(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve all dashboards"""
    return get_dashboards(db, user_id)


@router.get("/{dashboard_id}", response_model=Dashboard)
def read_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    """Retrieve a single dashboard by ID"""
    db_dashboard = get_dashboard(db, dashboard_id)
    if not db_dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return db_dashboard


@router.put("/{dashboard_id}", response_model=Dashboard)
def modify_dashboard(dashboard_id: int, dashboard: DashboardUpdate, db: Session = Depends(get_db)):
    """Update an existing dashboard"""
    db_dashboard = update_dashboard(db, dashboard_id, dashboard)
    if not db_dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return db_dashboard


@router.delete("/{dashboard_id}", response_model=Dashboard)
def remove_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    """Delete a dashboard by ID"""
    db_dashboard = delete_dashboard(db, dashboard_id)
    if not db_dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return db_dashboard
