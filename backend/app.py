from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "API Working 🚀"})

@app.route("/detect")
def detect():
    return jsonify({"result": "FAKE", "confidence": 95})

if __name__ == "__main__":
    app.run()
