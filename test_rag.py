"""
Quick test to verify the RAG pipeline works:
PDF extraction → chunking → ChromaDB indexing → search
"""

import os
from tools.rag_tool import extract_text_from_pdf, chunk_text, index_pdf, search_documents

# Update this to match your exact filename
PDF_PATH = "data/documents/SQL Cheat sheet.pdf"

print("Step 1: Extracting text from PDF...")
pages = extract_text_from_pdf(PDF_PATH)
print(f"  Extracted {len(pages)} pages")
for p in pages[:3]:
    print(f"  Page {p['page']}: {p['text'][:80]}...")

print("\nStep 2: Chunking text...")
chunks = chunk_text(pages)
print(f"  Created {len(chunks)} chunks")

print("\nStep 3: Indexing into ChromaDB...")
num_indexed = index_pdf(PDF_PATH)
print(f"  Indexed {num_indexed} chunks")

print("\nStep 4: Searching...")
query = "How do I write a JOIN query?"
results = search_documents(query, top_k=3)
print(f"  Query: '{query}'")
print(f"  Found {len(results)} results:\n")

for i, r in enumerate(results):
    print(f"  Result {i+1} (page {r['page']}, distance: {r['distance']:.4f}):")
    print(f"  {r['content'][:150]}...")
    print()

print("RAG pipeline working!")