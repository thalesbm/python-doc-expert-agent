from langchain_core.documents import Document
from typing import List

def remove_duplicate_chunks(chunks: List[Document]):
    unique_chunks = []
    seen_contents = set()

    for chunk in chunks:
        if chunk.page_content not in seen_contents:
            unique_chunks.append(chunk)
            seen_contents.add(chunk.page_content)
    return unique_chunks