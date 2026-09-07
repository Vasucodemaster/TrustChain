from ml.contribution_quality.scorer import ContributionQualityScorer


class F4Service:

    def __init__(self):
        self.scorer = ContributionQualityScorer()

    def score_contribution(self, contribution):

        contribution_type = contribution["type"].upper()

        if contribution_type == "CODE":

            result = self.scorer.score_code(contribution)

            return {
                "code_quality": result["code_quality"],
                "research_quality": 0.0,
                "impact_score": float(contribution["impact"]),
                "quality_score": result["code_quality"],
                "model_version": "F4-v1-CodeBERT"
            }

        elif contribution_type == "RESEARCH":

            result = self.scorer.score_research(contribution)

            return {
                "code_quality": 0.0,
                "research_quality": result["research_quality"],
                "impact_score": float(contribution["impact"]),
                "quality_score": result["research_quality"],
                "model_version": "F4-v1-SciBERT"
            }

        elif contribution_type == "DOCUMENTATION":

            result = self.scorer.score_documentation(contribution)

            return {
                "code_quality": 0.0,
                "research_quality": 0.0,
                "impact_score": float(contribution["impact"]),
                "quality_score": result["documentation_quality"],
                "model_version": "F4-v1-SciBERT-Documentation"
            }

        else:
            raise ValueError(
                "Unsupported contribution type. "
                "Use CODE, RESEARCH, or DOCUMENTATION."
            )
