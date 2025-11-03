from fastapi import FastAPI, HTTPException, Request
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.connection import router as connection_router
from app.routers.chat import router as chat_router
from app.routers.chart import router as chart_router
from app.routers.csv import router as csv_router
from app.routers.message import router as message_router
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(title="Zepr")


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
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(connection_router)
app.include_router(csv_router)
app.include_router(chat_router)
app.include_router(chart_router)
app.include_router(message_router)
