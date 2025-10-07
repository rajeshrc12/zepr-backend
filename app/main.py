from fastapi import FastAPI
from app.core.database import init_db
from app.routers.task import router as task_router
from app.routers.auth import router as auth_router
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings

app = FastAPI(title="Task CRUD API")
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(task_router)
app.include_router(auth_router)
