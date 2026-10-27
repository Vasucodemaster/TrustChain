from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import Base, engine

from app.models import (
    User,
    Contribution,
    Reputation,
    ContributionScore
)

from app.api.users import router as users_router
from app.api.contributions import router as contributions_router
from app.api.reputation import router as reputation_router
from app.api.graph import router as graph_router

from app.api.contribution import router as contribution_router
from app.api.github import router as github_router
from app.api.research import router as research_router
from app.api.documentation import router as documentation_router
from app.api.temporal_anomaly import router as temporal_anomaly_router
from app.api.zk_verification import router as zk_verification_router
from app.api.sybil_detection import router as sybil_detection_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TrustChain API",
    description="AI-Powered Contribution Intelligence & Reputation Network",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(contributions_router)
app.include_router(reputation_router)
app.include_router(graph_router)
app.include_router(contribution_router)
app.include_router(github_router)
app.include_router(research_router)
app.include_router(documentation_router)
app.include_router(temporal_anomaly_router)
app.include_router(zk_verification_router)
app.include_router(sybil_detection_router)

@app.get("/")
def root():
    return {
        "project": "TrustChain",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
