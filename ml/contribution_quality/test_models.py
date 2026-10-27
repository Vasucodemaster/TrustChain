import pytest
import numpy as np
from ml.contribution_quality.models import (
    CodeBERTEncoder,
    SciBERTEncoder,
)


@pytest.fixture(scope="module")
def code_encoder():
    return CodeBERTEncoder()


@pytest.fixture(scope="module")
def sci_encoder():
    return SciBERTEncoder()


def test_codebert_generates_embedding(code_encoder):
    embedding = code_encoder.encode(
        "def add(a, b): return a + b"
    )
    assert embedding is not None
    assert len(embedding) > 0


def test_scibert_generates_embedding(sci_encoder):
    embedding = sci_encoder.encode(
        "We propose a privacy-preserving machine learning framework."
    )
    assert embedding is not None
    assert len(embedding) > 0


def test_codebert_embedding_is_numeric(code_encoder):
    embedding = code_encoder.encode(
        "def multiply(a, b): return a * b"
    )
    assert np.issubdtype(embedding.dtype, np.number)

def test_scibert_embedding_is_numeric(sci_encoder):
    embedding = sci_encoder.encode(
        "Differential privacy protects sensitive training data."
    )
    assert np.issubdtype(embedding.dtype, np.number)
