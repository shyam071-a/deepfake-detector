from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "API Working 🚀"})

@app.route("/detect", methods=["POST"])
def detect():
    return jsonify({"result": "FAKE", "confidence": 95})
