import os
import warnings
import logging
warnings.filterwarnings("ignore")
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("faiss").setLevel(logging.ERROR)
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
embedder = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("vectorstore/index.faiss")
with open("vectorstore/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

def get_answer(question: str) -> str:
    try:
        question_embedding = embedder.encode([question])
        question_embedding = np.array(question_embedding).astype("float32")
        _, indices = index.search(question_embedding, k=5)
        relevant_chunks = [chunks[i] for i in indices[0] if i < len(chunks)]
        context = "\n\n".join(relevant_chunks)
        prompt = f"""You are a helpful assistant for Workshop Carnival 2.0, organized by MLRIT-CIE.
Answer the user's question using ONLY the context provided below.
If the answer is not in the context, say "I don't have that information right now. Please contact us at ciemlrit@mlrit.ac.in"

Context:
{context}

Question: {question}

Answer:"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"