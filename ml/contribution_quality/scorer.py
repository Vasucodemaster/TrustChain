import numpy as np

from ml.contribution_quality.models import (
    CodeBERTEncoder,
    SciBERTEncoder
)

from ml.contribution_quality.features import (
    calculate_engineering_score,
    calculate_research_score,
    calculate_documentation_score
)


class ContributionQualityScorer:

    def __init__(self):
        self.codebert = None
        self.scibert = None

    def load_code_model(self):
        if self.codebert is None:
            self.codebert = CodeBERTEncoder()

    def load_research_model(self):
        if self.scibert is None:
            self.scibert = SciBERTEncoder()

    def score_code(self, row):
        self.load_code_model()

        text = (
            str(row["title"]) + " " +
            str(row["description"]) + " " +
            str(row["code_text"])
        )

        embedding = self.codebert.encode(text)

        semantic_signal = float(np.linalg.norm(embedding))
        semantic_score = min(
            100,
            50 + semantic_signal * 2
        )

        engineering_score = calculate_engineering_score(row)

        final_score = (
            0.30 * semantic_score +
            0.70 * engineering_score
        )

        return {
            "code_quality": round(
                float(np.clip(final_score, 0, 100)),
                2
            ),
            "embedding_dimension": len(embedding)
        }

    def score_research(self, row):
        self.load_research_model()

        text = (
            str(row["title"]) + " " +
            str(row["description"]) + " " +
            str(row["research_text"])
        )

        embedding = self.scibert.encode(text)

        semantic_signal = float(np.linalg.norm(embedding))
        semantic_score = min(
            100,
            50 + semantic_signal * 2
        )

        research_score = calculate_research_score(row)

        final_score = (
            0.30 * semantic_score +
            0.70 * research_score
        )

        return {
            "research_quality": round(
                float(np.clip(final_score, 0, 100)),
                2
            ),
            "embedding_dimension": len(embedding)
        }

    def score_documentation(self, row):
        self.load_research_model()

        text = (
            str(row["title"]) + " " +
            str(row["description"]) + " " +
            str(row["documentation_text"])
        )

        embedding = self.scibert.encode(text)

        semantic_signal = float(np.linalg.norm(embedding))
        semantic_score = min(
            100,
            50 + semantic_signal * 2
        )

        documentation_score = calculate_documentation_score(row)

        final_score = (
            0.30 * semantic_score +
            0.70 * documentation_score
        )

        return {
            "documentation_quality": round(
                float(np.clip(final_score, 0, 100)),
                2
            ),
            "embedding_dimension": len(embedding)
        }
