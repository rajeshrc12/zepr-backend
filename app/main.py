from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db, close_db
from app.routers.task import router as task_router
from app.routers.auth import router as auth_router
from app.routers.user import router as user_router
from app.routers.message import router as message_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    init_db()
    yield
    close_db()

app = FastAPI(title="Zepr", lifespan=lifespan)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        # Clear token cookie when user is unauthorized
        response = JSONResponse(
            status_code=401,
            content={"detail": exc.detail}
        )
        response.delete_cookie("token", path="/")
        return response
    # For other HTTP exceptions
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# Session middleware
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

# CORS middleware
origins = [
    settings.FRONTEND_URL     # production frontend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,   # important to send cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(task_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(message_router)
