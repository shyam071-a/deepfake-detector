from flask import Flask, request, jsonify, send_from_directory
import os
import cv2
import numpy as np
import uuid
import librosa

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---------- IMAGE ----------
def detect_image(path):
    img = cv2.imread(path)
    if img is None:
        return "Error", 0

    val = np.mean(img)

    if val > 120:
        return "Real", 0.3
    else:
        return "Fake", 0.85

# ---------- VIDEO ----------
def detect_video(path):
    cap = cv2.VideoCapture(path)
    count = 0
    fake = 0

    while True:
        ret, frame = cap.read()
        if not ret or count > 15:
            break

        count += 1
        if np.mean(frame) < 100:
            fake += 1

    cap.release()

    prob = fake / max(count,1)

    if prob > 0.5:
        return "Fake", prob
    else:
        return "Real", prob

# ---------- AUDIO ----------
def detect_audio(path):
    try:
        y, sr = librosa.load(path)
        energy = np.mean(np.abs(y))

        if energy < 0.02:
            return "Fake", 0.8
        else:
            return "Real", 0.2
    except:
        return "Error", 0

# ---------- API ----------
@app.route("/detect", methods=["POST"])
def detect():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file"}), 400

    filename = str(uuid.uuid4()) + file.filename
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    ext = filename.split(".")[-1].lower()

    if ext in ["jpg","jpeg","png"]:
        result, prob = detect_image(path)
        type_ = "Image"

    elif ext in ["mp4","avi","mov"]:
        result, prob = detect_video(path)
        type_ = "Video"

    elif ext in ["wav","mp3"]:
        result, prob = detect_audio(path)
        type_ = "Audio"

    else:
        return jsonify({"error":"Unsupported file"}), 400

    return jsonify({
        "type": type_,
        "result": result,
        "confidence": round(prob*100,2)
    })

if __name__ == "__main__":
    app.run(debug=True)
