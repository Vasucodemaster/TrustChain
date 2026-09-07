from fastapi import APIRouter, HTTPException

from app.database.neo4j import driver
from ml.sybil_detection.service import SybilDetectionService


router = APIRouter(
    prefix="/sybil",
    tags=["Sybil Detection"],
)

service = SybilDetectionService()


@router.get("/test")
def sybil_detection_test():
    """
    Run Sybil-risk analysis on contributors stored in Neo4j.
    """

    with driver.session() as session:

        users = [
            dict(record["u"])
            for record in session.run(
                """
                MATCH (u:User)
                RETURN u
                ORDER BY u.id
                """
            )
        ]

        contributions = [
            dict(record["c"])
            for record in session.run(
                """
                MATCH (c:Contribution)
                RETURN c
                ORDER BY c.id
                """
            )
        ]

        user_contribution_edges = [
            (
                int(record["user_id"]),
                int(record["contribution_id"]),
            )
            for record in session.run(
                """
                MATCH (u:User)-[:CONTRIBUTED_TO]->(c:Contribution)
                RETURN u.id AS user_id, c.id AS contribution_id
                """
            )
        ]

        reputation_scores = {}

        for record in session.run(
            """
            MATCH (u:User)-[:HAS_REPUTATION]->(r:ReputationEvent)
            RETURN u.id AS user_id, collect(r.score) AS scores
            """
        ):
            reputation_scores[int(record["user_id"])] = [
                float(score)
                for score in record["scores"]
            ]

    if not users:
        raise HTTPException(
            status_code=404,
            detail="No users found in Neo4j",
        )

    results = service.predict(
        users=users,
        contributions=contributions,
        user_contribution_edges=user_contribution_edges,
        reputation_scores=reputation_scores,
    )

    return {
        "status": "success",
        "model": "Structural GNN",
        "users_analyzed": len(results),
        "results": results,
    }
