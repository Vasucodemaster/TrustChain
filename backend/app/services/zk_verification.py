import json
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
BLOCKCHAIN_DIR = PROJECT_ROOT / "blockchain"
VERIFIER_SCRIPT = BLOCKCHAIN_DIR / "verify_proof.js"


def verify_zk_proof(credential_score: int, minimum_score: int) -> dict:
    result = subprocess.run(
        [
            "node",
            str(VERIFIER_SCRIPT),
            str(credential_score),
            str(minimum_score),
        ],
        cwd=str(BLOCKCHAIN_DIR),
        capture_output=True,
        text=True,
        check=True,
    )

    output = json.loads(result.stdout.strip())

    proof_valid = output.get("verified", False)
    public_signals = output.get("publicSignals", [])

    eligible = (
        proof_valid
        and len(public_signals) > 0
        and str(public_signals[0]) == "1"
    )

    return {
        "proof_valid": proof_valid,
        "eligible": eligible,
        "public_signals": public_signals,
    }
