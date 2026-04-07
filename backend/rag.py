import os
import pickle
import time
from google import genai

# ==============================
# 🔑 API SETUP
# ==============================
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)

# ==============================
# 📦 LOAD DATA
# ==============================
if not os.path.exists("vectorstore/chunks.pkl"):
    import ingest
    ingest.main()

with open("vectorstore/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# ==============================
# 🔍 IMPROVED SEARCH
# ==============================
def search_chunks(question):
    q = question.lower()

    synonyms = {
        "fee": ["cost", "price", "registration"],
        "domain": ["field", "track"],
        "team": ["duo", "trio", "group"],
        "prize": ["reward", "winnings", "cash"],
        "ai": ["agentic ai"],
        "hacking": ["ethical hacking", "cybersecurity"],
        "data": ["data analytics"],
        "design": ["ui ux"]
    }

    words = set(q.split())
    expanded = set(words)

    # expand query
    for word in words:
        if word in synonyms:
            expanded.update(synonyms[word])

    scored = []

    for chunk in chunks:
        chunk_lower = chunk.lower()

        score = 0
        for word in expanded:
            if word in chunk_lower:
                score += 1

        # boost exact phrase matches
        if q in chunk_lower:
            score += 5

        if score > 0:
            scored.append((score, chunk))

    scored.sort(reverse=True)

    return [chunk for _, chunk in scored[:5]]

# ==============================
# ⚡ SMART QUICK ANSWERS
# ==============================
def quick_answer(question):
    q = question.lower()

    # Fee (strict)
    if "fee" in q or ("cost" in q and "event" in q):
        return "The registration fee is ₹369 per head."

    # Prize
    if "prize" in q:
        return "The total prize pool is ₹30,000."

    # Dates
    if "date" in q or "when" in q:
        return "The event will be held on 10th and 11th April."

    # Team
    if any(x in q for x in ["team", "duo", "trio"]):
        return "You can register as solo, duo, or trio. The fee is ₹369 per person."

    # Domains ONLY if explicitly asked
    if "all domains" in q or "list domains" in q or "what domains" in q:
        return "The domains are App Dev, Web Dev, Agentic AI, Ethical Hacking, Data Analytics, and UI/UX."

    return None

# ==============================
# 🤖 MAIN FUNCTION
# ==============================
def get_answer(question: str) -> str:
    try:
        q = question.lower()

        # 1. Try quick answers
        fast = quick_answer(q)
        if fast:
            return fast

        # 2. Retrieve context
        relevant_chunks = search_chunks(q)

        if not relevant_chunks:
            return "I don't have that information right now. Please contact us at ciemlrit@mlrit.ac.in"

        context = "\n\n".join(relevant_chunks)

        prompt = f"""
You are an assistant for Workshop Carnival 2.0 (MLRIT-CIE).

Rules:
- Answer clearly and briefly
- No markdown (*, **)
- Use ONLY given context
- Be helpful and natural

Context:
{context}

Question: {question}

Answer:
"""

        # 3. Retry for API issues
        for _ in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                answer = response.text.replace("*", "").strip()

                if not answer:
                    return "I couldn't find a clear answer. Please try rephrasing."

                return answer

            except Exception as e:
                if "503" in str(e):
                    time.sleep(2)
                else:
                    raise e

        return "Server is busy right now. Please try again."

    except Exception as e:
        return f"Error: {str(e)}"