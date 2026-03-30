import os
import pickle
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

with open("vectorstore/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


def search_chunks(question):
    results = []
    words = question.lower().split()

    for chunk in chunks:
        chunk_lower = chunk.lower()
        if any(word in chunk_lower for word in words):
            results.append(chunk)

    return results[:5]


def get_answer(question: str) -> str:
    try:
        relevant_chunks = search_chunks(question)
        context = "\n\n".join(relevant_chunks)

        prompt = f"""You are a helpful assistant for Workshop Carnival 2.0.
Answer ONLY using the context below.
If not found, say you don't know.

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
        return f"Error: {str(e)}"