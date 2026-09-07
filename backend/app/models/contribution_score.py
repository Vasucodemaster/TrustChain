from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.connection import Base


class ContributionScore(Base):
    __tablename__ = "contribution_scores"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    contribution_id = Column(
        Integer,
        ForeignKey("contributions.id"),
        nullable=False
    )

    code_quality = Column(
        Float,
        default=0.0
    )

    research_quality = Column(
        Float,
        default=0.0
    )

    impact_score = Column(
        Float,
        default=0.0
    )

    quality_score = Column(
        Float,
        default=0.0
    )

    model_version = Column(
        String(50),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
