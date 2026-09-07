from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.sql import func

from app.database.connection import Base


class Contribution(Base):
    __tablename__ = "contributions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    type = Column(String(50), nullable=False)

    title = Column(String(200), nullable=False)

    description = Column(Text, nullable=True)

    repository_url = Column(String(500), nullable=True)

    source_url = Column(String(500), nullable=True)

    # Actual contribution content
    code_text = Column(Text, nullable=True)

    research_text = Column(Text, nullable=True)

    documentation_text = Column(Text, nullable=True)

    # Engineering signals
    complexity = Column(Float, nullable=True)

    test_coverage = Column(Float, nullable=True)

    documentation_quality = Column(Float, nullable=True)

    review_quality = Column(Float, nullable=True)

    # Research signals
    methodology_quality = Column(Float, nullable=True)

    technical_depth = Column(Float, nullable=True)

    clarity = Column(Float, nullable=True)

    novelty = Column(Float, nullable=True)

    # Common signal
    impact = Column(Float, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
