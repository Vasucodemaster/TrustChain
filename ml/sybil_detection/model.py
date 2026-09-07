from __future__ import annotations

import torch
import torch.nn as nn


class StructuralGraphConvolution(nn.Module):
    """Simple graph convolution layer for structural analysis."""

    def __init__(self, input_size: int, output_size: int):
        super().__init__()

        self.linear = nn.Linear(input_size, output_size)

    def forward(
        self,
        x: torch.Tensor,
        adjacency: torch.Tensor,
    ) -> torch.Tensor:
        # Add self-loops so each node retains its own information.
        identity = torch.eye(
            adjacency.size(0),
            device=adjacency.device,
        )

        graph = adjacency + identity

        # Row-normalize the adjacency matrix.
        degree = graph.sum(dim=1, keepdim=True).clamp(min=1.0)
        normalized_graph = graph / degree

        aggregated = torch.matmul(normalized_graph, x)

        return torch.relu(self.linear(aggregated))


class SybilDetectionGNN(nn.Module):
    """
    Structural GNN for contributor Sybil-risk prediction.

    Input features:
        1. degree
        2. contribution overlap
        3. neighbor similarity
        4. reputation similarity
        5. cluster density

    Output:
        Sybil probability for every contributor.
    """

    def __init__(
        self,
        input_size: int = 5,
        hidden_size: int = 16,
    ):
        super().__init__()

        self.graph_layer = StructuralGraphConvolution(
            input_size,
            hidden_size,
        )

        self.second_graph_layer = StructuralGraphConvolution(
            hidden_size,
            hidden_size,
        )

        self.output_layer = nn.Linear(hidden_size, 1)

    def forward(
        self,
        x: torch.Tensor,
        adjacency: torch.Tensor,
    ) -> torch.Tensor:
        hidden = self.graph_layer(
            x,
            adjacency,
        )

        hidden = self.second_graph_layer(
            hidden,
            adjacency,
        )

        logits = self.output_layer(hidden)

        return torch.sigmoid(logits).squeeze(-1)


def create_sybil_gnn() -> SybilDetectionGNN:
    return SybilDetectionGNN(
        input_size=5,
        hidden_size=16,
    )
