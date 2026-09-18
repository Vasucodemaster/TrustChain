from fastapi import APIRouter, HTTPException

from app.services.reputation_blockchain import (
    get_reputation as get_blockchain_reputation
)


router = APIRouter(
    prefix="/reputation",
    tags=["Reputation"]
)


@router.get("/")
def get_reputation():
    return {
        "message": "Reputation endpoint is working"
    }


@router.get("/blockchain/{contributor_id}")
def get_blockchain_reputation_endpoint(contributor_id: int):

    try:
        return get_blockchain_reputation(contributor_id)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
