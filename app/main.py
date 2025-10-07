from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.core.database import init_db, close_db
from app.routers.task import router as task_router
from app.routers.auth import router as auth_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    init_db()
    yield
    close_db()

app = FastAPI(title="Zepr", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

app.include_router(task_router)
app.include_router(auth_router)
