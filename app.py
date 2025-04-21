from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

# ✅ Use env variable or paste your API key here
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyCz-iB1TpgTcj_1DVIcG69pJLGoPNFwGHA"))

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction=(
        "You are a travel assistant. Ask questions to understand the user's preferences one at a time, "
        "then generate a table itinerary in markdown with 3 columns (morning, afternoon, night)."
    )
)
chat = model.start_chat(history=[])

app = Flask(__name__)
CORS(app)  # allow frontend to access backend

@app.route("/", methods=["GET"])
def root():
    return "✅ Gemini Travel Assistant backend running!"

@app.route("/chat", methods=["POST"])
def chat_api():
    try:
        data = request.get_json()
        user_input = data.get("message", "")
        if not user_input:
            return jsonify({"reply": "⚠️ No message received"}), 400

        response = chat.send_message(user_input)
        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
