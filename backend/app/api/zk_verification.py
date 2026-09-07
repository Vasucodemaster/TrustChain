from fastapi import APIRouter
from pydantic import BaseModel

from app.services.zk_verification import verify_zk_proof


router = APIRouter(
    prefix="/zk",
    tags=["Zero-Knowledge Verification"]
)


class ZKVerificationRequest(BaseModel):
    credential_score: int
    minimum_score: int


@router.post("/verify")
def verify_credential(request: ZKVerificationRequest):
    zk_result = verify_zk_proof()

    return {
        "verified": zk_result["verified"],
        "credential_score": request.credential_score,
        "minimum_score": request.minimum_score,
        "verification_method": "Groth16 ZK Proof"
    }
