from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

sys.path.append(os.path.dirname(__file__))

from agent import ask_asha

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/")
def index():
    return "Asha AI Bot Backend is Running 🚀"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_query = data.get("message", "")

        if not user_query:
            return jsonify({"error": "Message is required"}), 400

        response = ask_asha(user_query)
        return jsonify({"response": response})

    except Exception as e:
        print(f"[Backend Error] {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
