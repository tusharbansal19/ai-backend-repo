import os
from dotenv import load_dotenv
load_dotenv()
"""
rag/retriever.py — fetch relevant chunks from local FAISS store
"""

from typing import Any, Dict, List

from config.faiss_store import get_faiss_store

TOP_K = int(os.getenv("RAG_TOP_K", "3"))
SCORE_THRESHOLD = float(os.getenv("RAG_SCORE_THRESHOLD", "0.40"))

def retrieve_context(query: str) -> List[Dict[str, Any]]:
    store = get_faiss_store()
    if store is None:
        return []

    if not query.strip():
        return []

    results = store.similarity_search_with_score(query, k=TOP_K)

    output = []

    for doc, dist in results:
        # FAISS returns distance; convert to bounded similarity-like score.
        score = 1.0 / (1.0 + float(dist))

        if score < SCORE_THRESHOLD:
            continue

        meta = doc.metadata or {}

        output.append({
            "text": doc.page_content,
            "score": round(score, 4),
            "source": meta.get("source", "unknown"),
            "fileName": meta.get("fileName", ""),
            "type": meta.get("type", "unknown"),
        })

    return output


def format_context_for_prompt(chunks: List[Dict[str, Any]]) -> str:
    if not chunks:
        return ""

    context = "## Context\n\n"

    for i, chunk in enumerate(chunks, 1):
        context += f"[{i}] {chunk['text']}\n\n"

    return context