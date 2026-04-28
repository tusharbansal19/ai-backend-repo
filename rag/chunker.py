"""
rag/chunker.py — simple text splitter using LangChain
"""

from typing import List, Dict

# Lazy initialization function to save memory at boot
def get_splitter():
    from langchain_text_splitters import TokenTextSplitter
    return TokenTextSplitter(
        chunk_size=150,
        chunk_overlap=20
    )

def chunk_text(text: str, source="", file_name="", doc_type="") -> List[Dict]:
    splitter = get_splitter()
    chunks = splitter.split_text(text)

    result = []
    for i, chunk in enumerate(chunks):
        result.append({
            "text": chunk,
            "source": source,
            "fileName": file_name,
            "type": doc_type,
            "chunkIndex": i,
        })
        

    return result