import torch
import torch.nn as nn
import torch.optim as optim

from ml.temporal_gnn.model import create_temporal_gnn


def create_training_data():

    # Snapshot 1
    x1 = torch.tensor(
        [
            [0.65, 0.0, 0.0, 0.0],
            [0.70, 0.0, 0.0, 0.0]
        ],
        dtype=torch.float32
    )

    # Snapshot 2
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

    # Ground-truth anomaly labels from F2.2.
    labels = torch.tensor(
        [
            [0.0],
            [1.0]
        ],
        dtype=torch.float32
    )

    return graph_snapshots, labels


def train_model(epochs=100):

    graph_snapshots, labels = create_training_data()

    model = create_temporal_gnn()

    optimizer = optim.Adam(
        model.parameters(),
        lr=0.01
    )

    loss_function = nn.MSELoss()

    model.train()

    for epoch in range(epochs):

        optimizer.zero_grad()

        predictions = model(
            graph_snapshots
        )

        loss = loss_function(
            predictions,
            labels
        )

        loss.backward()

        optimizer.step()

        if (epoch + 1) % 20 == 0:

            print(
                f"Epoch {epoch + 1}/{epochs} "
                f"Loss: {loss.item():.6f}"
            )

    return model


if __name__ == "__main__":

    model = train_model()

    graph_snapshots, labels = create_training_data()

    model.eval()

    with torch.no_grad():

        predictions = model(
            graph_snapshots
        )

    print("\nTraining complete")

    print(
        "Predictions:",
        predictions.flatten().tolist()
    )

    print(
        "Labels:",
        labels.flatten().tolist()
    )

    torch.save(
        model.state_dict(),
        "temporal_gnn_model.pt"
    )

    print(
        "Model saved to temporal_gnn_model.pt"
    )
