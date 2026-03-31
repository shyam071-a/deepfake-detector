from flask import Flask, request, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

app = Flask(__name__)

# Load pretrained XceptionNet Deepfake model
model = load_model("xception_deepfake.h5")  # pretrained weights

def preprocess_face(img):
    # Resize to 299x299 (XceptionNet input)
    img = cv2.resize(img, (299, 299))
    img = img.astype("float") / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return img

@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Preprocess image
    processed = preprocess_face(img)

    # Predict
    pred = model.predict(processed)[0][0]  # 0 = real, 1 = fake

    # Convert to percentage
    fake_score = float(pred)
    real_score = 1 - fake_score

    # Description based on probability
    if fake_score > 0.5:
        status = "Fake Image"
        description = "Face artifacts, unnatural textures, possible manipulation detected."
    else:
        status = "Real Image"
        description = "Natural facial features, lighting, and textures consistent."

    return jsonify({
        "status": status,
        "fake_score": round(fake_score*100,2),
        "real_score": round(real_score*100,2),
        "description": description
    })

if __name__ == "__main__":
    app.run(debug=True)
