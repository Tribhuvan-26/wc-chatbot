import os
import pickle
from google import genai

# Load API key from Render
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)

# Auto-generate chunks if missing
if not os.path.exists("vectorstore/chunks.pkl"):
    import ingest
    ingest.main()

# Load chunks
with open("vectorstore/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


# 🔥 SMART SEARCH (keyword + synonym + scoring)
def search_chunks(question):
    q = question.lower()

    synonyms = {
        "fee": ["cost", "price", "registration"],
        "domain": ["field", "track", "workshop"],
        "team": ["duo", "trio", "group"],
        "prize": ["reward", "winnings", "cash"],
        "ai": ["agentic ai"],
        "hacking": ["ethical hacking", "cybersecurity"],
        "data": ["data analytics"],
        "design": ["ui ux"]
    }

    words = set(q.split())

    # expand words using synonyms
    expanded = set(words)
    for word in words:
        if word in synonyms:
            expanded.update(synonyms[word])

    results = []

    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = sum(1 for word in expanded if word in chunk_lower)

        if score > 0:
            results.append((score, chunk))

    results.sort(reverse=True)
    return [chunk for _, chunk in results[:5]]


# ⚡ FAST DIRECT ANSWERS (no Gemini needed)
def quick_answer(question):
    q = question.lower()

    if any(x in q for x in ["fee", "cost", "price"]):
        return "The registration fee is ₹369 per head."

    if any(x in q for x in ["prize", "reward", "winnings"]):
        return "The total prize pool is ₹30,000."

    if any(x in q for x in ["domain", "workshop", "field"]):
        return "The domains are App Dev, Web Dev, Agentic AI, Ethical Hacking, Data Analytics, and UI/UX."

    if any(x in q for x in ["team", "duo", "trio", "group"]):
        return "You can register as solo, duo, or trio. The fee is ₹369 per person."

    return None


# 🤖 MAIN FUNCTION
def get_answer(question: str) -> str:
    try:
        # 1. Try quick answers first (fast + reliable)
        fast = quick_answer(question)
        if fast:
            return fast

        # 2. Search relevant chunks
        relevant_chunks = search_chunks(question)
        context = "\n\n".join(relevant_chunks)

        # 3. Generate answer using Gemini
        prompt = f"""
You are a friendly assistant for Workshop Carnival 2.0.

Answer naturally like a human (not robotic).

Rules:
- Keep answers short and clear
- Use context below
- If info is missing, still try to help
- Mention ₹369 for fee-related questions
- Mention ₹30,000 for prize questions

Context:
{context}

Question: {question}

Answer:
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        return f"Error: {str(e)}"