"""
RAG Tool — handles PDF processing, chunking, embedding, and retrieval.

This is the engine behind the document agent.
"""

import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions


# ChromaDB setup — persistent storage in project folder
CHROMA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
COLLECTION_NAME = "research_documents"


def get_chroma_collection():
    """Get or create the ChromaDB collection."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Use sentence-transformers for embeddings (runs locally)
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn,
    )

    return collection


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """
    Extract text from a PDF file, page by page.
    
    Returns a list of dicts: [{"text": "...", "page": 1, "source": "filename.pdf"}, ...]
    """
    reader = PdfReader(pdf_path)
    filename = os.path.basename(pdf_path)
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            pages.append({
                "text": text.strip(),
                "page": i + 1,
                "source": filename,
            })

    return pages


def chunk_text(pages: list[dict]) -> list[dict]:
    """
    Split page text into smaller chunks for better retrieval.
    
    Uses 1000-char chunks with 200-char overlap (same as your RAG project).
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    chunks = []
    for page in pages:
        splits = splitter.split_text(page["text"])
        for j, split in enumerate(splits):
            chunks.append({
                "text": split,
                "page": page["page"],
                "source": page["source"],
                "chunk_id": f"{page['source']}_p{page['page']}_c{j}",
            })

    return chunks


def index_pdf(pdf_path: str) -> int:
    """
    Full pipeline: extract text → chunk → embed → store in ChromaDB.
    
    Returns the number of chunks indexed.
    """
    collection = get_chroma_collection()

    # Extract and chunk
    pages = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(pages)

    if not chunks:
        return 0

    # Add to ChromaDB
    collection.add(
        ids=[c["chunk_id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[{"source": c["source"], "page": c["page"]} for c in chunks],
    )

    return len(chunks)


def search_documents(query: str, top_k: int = 4) -> list[dict]:
    """
    Search ChromaDB for chunks most relevant to the query.
    
    Returns top_k results with content, source, and page number.
    """
    collection = get_chroma_collection()

    # Check if collection has any documents
    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count()),
    )

    # Format results
    formatted = []
    for i in range(len(results["documents"][0])):
        formatted.append({
            "content": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "page": results["metadatas"][0][i]["page"],
            "distance": results["distances"][0][i],
        })

    return formatted