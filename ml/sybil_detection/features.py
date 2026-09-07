from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Set, Tuple


def jaccard_similarity(a: Set[int], b: Set[int]) -> float:
    """Return Jaccard similarity between two sets."""
    if not a and not b:
        return 0.0

    union = a | b
    if not union:
        return 0.0

    return len(a & b) / len(union)


def build_structural_features(
    users: List[Dict],
    contributions: List[Dict],
    user_contribution_edges: List[Tuple[int, int]],
    reputation_scores: Dict[int, List[float]],
) -> List[Dict]:
    """
    Build structural Sybil-detection features for each contributor.

    Features:
        degree                  - number of contributions
        contribution_overlap   - maximum overlap with another user
        neighbor_similarity     - maximum Jaccard similarity
        reputation_similarity   - similarity of reputation behavior
        cluster_density          - density of the user's suspicious neighborhood
    """

    user_ids = [int(user["id"]) for user in users]

    user_contributions: Dict[int, Set[int]] = defaultdict(set)

    for user_id, contribution_id in user_contribution_edges:
        user_contributions[int(user_id)].add(int(contribution_id))

    # User-to-user similarity based on shared contribution structure.
    similarities: Dict[int, List[float]] = defaultdict(list)

    for i, user_a in enumerate(user_ids):
        for user_b in user_ids[i + 1:]:
            set_a = user_contributions[user_a]
            set_b = user_contributions[user_b]

            similarity = jaccard_similarity(set_a, set_b)

            similarities[user_a].append(similarity)
            similarities[user_b].append(similarity)

    features = []

    for user_id in user_ids:
        contribution_set = user_contributions[user_id]

        degree = len(contribution_set)

        max_similarity = (
            max(similarities[user_id])
            if similarities[user_id]
            else 0.0
        )

        # Contribution overlap is represented by the same structural
        # similarity signal, making it easy to explain in the prototype.
        contribution_overlap = max_similarity

        # Reputation similarity:
        # compare the user's average reputation with the averages
        # of other users. Higher similarity means more similar behavior.
        own_scores = reputation_scores.get(user_id, [])
        own_average = (
            sum(own_scores) / len(own_scores)
            if own_scores
            else 0.0
        )

        reputation_similarities = []

        for other_id in user_ids:
            if other_id == user_id:
                continue

            other_scores = reputation_scores.get(other_id, [])

            if not other_scores:
                continue

            other_average = sum(other_scores) / len(other_scores)

            similarity = 1.0 - min(
                abs(own_average - other_average) / 100.0,
                1.0,
            )

            reputation_similarities.append(similarity)

        reputation_similarity = (
            max(reputation_similarities)
            if reputation_similarities
            else 0.0
        )

        # A compact cluster-density proxy for the prototype:
        # high structural similarity to other contributors indicates
        # a potentially coordinated neighborhood.
        cluster_density = max_similarity

        features.append(
            {
                "user_id": user_id,
                "degree": float(degree),
                "contribution_overlap": float(contribution_overlap),
                "neighbor_similarity": float(max_similarity),
                "reputation_similarity": float(reputation_similarity),
                "cluster_density": float(cluster_density),
            }
        )

    return features
