from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.connection import Base


class Reputation(Base):
    __tablename__ = "reputation"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    reputation_score = Column(
        Float,
        default=0.0
    )

    previous_score = Column(
        Float,
        default=0.0
    )

    reason = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
