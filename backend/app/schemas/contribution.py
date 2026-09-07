from typing import Optional

from pydantic import BaseModel, Field


class ContributionCreate(BaseModel):
    user_id: int

    type: str = Field(..., description="CODE, RESEARCH, or DOCUMENTATION")

    title: str
    description: Optional[str] = None

    repository_url: Optional[str] = None
    source_url: Optional[str] = None

    code_text: Optional[str] = None
    research_text: Optional[str] = None
    documentation_text: Optional[str] = None

    # Engineering quality signals
    complexity: float = 1.0
    test_coverage: float = 0.0
    documentation_quality: float = 0.0
    review_quality: float = 0.0

    # Research quality signals
    methodology_quality: float = 0.0
    technical_depth: float = 0.0
    clarity: float = 0.0
    novelty: float = 0.0

    # Common impact signal
    impact: float = 0.0
