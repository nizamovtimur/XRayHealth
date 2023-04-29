from datetime import datetime

from config import Config
from neuralnet.resnet import ResidualBlock, ResNet
from neuralnet.predict import get_prediction

import jwt
import torch
from flask import Flask, jsonify, request

from auth_middleware import token_required
from models import Analysis, User
from validate import validate_analyze, validate_email_and_password, validate_user

app = Flask(__name__)
app.config.from_object(Config)

model = ResNet(ResidualBlock, [3, 4, 6, 3])
model.load_state_dict(torch.load("neuralnet/weights.pth", map_location=torch.device("cpu")))


@app.route("/", methods=["GET"])  # список всех анализов всех пользователей
@token_required
def index():
    pass


@app.route("/analyzes/predict", methods=["POST"])  # создание анализа с предсказанием через api с проверкой токена
@token_required
def predict(current_user):
    try:
        analysis = dict(request.form)
        if not analysis:
            return {
                "message": "Invalid data, you need to give the image and patient_id",
                "data": None,
                "error": "Bad Request"
            }, 400
        if not request.files["image"]:
            return {
                "message": "image is required",
                "data": None
            }, 400
        analysis["image_bytes"] = request.files["image"].read()
        is_validated = validate_analyze(**analysis)
        if is_validated is not True:
            return {
                "message": "Invalid data",
                "data": None,
                "error": is_validated
            }, 400
        analysis["user_id"] = current_user["_id"]
        analysis["prediction"] = get_prediction(image_bytes=analysis["image_bytes"], model=model)
        analysis["date"] = datetime.now()
        analysis = Analysis().create(**analysis)
        if not analysis:
            return {
                "message": "The analysis is not created",
                "data": None,
                "error": "Conflict"
            }, 400
        return jsonify({
            "message": "successfully created a new analysis",
            "data": analysis
        }), 201
    except Exception as e:
        return jsonify({
            "message": "failed to create a new analysis",
            "error": str(e),
            "data": None
        }), 500


@app.route("/analyzes/<analysis_id>", methods=["GET", "DELETE"])  # страница просмотра анализа GET и его удаления DELETE
@token_required
def get_analysis(analysis_id):
    pass


@app.route("/api", methods=["GET"])  # страница описания подключения аппаратного комплекса с токеном доступа
@token_required
def personal():
    pass


@app.route("/login", methods=["GET", "POST"])  # форма логина или редирект на /
def login():
    pass


@app.route("/logout", methods=["POST"])  # редирект на /login
def logout():
    pass


@app.route("/register", methods=["GET", "POST"])  # форма регистрации или редирект на /
def register():
    pass


if __name__ == "__main__":
    app.run()
