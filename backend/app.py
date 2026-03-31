from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import dlib
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load model
model = load_model("models/xception_deepfake.h5")

# Face detector
detector = dlib.get_frontal_face_detector()


def preprocess_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) == 0:
        return None

    # Take first face
    f = faces[0]

    x, y, w, h = f.left(), f.top(), f.width(), f.height()

    # Safe crop
    h_img, w_img = img.shape[:2]
    x = max(0, x)
    y = max(0, y)
    w = min(w, w_img - x)
    h = min(h, h_img - y)

    face = img[y:y+h, x:x+w]

    face = cv2.resize(face, (299, 299))

    # Normalize (important)
    face = face / 127.5 - 1.0

    face = img_to_array(face)
    face = np.expand_dims(face, axis=0)

    return face


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['image']

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Unique filename
    filename = str(uuid.uuid4()) + ".jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(filepath)

    # Read image
    img = cv2.imread(filepath)

    face = preprocess_face(img)

    if face is None:
        return jsonify({"error": "No face detected"}), 400

    # Prediction
    pred = model.predict(face)[0][0]
    print("Prediction:", pred)

    fake_score = float(pred)
    real_score = 1 - fake_score

    if fake_score > 0.5:
        status = "Fake Image"
        short_diff = "Fake: artifacts, unnatural textures"
        description = "Detected inconsistencies in face texture, lighting mismatch, or blending artifacts."
    else:
        status = "Real Image"
        short_diff = "Real: natural texture, proper lighting"
        description = "Face shows natural texture, consistent lighting, and realistic alignment."

    return jsonify({
        "status": status,
        "fake_score": round(fake_score * 100, 2),
        "real_score": round(real_score * 100, 2),
        "short_diff": short_diff,
        "description": description,
        "image": filepath
    })


if __name__ == "__main__":
    app.run(debug=True)
