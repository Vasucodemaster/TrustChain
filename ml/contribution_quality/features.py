import numpy as np


def normalize(value, minimum, maximum):
    if maximum == minimum:
        return 0.0

    return (value - minimum) / (maximum - minimum)


def calculate_engineering_score(row):
    complexity_score = max(
        0,
        100 - float(row["complexity"]) * 5
    )

    test_score = float(row["test_coverage"])
    documentation_score = float(row["documentation_quality"])
    review_score = float(row["review_quality"])
    impact_score = float(row["impact"])

    score = (
        0.15 * complexity_score +
        0.25 * test_score +
        0.20 * documentation_score +
        0.20 * review_score +
        0.20 * impact_score
    )

    return float(np.clip(score, 0, 100))


def calculate_research_score(row):
    methodology = float(row["methodology_quality"])
    technical_depth = float(row["technical_depth"])
    clarity = float(row["clarity"])
    novelty = float(row["novelty"])
    impact = float(row["impact"])

    score = (
        0.25 * methodology +
        0.25 * technical_depth +
        0.15 * clarity +
        0.20 * novelty +
        0.15 * impact
    )

    return float(np.clip(score, 0, 100))
def calculate_documentation_score(row):
    clarity = float(row["clarity"])
    technical_depth = float(row["technical_depth"])
    completeness = float(row["documentation_quality"])
    impact = float(row["impact"])

    score = (
        0.30 * clarity +
        0.25 * technical_depth +
        0.25 * completeness +
        0.20 * impact
    )

    return float(np.clip(score, 0, 100))
