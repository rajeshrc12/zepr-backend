from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.task import Base
from app.core.database import engine, get_db
from app.crud.task import create_task, get_tasks, get_task, update_task, delete_task
from app.schemas.task import Task, TaskUpdate, TaskCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task CRUD App")


@app.post("/tasks/", response_model=Task)
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)


@app.get("/tasks/", response_model=list[Task])
def read_tasks(db: Session = Depends(get_db)):
    return get_tasks(db)


@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.put("/tasks/{task_id}", response_model=Task)
def modify_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = update_task(db, task_id, task)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.delete("/tasks/{task_id}", response_model=Task)
def remove_task(task_id: int, db: Session = Depends(get_db)):
    db_task = delete_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
