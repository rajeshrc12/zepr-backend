from fastapi import FastAPI
from app.models.task import Base
from app.core.database import engine
from app.routers.task import router as task_router
from app.routers.user import router as user_router

# Create all tables at startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Zepr")

# Register routers
app.include_router(task_router)
app.include_router(user_router)
