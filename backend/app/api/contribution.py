from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.contribution import Contribution
from app.models.contribution_score import ContributionScore
from app.schemas.contribution import ContributionCreate

from ml.contribution_quality.service import F4Service


router = APIRouter(
    prefix="/contributions",
    tags=["Contributions"]
)


f4_service = F4Service()


@router.post("/")
def create_contribution(
    contribution_data: ContributionCreate,
    db: Session = Depends(get_db)
):
    contribution = Contribution(
        user_id=contribution_data.user_id,
        type=contribution_data.type,
        title=contribution_data.title,
        description=contribution_data.description,
        repository_url=contribution_data.repository_url,
        source_url=contribution_data.source_url,

        code_text=contribution_data.code_text,
        research_text=contribution_data.research_text,
        documentation_text=contribution_data.documentation_text,

        complexity=contribution_data.complexity,
        test_coverage=contribution_data.test_coverage,
        documentation_quality=contribution_data.documentation_quality,
        review_quality=contribution_data.review_quality,

        methodology_quality=contribution_data.methodology_quality,
        technical_depth=contribution_data.technical_depth,
        clarity=contribution_data.clarity,
        novelty=contribution_data.novelty,

        impact=contribution_data.impact
    )

    db.add(contribution)
    db.commit()
    db.refresh(contribution)

    scoring_data = {
        "type": contribution.type,
        "title": contribution.title,
        "description": contribution.description or "",

        "code_text": contribution.code_text or "",
        "research_text": contribution.research_text or "",

        "complexity": contribution.complexity or 0,
        "test_coverage": contribution.test_coverage or 0,
        "documentation_quality": contribution.documentation_quality or 0,
        "review_quality": contribution.review_quality or 0,

        "methodology_quality": contribution.methodology_quality or 0,
        "technical_depth": contribution.technical_depth or 0,
        "clarity": contribution.clarity or 0,
        "novelty": contribution.novelty or 0,
        "documentation_text": contribution.documentation_text,
        "impact": contribution.impact or 0
    }

    try:
        score_result = f4_service.score_contribution(scoring_data)

    except ValueError as error:
        db.delete(contribution)
        db.commit()

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    contribution_score = ContributionScore(
        contribution_id=contribution.id,
        code_quality=score_result["code_quality"],
        research_quality=score_result["research_quality"],
        impact_score=score_result["impact_score"],
        quality_score=score_result["quality_score"],
        model_version=score_result["model_version"]
    )

    db.add(contribution_score)
    db.commit()
    db.refresh(contribution_score)

    return {
        "contribution_id": contribution.id,
        "type": contribution.type,
        "title": contribution.title,
        "quality_score": contribution_score.quality_score,
        "code_quality": contribution_score.code_quality,
        "research_quality": contribution_score.research_quality,
        "impact_score": contribution_score.impact_score,
        "model_version": contribution_score.model_version
    }


@router.get("/{contribution_id}")
def get_contribution(
    contribution_id: int,
    db: Session = Depends(get_db)
):
    contribution = (
        db.query(Contribution)
        .filter(Contribution.id == contribution_id)
        .first()
    )

    if not contribution:
        raise HTTPException(
            status_code=404,
            detail="Contribution not found"
        )

    score = (
        db.query(ContributionScore)
        .filter(
            ContributionScore.contribution_id == contribution.id
        )
        .order_by(ContributionScore.id.desc())
        .first()
    )

    return {
        "contribution_id": contribution.id,
        "user_id": contribution.user_id,
        "type": contribution.type,
        "title": contribution.title,
        "description": contribution.description,
        "repository_url": contribution.repository_url,
        "source_url": contribution.source_url,
        "quality_score": score.quality_score if score else None,
        "code_quality": score.code_quality if score else None,
        "research_quality": score.research_quality if score else None,
        "model_version": score.model_version if score else None
    }
