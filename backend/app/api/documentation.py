from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional


router = APIRouter(
    prefix="/documentation",
    tags=["Documentation"]
)


class DocumentationSubmission(BaseModel):
    title: str
    description: Optional[str] = None
    source_url: Optional[str] = None
    documentation_text: str


@router.post("/submit")
def submit_documentation(data: DocumentationSubmission):

    return {
        "source": "Documentation",
        "title": data.title,
        "source_url": data.source_url,
        "status": "received",
        "message": "Documentation contribution received"
    }
