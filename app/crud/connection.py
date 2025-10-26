from sqlalchemy.orm import Session
from app.models.connection import Connection
from app.schemas.connection import ConnectionUpdate, ConnectionCreate


def get_connections(db: Session):
    return db.query(Connection).all()


def get_connection(db: Session, connection_id: int):
    return db.query(Connection).filter(Connection.id == connection_id).first()


def create_connection(db: Session, connection: ConnectionCreate):
    db_connection = Connection(**connection.dict())
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection


def update_connection(db: Session, connection_id: int, connection: ConnectionUpdate):
    db_connection = get_connection(db, connection_id)
    if not db_connection:
        return None
    db_connection.name = connection.name
    db_connection.type = connection.type
    db_connection.user_id = connection.user_id
    db.commit()
    db.refresh(db_connection)
    return db_connection


def delete_connection(db: Session, connection_id: int):
    db_connection = get_connection(db, connection_id)
    if not db_connection:
        return None
    db.delete(db_connection)
    db.commit()
    return db_connection
