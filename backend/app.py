from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "API Working 🚀"})

@app.route("/detect", methods=["POST"])
def detect():
    return jsonify({"result": "FAKE", "confidence": 95})
