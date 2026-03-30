from flask import Flask, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Load your knowledge base (simple text)
with open("data/workshop_data.txt", "r", encoding="utf-8") as f:
    KNOWLEDGE = f.read()


@app.route("/")
def home():
    return {"status": "Flask Gemini chatbot running"}


@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("question", "")

        prompt = f"""
You are a helpful assistant for Workshop Carnival 2.0 (MLRIT-CIE).

Answer ONLY using the information below.
If not found, say:
"I don't have that information right now. Please contact ciemlrit@mlrit.ac.in"

DATA:
{KNOWLEDGE}

QUESTION:
{user_input}

ANSWER:
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return jsonify({"answer": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)