// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract ReputationSBT {

    struct Reputation {
        uint256 score;
        uint256 updatedAt;
        bool exists;
    }

    // Contributor ID => reputation
    mapping(uint256 => Reputation) private reputations;

    // Contributor ID => wallet address
    mapping(uint256 => address) private owners;

    address public admin;

    event ReputationMinted(
        uint256 indexed contributorId,
        address indexed owner,
        uint256 score
    );

    event ReputationUpdated(
        uint256 indexed contributorId,
        uint256 oldScore,
        uint256 newScore
    );

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    function mintReputation(
        uint256 contributorId,
        address owner,
        uint256 score
    ) external onlyAdmin {

        require(!reputations[contributorId].exists, "Reputation already exists");
        require(owner != address(0), "Invalid owner");
        require(score <= 100, "Score must be 0-100");

        owners[contributorId] = owner;

        reputations[contributorId] = Reputation({
            score: score,
            updatedAt: block.timestamp,
            exists: true
        });

        emit ReputationMinted(
            contributorId,
            owner,
            score
        );
    }

    function updateReputation(
        uint256 contributorId,
        uint256 newScore
    ) external onlyAdmin {

        require(reputations[contributorId].exists, "Reputation does not exist");
        require(newScore <= 100, "Score must be 0-100");

        uint256 oldScore = reputations[contributorId].score;

        reputations[contributorId].score = newScore;
        reputations[contributorId].updatedAt = block.timestamp;

        emit ReputationUpdated(
            contributorId,
            oldScore,
            newScore
        );
    }

    function getReputation(
        uint256 contributorId
    )
        external
        view
        returns (
            uint256 score,
            uint256 updatedAt,
            address owner
        )
    {
        require(
            reputations[contributorId].exists,
            "Reputation does not exist"
        );

        return (
            reputations[contributorId].score,
            reputations[contributorId].updatedAt,
            owners[contributorId]
        );
    }

    // Soulbound: there is deliberately no transfer function.
    // Reputation is permanently associated with the contributor ID.
}
