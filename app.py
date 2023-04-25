from config import Config
from model.resnet import ResidualBlock, ResNet
from model.predict import get_prediction

import torch
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config.from_object(Config)

model = ResNet(ResidualBlock, [3, 4, 6, 3])
model.load_state_dict(torch.load("model/weights.pth", map_location=torch.device("cpu")))


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        file = request.files["file"]
        img_bytes = file.read()
        prediction = get_prediction(image_bytes=img_bytes, model=model)
        return jsonify({"result": prediction})


if __name__ == "__main__":
    app.run()
