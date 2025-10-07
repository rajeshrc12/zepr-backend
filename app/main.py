from fastapi import FastAPI
from app.core.database import init_db
from app.routers.task import router as task_router

app = FastAPI(title="Task CRUD API")


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(task_router)
