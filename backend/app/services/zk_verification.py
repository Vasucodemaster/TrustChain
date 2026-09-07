import json
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
BLOCKCHAIN_DIR = PROJECT_ROOT / "blockchain"
VERIFIER_SCRIPT = BLOCKCHAIN_DIR / "verify_proof.js"


def verify_zk_proof() -> dict:
    result = subprocess.run(
        ["node", str(VERIFIER_SCRIPT)],
        cwd=str(BLOCKCHAIN_DIR),
        capture_output=True,
        text=True,
        check=True,
    )

    output = result.stdout.strip()

    return json.loads(output)
