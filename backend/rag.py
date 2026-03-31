import os
import pickle
import time
from google import genai

# Load API key from Render
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)

# Auto-create vectorstore if missing
if not os.path.exists("vectorstore/chunks.pkl"):
    import ingest
    ingest.main()

# Load chunks
with open("vectorstore/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


# 🔍 SMART SEARCH
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


# ⚡ QUICK ANSWERS
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


# 🤖 MAIN FUNCTION (WITH RETRY)
def get_answer(question: str) -> str:
    try:
        # 1. Fast answers first
        fast = quick_answer(question)
        if fast:
            return fast

        # 2. Search context
        relevant_chunks = search_chunks(question)
        context = "\n\n".join(relevant_chunks)

        prompt = f"""
You are a friendly assistant for Workshop Carnival 2.0.

Answer naturally like a human (not robotic).
Keep it short and clear.

Context:
{context}

Question: {question}

Answer:
"""

        # 3. Retry for 503 errors
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                return response.text.replace("*", "").strip()

            except Exception as e:
                if "503" in str(e):
                    time.sleep(2)
                else:
                    raise e

        # 4. Final fallback
        return "Server is busy right now. Please try again in a few seconds."

    except Exception as e:
        return f"Error: {str(e)}"