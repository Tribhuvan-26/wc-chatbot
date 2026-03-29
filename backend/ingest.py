import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

DATA_DIR = "data"
VECTOR_DIR = "vectorstore"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def extract_text(data_dir):
    all_text = []
    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        if filename.endswith(".pdf"):
            print(f"Reading PDF: {filename}")
            reader = PdfReader(filepath)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    all_text.append(text)
        elif filename.endswith(".txt"):
            print(f"Reading TXT: {filename}")
            with open(filepath, "r", encoding="utf-8") as f:
                all_text.append(f.read())
    return all_text

def chunk_text(pages, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    for page in pages:
        words = page.split()
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i+chunk_size])
            if chunk.strip():
                chunks.append(chunk)
    return chunks

def embed_and_store(chunks):
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print(f"Embedding {len(chunks)} chunks...")
    embeddings = model.encode(chunks, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, os.path.join(VECTOR_DIR, "index.faiss"))
    with open(os.path.join(VECTOR_DIR, "chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)
    print(f"✅ Saved {index.ntotal} vectors to vectorstore/")

if __name__ == "__main__":
    pages = extract_text(DATA_DIR)
    print(f"Extracted {len(pages)} pages/files")
    chunks = chunk_text(pages)
    print(f"Created {len(chunks)} chunks")
    embed_and_store(chunks)