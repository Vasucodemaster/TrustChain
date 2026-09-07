from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional


router = APIRouter(
    prefix="/research",
    tags=["Research"]
)


class ResearchSubmission(BaseModel):
    title: str
    description: Optional[str] = None
    source_url: Optional[str] = None
    research_text: str


@router.post("/submit")
def submit_research(data: ResearchSubmission):

    return {
        "source": "Research",
        "title": data.title,
        "source_url": data.source_url,
        "status": "received",
        "message": "Research contribution ready for F4 SciBERT analysis"
    }
