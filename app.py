from datetime import datetime
from base64 import b64encode

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


@app.route("/", methods=["GET"])  # заглавная страница проекта с сочной кнопкой перехода к анализам
def index():
    return jsonify({
        "message": "Welcome to the project",
        "data": None
    })


@app.route("/analyzes", methods=["GET"])  # список всех анализов всех пользователей
@token_required
def get_analyzes(current_user):
    try:
        analyzes = Analysis().get_all()
        return jsonify({
            "message": "successfully retrieved all analyzes",
            "data": analyzes
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all analyzes",
            "error": str(e),
            "data": None
        }), 500


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
        analysis["image_bytes"] = b64encode(analysis["image_bytes"]).decode("utf-8")
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
def get_analysis(analysis_id, current_user):
    if request.method == "GET":
        try:
            analysis = Analysis().get_by_id(analysis_id)
            if not analysis:
                return {
                    "message": "Analysis not found",
                    "data": None,
                    "error": "Not Found"
                }, 404
            return jsonify({
                "message": "successfully retrieved an analysis",
                "data": analysis
            })
        except Exception as e:
            return jsonify({
                "message": "Something went wrong",
                "error": str(e),
                "data": None
            }), 500
    if request.method == "DELETE":
        try:
            analysis = Analysis().delete(analysis_id)
            if not analysis:
                return {
                    "message": "Analysis not found",
                    "data": None,
                    "error": "Not Found"
                }, 404
            return jsonify({
                "message": "successfully deleted an analysis",
                "data": analysis
            })
        except Exception as e:
            return jsonify({
                "message": "Something went wrong",
                "error": str(e),
                "data": None
            }), 500


@app.route("/api", methods=["GET"])  # страница описания подключения аппаратного комплекса с токеном доступа
@token_required
def personal(current_user):
    pass


@app.route("/auth/login", methods=["GET", "POST"])  # форма логина или редирект на /
def login():
    if request.method == "GET":
        return {
            "message": "This is a login form",
            "data": None
        }
    if request.method == "POST":
        try:
            data = request.json
            if not data:
                return {
                    "message": "Please provide user details",
                    "data": None,
                    "error": "Bad request"
                }, 400
            # validate input
            is_validated = validate_email_and_password(data.get('email'), data.get('password'))
            if is_validated is not True:
                return dict(message='Invalid data', data=None, error=is_validated), 400
            user = User().login(
                data["email"],
                data["password"]
            )
            if user:
                try:
                    # token should expire after 24 hrs
                    user["token"] = jwt.encode(
                        {"user_id": user["_id"]},
                        app.config["SECRET_KEY"],
                        algorithm="HS256"
                    )
                    return {
                        "message": "Successfully fetched auth token",
                        "data": user
                    }
                except Exception as e:
                    return {
                        "error": "Something went wrong",
                        "message": str(e)
                    }, 500
            return {
                "message": "Error fetching auth token!, invalid email or password",
                "data": None,
                "error": "Unauthorized"
            }, 404
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
            }, 500


@app.route("/auth/register", methods=["GET", "POST"])  # форма регистрации или редирект на /
def register():
    if request.method == "GET":
        return {
            "message": "This is a registration form",
            "data": None
        }
    if request.method == "POST":
        try:
            user = request.json
            if not user:
                return {
                    "message": "Please provide user details",
                    "data": None,
                    "error": "Bad request"
                }, 400
            is_validated = validate_user(**user)
            if is_validated is not True:
                return dict(message='Invalid data', data=None, error=is_validated), 400
            user = User().create(**user)
            if not user:
                return {
                    "message": "User already exists",
                    "error": "Conflict",
                    "data": None
                }, 409
            return {
                "message": "Successfully created new user",
                "data": user
            }, 201
        except Exception as e:
            return {
                "message": "Something went wrong",
                "error": str(e),
                "data": None
            }, 500


if __name__ == "__main__":
    app.run(debug=True)
