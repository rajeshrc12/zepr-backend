from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.connection import Connection, ConnectionCreate, ConnectionUpdate
from app.crud.connection import create_connection, get_connections, get_connection, update_connection, delete_connection

router = APIRouter(prefix="/connection", tags=["Connection"])


@router.post("/", response_model=Connection)
def add_connection(connection: ConnectionCreate, db: Session = Depends(get_db)):
    """Create a new connection"""
    return create_connection(db, connection)


@router.get("/", response_model=list[Connection])
def read_connections(db: Session = Depends(get_db)):
    """Retrieve all connections"""
    return get_connections(db)


@router.get("/{connection_id}", response_model=Connection)
def read_connection(connection_id: int, db: Session = Depends(get_db)):
    """Retrieve a single connection by ID"""
    db_connection = get_connection(db, connection_id)
    if not db_connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    return db_connection


@router.put("/{connection_id}", response_model=Connection)
def modify_connection(connection_id: int, connection: ConnectionUpdate, db: Session = Depends(get_db)):
    """Update an existing connection"""
    db_connection = update_connection(db, connection_id, connection)
    if not db_connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    return db_connection


@router.delete("/{connection_id}", response_model=Connection)
def remove_connection(connection_id: int, db: Session = Depends(get_db)):
    """Delete a connection by ID"""
    db_connection = delete_connection(db, connection_id)
    if not db_connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    return db_connection
