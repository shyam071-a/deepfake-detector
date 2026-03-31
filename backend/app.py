from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

# Load real trained model (IMPORTANT)
model = load_model("model/model.h5")

def preprocess(img):
    img = cv2.resize(img, (224,224))
    img = img / 255.0
    img = np.reshape(img, (1,224,224,3))
    return img

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    ext = file.filename.split('.')[-1].lower()

    # IMAGE DETECTION
    if ext in ['jpg','jpeg','png']:
        img = cv2.imread(filepath)
        img = preprocess(img)

        pred = model.predict(img)[0][0]

        fake_score = float(pred)
        real_score = 1 - fake_score

        if fake_score > 0.5:
            status = "FAKE"
            short = "Unnatural texture & artifacts"
            desc = "Image shows inconsistencies in lighting and facial texture."
        else:
            status = "REAL"
            short = "Natural texture & lighting"
            desc = "Image has consistent lighting and natural facial details."

    # AUDIO (basic demo logic)
    elif ext in ['mp3','wav']:
        status = "CHECKED (Audio)"
        fake_score = 50
        real_score = 50
        short = "Audio analysis basic"
        desc = "Advanced model required for audio deepfake detection."

    # VIDEO (basic demo logic)
    elif ext in ['mp4','avi']:
        status = "CHECKED (Video)"
        fake_score = 50
        real_score = 50
        short = "Frame-based detection"
        desc = "Video frames need deep analysis using CNN+LSTM."

    else:
        return jsonify({"error":"Unsupported file type"})

    return jsonify({
        "status": status,
        "fake": round(fake_score*100,2),
        "real": round(real_score*100,2),
        "short": short,
        "desc": desc,
        "file": filepath
    })

if __name__ == "__main__":
    app.run(debug=True)
