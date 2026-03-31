from flask import Flask, request, jsonify
import cv2, numpy as np, os
from tensorflow.keras.models import load_model

app = Flask(__name__)
model = load_model("model.h5")

def preprocess(img):
    img = cv2.resize(img, (224,224))
    img = img/255.0
    return np.reshape(img,(1,224,224,3))

@app.route("/detect", methods=["POST"])
def detect():
    file = request.files["file"]
    path = "temp.jpg"
    file.save(path)

    img = cv2.imread(path)
    img = preprocess(img)
    pred = model.predict(img)[0][0]

    os.remove(path)

    if pred > 0.5:
        return jsonify({"result":"FAKE","confidence":float(pred*100)})
    else:
        return jsonify({"result":"REAL","confidence":float((1-pred)*100)})

if __name__ == "__main__":
    app.run(debug=True)
