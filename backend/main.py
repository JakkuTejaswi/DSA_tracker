from fastapi import FastAPI
from routers.analytics import router as analytics_router
from database import engine
from routers import users
import models
from routers.problems import router as problem_router
from routers.users import router as user_router
from routers import ml
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="DSA Tracker API"
)

app.include_router(
    problem_router
)
app.include_router(
    analytics_router
)
app.include_router(users.router)

app.include_router(
    ml.router
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():

    return {
        "message": "DSA Tracker Running"
    }