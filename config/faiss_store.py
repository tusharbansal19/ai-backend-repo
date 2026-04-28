import os
from dotenv import load_dotenv
load_dotenv()
"""
config/faiss_store.py — local FAISS vector store helpers
"""
from pathlib import Path
from typing import Optional

from rag.embedder import get_embedding_model


def _index_path() -> Path:
    return Path(os.getenv("FAISS_INDEX_DIR", "./faiss_index"))


from functools import lru_cache

@lru_cache(maxsize=1)
def get_faiss_store():
    """
    Load FAISS vector store if it exists, otherwise return None.
    """
    model = get_embedding_model()
    if model is None:
        return None

    from langchain_community.vectorstores import FAISS

    index_dir = _index_path()
    index_file = index_dir / "index.faiss"
    if not index_file.exists():
        return None

    return FAISS.load_local(
        folder_path=str(index_dir),
        embeddings=model,
        allow_dangerous_deserialization=True,
    )


def save_faiss_store(store) -> None:
    index_dir = _index_path()
    index_dir.mkdir(parents=True, exist_ok=True)
    store.save_local(str(index_dir))