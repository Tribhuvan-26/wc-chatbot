import os
import pickle
import re
from google import genai

# Get API key from Render environment
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)

# Ensure vectorstore exists
if not os.path.exists("vectorstore/chunks.pkl"):
    import ingest
    ingest.main()

# Load chunks
with open("vectorstore/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


# ---------- NEW: NORMALIZE ----------
def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text


# ---------- NEW: SYNONYMS ----------
SYNONYMS = {
    "ai": ["artificial intelligence", "machine learning"],
    "ml": ["machine learning"],
    "hacking": ["ethical hacking", "cybersecurity"],
    "cyber": ["cybersecurity", "security"],
    "web": ["web development", "frontend", "backend"],
    "python": ["programming", "coding"]
}


def expand_query(query):
    words = query.split()
    expanded = words[:]

    for word in words:
        if word in SYNONYMS:
            expanded.extend(SYNONYMS[word])

    return " ".join(expanded)


# ---------- UPDATED SEARCH ----------
def search_chunks(question):
    query = normalize(question)
    query = expand_query(query)

    results = []

    for chunk in chunks:
        chunk_text = normalize(chunk)

        score = 0
        for word in query.split():
            if word in chunk_text:
                score += 1

        if score > 0:
            results.append((score, chunk))

    results.sort(reverse=True, key=lambda x: x[0])

    return [chunk for _, chunk in results[:3]]


# ---------- UPDATED ANSWER ----------
def get_answer(question: str) -> str:
    try:
        relevant_chunks = search_chunks(question)

        if not relevant_chunks:
            context = "General workshop topics include AI, Web Development, Cybersecurity, and Programming."
        else:
            context = "\n\n".join(relevant_chunks)

        prompt = f"""You are a helpful assistant for Workshop Carnival 2.0.
Answer using the context below. If exact info is missing, give a helpful related answer.

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