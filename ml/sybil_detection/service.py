from __future__ import annotations

from pathlib import Path
from typing import Dict

import torch

from ml.sybil_detection.features import build_structural_features
from ml.sybil_detection.model import create_sybil_gnn


MODEL_PATH = Path(__file__).resolve().parents[2] / "sybil_gnn_model.pt"


class SybilDetectionService:
    def __init__(self):
        self.model = create_sybil_gnn()

        self.model.load_state_dict(
            torch.load(
                MODEL_PATH,
                map_location=torch.device("cpu"),
            )
        )

        self.model.eval()

    def predict(
        self,
        users,
        contributions,
        user_contribution_edges,
        reputation_scores,
    ):
        features = build_structural_features(
            users=users,
            contributions=contributions,
            user_contribution_edges=user_contribution_edges,
            reputation_scores=reputation_scores,
        )

        if not features:
            return []

        feature_tensor = torch.tensor(
            [
                [
                    item["degree"],
                    item["contribution_overlap"],
                    item["neighbor_similarity"],
                    item["reputation_similarity"],
                    item["cluster_density"],
                ]
                for item in features
            ],
            dtype=torch.float32,
        )

        user_count = len(features)

        # Build a basic user adjacency matrix.
        # Users with structural similarity are connected.
        adjacency = torch.zeros(
            (user_count, user_count),
            dtype=torch.float32,
        )

        for i in range(user_count):
            for j in range(user_count):
                if i == j:
                    continue

                similarity = min(
                    features[i]["neighbor_similarity"],
                    features[j]["neighbor_similarity"],
                )

                if similarity >= 0.5:
                    adjacency[i, j] = 1.0

        with torch.no_grad():
            probabilities = self.model(
                feature_tensor,
                adjacency,
            )

        results = []

        for item, probability in zip(
            features,
            probabilities.tolist(),
        ):
            risk = float(probability)

            if risk >= 0.75:
                classification = "HIGH_RISK"
            elif risk >= 0.50:
                classification = "MEDIUM_RISK"
            else:
                classification = "LOW_RISK"

            results.append(
                {
                    "user_id": item["user_id"],
                    "sybil_probability": round(risk, 4),
                    "risk_level": classification,
                    "structural_features": {
                        "degree": item["degree"],
                        "contribution_overlap": item[
                            "contribution_overlap"
                        ],
                        "neighbor_similarity": item[
                            "neighbor_similarity"
                        ],
                        "reputation_similarity": item[
                            "reputation_similarity"
                        ],
                        "cluster_density": item[
                            "cluster_density"
                        ],
                    },
                }
            )

        return results
