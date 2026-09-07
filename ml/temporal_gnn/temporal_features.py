from app.database.neo4j import driver


def get_temporal_events():

    with driver.session() as session:

        result = session.run(
            """
            MATCH (u:User)-[:HAS_REPUTATION]->(r:ReputationEvent)

            RETURN
                u.id AS user_id,
                u.name AS user_name,
                r.score AS reputation_score,
                r.timestamp AS timestamp

            ORDER BY u.id, r.timestamp
            """
        )

        return [record.data() for record in result]


def calculate_temporal_features(events):

    user_history = {}

    for event in events:

        user_id = event["user_id"]

        if user_id not in user_history:
            user_history[user_id] = []

        user_history[user_id].append(event)

    features = []

    for user_id, history in user_history.items():

        previous_score = None
        previous_timestamp = None

        for event in history:

            current_score = float(
                event["reputation_score"]
            )

            if previous_score is None:

                change = 0.0
                percentage_change = 0.0
                time_difference = 0.0

            else:

                change = current_score - previous_score

                if previous_score != 0:
                    percentage_change = (
                        change / previous_score
                    ) * 100
                else:
                    percentage_change = 0.0

                duration = event["timestamp"] - previous_timestamp
                time_difference = (
                    duration.days
                    + duration.seconds / 86400
                )

            # Flag unusually large reputation increases.
            anomaly_flag = (
                1
                if percentage_change >= 20
                else 0
            )

            features.append(
                {
                    "user_id": user_id,
                    "user_name": event["user_name"],
                    "timestamp": event["timestamp"],
                    "previous_score": previous_score,
                    "current_score": current_score,
                    "change": round(change, 2),
                    "percentage_change": round(
                        percentage_change,
                        2
                    ),
                    "time_difference_days": round(
                        time_difference,
                        2
                    ),
                    "anomaly_flag": anomaly_flag
                }
            )

            previous_score = current_score
            previous_timestamp = event["timestamp"]

    return features


if __name__ == "__main__":

    events = get_temporal_events()

    features = calculate_temporal_features(
        events
    )

    print("\nTemporal anomaly features:\n")

    for feature in features:
        print(feature)
