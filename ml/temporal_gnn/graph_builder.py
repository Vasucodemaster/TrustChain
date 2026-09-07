from datetime import datetime, timedelta

from app.database.neo4j import driver


def clear_test_graph():
    with driver.session() as session:
        session.run(
            """
            MATCH (n)
            DETACH DELETE n
            """
        )


def create_temporal_graph():

    base_time = datetime.now()

    with driver.session() as session:

        # Create users
        session.run(
            """
            CREATE (u1:User {
                id: 1,
                name: 'Institution User 1'
            })

            CREATE (u2:User {
                id: 2,
                name: 'Institution User 2'
            })
            """
        )

        # Create contributions
        session.run(
            """
            MATCH (u1:User {id: 1})
            MATCH (u2:User {id: 2})

            CREATE (c1:Contribution {
                id: 101,
                title: 'Authentication Module',
                timestamp: $t1
            })

            CREATE (c2:Contribution {
                id: 102,
                title: 'Research Paper',
                timestamp: $t2
            })

            CREATE (u1)-[:CONTRIBUTED_TO]->(c1)
            CREATE (u2)-[:CONTRIBUTED_TO]->(c2)
            """,
            t1=base_time,
            t2=base_time + timedelta(days=1)
        )

        # Create reputation events
        session.run(
            """
            MATCH (u1:User {id: 1})
            MATCH (u2:User {id: 2})

            CREATE (r1:ReputationEvent {
                score: 65.0,
                timestamp: $t1
            })

            CREATE (r2:ReputationEvent {
                score: 72.0,
                timestamp: $t2
            })

            CREATE (r3:ReputationEvent {
                score: 70.0,
                timestamp: $t3
            })

            CREATE (r4:ReputationEvent {
                score: 95.0,
                timestamp: $t4
            })

            CREATE (u1)-[:HAS_REPUTATION]->(r1)
            CREATE (u1)-[:HAS_REPUTATION]->(r2)
            CREATE (u2)-[:HAS_REPUTATION]->(r3)
            CREATE (u2)-[:HAS_REPUTATION]->(r4)
            """,
            t1=base_time,
            t2=base_time + timedelta(days=1),
            t3=base_time + timedelta(days=2),
            t4=base_time + timedelta(days=3)
        )


def get_temporal_graph():

    with driver.session() as session:

        result = session.run(
            """
            MATCH (u:User)-[:HAS_REPUTATION]->(r:ReputationEvent)

            RETURN
                u.id AS user_id,
                u.name AS user_name,
                r.score AS reputation_score,
                r.timestamp AS timestamp

            ORDER BY r.timestamp
            """
        )

        return [record.data() for record in result]


if __name__ == "__main__":

    clear_test_graph()

    create_temporal_graph()

    graph = get_temporal_graph()

    for event in graph:
        print(event)
