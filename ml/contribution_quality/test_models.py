from ml.contribution_quality.models import (
    CodeBERTEncoder,
    SciBERTEncoder
)


print("Loading CodeBERT...")

code_model = CodeBERTEncoder()

code_embedding = code_model.encode(
    "def add(a, b): return a + b"
)

print(
    "CodeBERT embedding dimension:",
    len(code_embedding)
)


print("Loading SciBERT...")

research_model = SciBERTEncoder()

research_embedding = research_model.encode(
    "We propose a privacy-preserving machine learning framework."
)

print(
    "SciBERT embedding dimension:",
    len(research_embedding)
)
