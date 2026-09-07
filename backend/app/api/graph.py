from fastapi import APIRouter

from app.database.neo4j import driver


router = APIRouter(
    prefix="/graph",
    tags=["Graph"]
)


@router.get("/test")
def test_graph():

    with driver.session() as session:

        result = session.run(
            "RETURN 'Neo4j connection successful' AS message"
        )

        record = result.single()

    return {
        "message": record["message"]
    }
