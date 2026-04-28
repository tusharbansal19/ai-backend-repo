"""
rag/embedder.py — free local embeddings (HuggingFace)
"""

from functools import lru_cache
from typing import List, Optional


@lru_cache(maxsize=1)
def _get_embedding_model():
    try:
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    except Exception:
        return None


def get_embedding_model():
    return _get_embedding_model()


def embed_text(text: str) -> List[float]:
    model = _get_embedding_model()
    if model is None:
        return []
    return model.embed_query(text)


def embed_batch(texts: List[str]) -> List[List[float]]:
    if not texts:
        return []

    model = _get_embedding_model()
    if model is None:
        return []
    return model.embed_documents(texts)