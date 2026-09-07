from fastapi import APIRouter
import torch

from ml.temporal_gnn.model import create_temporal_gnn

router = APIRouter(
    prefix="/temporal-anomaly",
    tags=["Temporal Anomaly Detection"]
)

MODEL_PATH = "temporal_gnn_model.pt"

model = create_temporal_gnn()
model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=torch.device("cpu")
    )
)
model.eval()


@router.get("/test")
def temporal_anomaly_test():

    x1 = torch.tensor(
        [
            [0.65, 0.0, 0.0, 0.0],
            [0.70, 0.0, 0.0, 0.0]
        ],
        dtype=torch.float32
    )

    x2 = torch.tensor(
        [
            [0.72, 0.1077, 1.0, 0.0],
            [0.95, 0.3571, 1.0, 1.0]
        ],
        dtype=torch.float32
    )

    adjacency = torch.tensor(
        [
            [1.0, 0.2],
            [0.2, 1.0]
        ],
        dtype=torch.float32
    )

    graph_snapshots = [
        (x1, adjacency),
        (x2, adjacency)
    ]

    with torch.no_grad():

        predictions = model(
            graph_snapshots
        )

    scores = predictions.flatten().tolist()

    return {
        "status": "success",
        "users": [
            {
                "user_id": 1,
                "anomaly_score": scores[0]
            },
            {
                "user_id": 2,
                "anomaly_score": scores[1]
            }
        ]
    }
