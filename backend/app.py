from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import dlib
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load pretrained XceptionNet model
model = load_model("models/xception_deepfake.h5")
detector = dlib.get_frontal_face_detector()

def preprocess_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if len(faces) == 0:
        return None
    x, y, w, h = faces[0].left(), faces[0].top(), faces[0].width(), faces[0].height()
    face = img[y:y+h, x:x+w]
    face = cv2.resize(face, (299, 299))
    face = face.astype("float") / 255.0
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
        return jsonify({"error":"No file uploaded"}),400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    face = preprocess_face(img)
    if face is None:
        return jsonify({"error": "No face detected"}), 400
    
    pred = model.predict(face)[0][0]
    fake_score = float(pred)
    real_score = 1 - fake_score
    
    if fake_score > 0.5:
        status = "Fake Image"
        description = "Artifacts, unnatural textures, or facial misalignment detected."
        short_diff = "Fake: unnatural textures, artifacts"
    else:
        status = "Real Image"
        description = "Consistent facial features, natural textures, and lighting."
        short_diff = "Real: natural textures, aligned face"
    
    return jsonify({
        "status": status,
        "fake_score": round(fake_score*100,2),
        "real_score": round(real_score*100,2),
        "description": description,
        "short_diff": short_diff,
        "filepath": filepath
    })

if __name__ == "__main__":
    app.run(debug=True)
