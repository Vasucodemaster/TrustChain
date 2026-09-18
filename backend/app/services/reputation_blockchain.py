import json
import os
from pathlib import Path

from web3 import Web3


# Local Hardhat blockchain
RPC_URL = "http://127.0.0.1:8545"

# F6 deployed contract
CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"



# Load the Solidity ABI
ABI_PATH = (
    Path(__file__).resolve().parents[2]
    / "blockchain"
    / "artifacts"
    / "contracts"
    / "ReputationSBT.sol"
    / "ReputationSBT.json"
)

# The actual project structure has blockchain beside backend,
# so use the absolute TrustChain path if necessary.
if not ABI_PATH.exists():
    ABI_PATH = (
        Path(__file__).resolve().parents[3]
        / "blockchain"
        / "artifacts"
        / "contracts"
        / "ReputationSBT.sol"
        / "ReputationSBT.json"
    )


def get_web3():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))

    if not w3.is_connected():
        raise RuntimeError(
            "Cannot connect to Hardhat blockchain at "
            f"{RPC_URL}"
        )

    return w3


def get_contract():
    w3 = get_web3()

    with open(ABI_PATH, "r") as f:
        artifact = json.load(f)

    contract = w3.eth.contract(
        address=Web3.to_checksum_address(CONTRACT_ADDRESS),
        abi=artifact["abi"]
    )

    return w3, contract


def get_reputation(contributor_id: int):
    w3, contract = get_contract()

    score, updated_at, owner = contract.functions.getReputation(
        contributor_id
    ).call()

    return {
        "contributor_id": contributor_id,
        "score": score,
        "updated_at": updated_at,
        "owner": owner
    }
