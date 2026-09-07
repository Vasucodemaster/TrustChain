import torch
import torch.nn as nn


class TemporalGraphConvolution(nn.Module):

    def __init__(self, input_size, hidden_size):
        super().__init__()

        self.weight = nn.Parameter(
            torch.randn(input_size, hidden_size) * 0.1
        )

        self.bias = nn.Parameter(
            torch.zeros(hidden_size)
        )

    def forward(self, x, adjacency):

        # Graph message passing
        messages = torch.matmul(adjacency, x)

        # Linear transformation
        output = torch.matmul(
            messages,
            self.weight
        ) + self.bias

        return torch.relu(output)


class TemporalGNN(nn.Module):

    def __init__(
        self,
        input_size=4,
        hidden_size=16,
        output_size=1
    ):
        super().__init__()

        self.graph_layer = TemporalGraphConvolution(
            input_size,
            hidden_size
        )

        # Evolves node representations through time.
        self.temporal_layer = nn.GRU(
            input_size=hidden_size,
            hidden_size=hidden_size,
            batch_first=True
        )

        self.output_layer = nn.Linear(
            hidden_size,
            output_size
        )

    def forward(self, graph_snapshots):

        temporal_outputs = []

        for x, adjacency in graph_snapshots:

            graph_features = self.graph_layer(
                x,
                adjacency
            )

            temporal_outputs.append(
                graph_features
            )

        # [time, nodes, hidden]
        sequence = torch.stack(
            temporal_outputs,
            dim=0
        )

        # [nodes, time, hidden]
        sequence = sequence.permute(
            1, 0, 2
        )

        temporal_output, _ = self.temporal_layer(
            sequence
        )

        final_state = temporal_output[:, -1, :]

        anomaly_score = self.output_layer(
            final_state
        )

        return anomaly_score


def create_temporal_gnn():

    return TemporalGNN(
        input_size=4,
        hidden_size=16,
        output_size=1
    )
