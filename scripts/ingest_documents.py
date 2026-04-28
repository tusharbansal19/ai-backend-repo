"""
scripts/ingest_documents.py
===========================
Ingests your portfolio documents into local FAISS for RAG.
Run once (or whenever you update your data):
    python scripts/ingest_documents.py
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from config.faiss_store import get_faiss_store, save_faiss_store
from rag.embedder import get_embedding_model
from rag.chunker import chunk_text

DATA_SOURCES = [
    {"path": "rag/datasource.txt",   "type": "datasource",  "source": "datasource"},
]


def load_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


def ingest():
    model = get_embedding_model()
    if model is None:
        print("Embedding model unavailable. Ingestion aborted.")
        return

    from langchain_community.vectorstores import FAISS

    store = get_faiss_store()
    total_chunks = 0

    for source in DATA_SOURCES:
        text = load_file(source["path"])
        if not text.strip():
            continue

        chunks = chunk_text(
            text=text,
            source=source["source"],
            file_name=Path(source["path"]).name,
            doc_type=source["type"],
        )
        if not chunks:
            continue

        documents  = [c["text"] for c in chunks]
        metadatas  = [
            {
                "source":   c["source"],
                "fileName": c["fileName"],
                "type":     c["type"],
                "chunkIndex": c["chunkIndex"],
            }
            for c in chunks
        ]

        if store is None:
            store = FAISS.from_texts(documents, embedding=model, metadatas=metadatas)
        else:
            store.add_texts(documents, metadatas=metadatas)

        total_chunks += len(chunks)

    if store is None:
        print("No valid content found to ingest.")
        return

    save_faiss_store(store)
    print(f"Ingestion complete. Total chunks indexed: {total_chunks}")


if __name__ == "__main__":
    ingest()
