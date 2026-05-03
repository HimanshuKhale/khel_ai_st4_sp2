from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.student4 import router as student4_router


app = FastAPI(
    title="Student 4 Sprint 2 Fielding Analytics API",
    description=(
        "Production-ready fielding analytics API with Expected Runs Saved, "
        "Catch Probability Model, Reaction Time Proxy, and Full Fielding Analysis."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Student 4 Sprint 2 Fielding Analytics API is running.",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "student4-fielding-analytics-api",
        "version": "1.0.0",
    }


app.include_router(student4_router)