import os
from flask import Flask, request, render_template, jsonify
import google.generativeai as genai

app = Flask(__name__)
API_KEY = os.environ.get("GEMINI_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-2.0-flash"
SYSTEM_PROMPT = (
    "You are Exam Buddy, an AI study assistant for students preparing for "
    "competitive government/PSU exams in India. When given a topic or "
    "question, respond with: 1) A clear, exam-focused explanation. "
    "2) A short memory trick. 3) One practice question with the answer."
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    question = (data.get("question") or "").strip()
    if not question:
        return jsonify({"error": "Please enter a topic or question."}), 400
    if not API_KEY:
        return jsonify({"error": "Server missing GEMINI_API_KEY."}), 500
    try:
        model = genai.GenerativeModel(model_name=MODEL_NAME, system_instruction=SYSTEM_PROMPT)
        response = model.generate_content(question)
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/healthz")
def healthz():
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
