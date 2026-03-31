from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "API Working 🚀"})

@app.route("/detect", methods=["POST"])
def detect():
    try:
        print("API HIT 🔥")

        # check file
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Empty file"}), 400

        # TEMP response (AI later)
        return jsonify({
            "result": "FAKE",
            "confidence": 92
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
