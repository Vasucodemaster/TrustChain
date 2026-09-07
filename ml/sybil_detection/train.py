from __future__ import annotations

import torch
import torch.nn as nn
import torch.optim as optim

from ml.sybil_detection.model import create_sybil_gnn


def build_training_graph():
    """
    Controlled demonstration graph.

    Nodes 0-5: legitimate contributors
    Nodes 6-9: coordinated/Sybil-like contributors
    """

    features = torch.tensor(
        [
            # degree, overlap, neighbor similarity, reputation similarity, density
            [0.60, 0.10, 0.12, 0.30, 0.10],
            [0.55, 0.08, 0.10, 0.35, 0.08],
            [0.65, 0.12, 0.15, 0.28, 0.12],
            [0.50, 0.09, 0.11, 0.32, 0.09],
            [0.70, 0.14, 0.16, 0.25, 0.13],
            [0.58, 0.11, 0.13, 0.31, 0.10],

            # Coordinated/Sybil-like cluster
            [0.85, 0.88, 0.92, 0.94, 0.90],
            [0.82, 0.91, 0.89, 0.96, 0.92],
            [0.87, 0.86, 0.94, 0.93, 0.91],
            [0.84, 0.90, 0.91, 0.95, 0.93],
        ],
        dtype=torch.float32,
    )

    adjacency = torch.tensor(
        [
            # Legitimate community
            [1, 1, 1, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 1, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 1, 0, 0, 0, 0],

            # Dense coordinated cluster
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        ],
        dtype=torch.float32,
    )

    labels = torch.tensor(
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        dtype=torch.float32,
    )

    return features, adjacency, labels


def train():
    torch.manual_seed(42)

    features, adjacency, labels = build_training_graph()

    model = create_sybil_gnn()

    optimizer = optim.Adam(
        model.parameters(),
        lr=0.01,
        weight_decay=0.0001,
    )

    loss_function = nn.BCELoss()

    for epoch in range(500):
        model.train()

        optimizer.zero_grad()

        predictions = model(
            features,
            adjacency,
        )

        loss = loss_function(
            predictions,
            labels,
        )

        loss.backward()
        optimizer.step()

        if (epoch + 1) % 100 == 0:
            print(
                f"Epoch {epoch + 1}/500 "
                f"- Loss: {loss.item():.4f}"
            )

    model.eval()

    with torch.no_grad():
        predictions = model(
            features,
            adjacency,
        )

    print("\nFinal predictions:")

    for index, probability in enumerate(predictions.tolist()):
        category = (
            "SYBIL-RISK"
            if probability >= 0.5
            else "LEGITIMATE"
        )

        print(
            f"User {index + 1}: "
            f"{probability:.4f} -> {category}"
        )

    torch.save(
        model.state_dict(),
        "sybil_gnn_model.pt",
    )

    print("\nModel saved to sybil_gnn_model.pt")


if __name__ == "__main__":
    train()
