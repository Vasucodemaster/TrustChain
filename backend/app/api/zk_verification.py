from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import subprocess

from app.services.zk_verification import verify_zk_proof

router = APIRouter(
    prefix="/zk",
    tags=["Zero-Knowledge Verification"]
)


class ZKVerificationRequest(BaseModel):
    credential_score: int = Field(ge=0, le=255)
    minimum_score: int = Field(ge=0, le=255)


@router.post("/verify")
def verify_credential(request: ZKVerificationRequest):
    try:
        zk_result = verify_zk_proof(
            request.credential_score,
            request.minimum_score
        )

        return {
            "proof_valid": zk_result["proof_valid"],
            "eligible": zk_result["eligible"],
            "credential_score": request.credential_score,
            "minimum_score": request.minimum_score,
            "public_signals": zk_result["public_signals"],
            "verification_method": "Groth16 ZK Proof"
        }

    except (subprocess.CalledProcessError, ValueError, KeyError) as exc:
        raise HTTPException(
            status_code=500,
            detail="Zero-knowledge proof verification failed."
        ) from exc
