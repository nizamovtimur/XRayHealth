from datetime import datetime
from base64 import b64encode

from config import Config
from neuralnet.basenet import BaseNet
from neuralnet.predict import get_prediction

import jwt
import torch
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from auth_middleware import token_required
from models import Analysis, User
from validate import validate_analyze, validate_email_and_password, validate_user

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r'/*': {'origins': '*'}})

basenet = BaseNet()
basenet.load_state_dict(torch.load("neuralnet/weights.pth", map_location=torch.device("cpu")))


@app.route("/", methods=["GET"])  # заглавная страница проекта с сочной кнопкой перехода к анализам
def index():
    return jsonify({
        "message": "Hello world",
        "data": "pong"
    }), 200


@app.route("/api", methods=["GET"])  # страница описания подключения аппаратного комплекса с токеном доступа
@token_required
def personal(current_user):
    pass


@app.route("/analyzes", methods=["GET"])  # список всех анализов всех пользователей
@token_required
def get_analyzes(current_user):
    try:
        analyzes = Analysis().get_all()
        return jsonify({
            "message": "Successfully retrieved all analyzes",
            "data": analyzes
        })
    except Exception as e:
        return jsonify({
            "message": "Failed to retrieve all analyzes",
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
                "message": "Требуется изображение",
                "data": None,
                "error": "Bad Request"
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
        analysis["prediction"] = get_prediction(image_bytes=analysis["image_bytes"], model=basenet)
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
            "message": "Successfully created a new analysis",
            "data": analysis
        }), 201
    except Exception as e:
        return jsonify({
            "message": "Failed to create a new analysis",
            "error": str(e),
            "data": None
        }), 500


@app.route("/analyzes/<analysis_id>", methods=["GET", "DELETE"])  # страница просмотра анализа GET и его удаления DELETE
@token_required
def get_analysis(current_user, analysis_id=""):
    print(analysis_id)
    if request.method == "GET":
        try:
            analysis = Analysis().get_by_id(analysis_id)
            if not analysis:
                return {
                    "message": "Анализ не найден",
                    "data": None,
                    "error": "Not Found"
                }, 404
            return jsonify({
                "message": "Successfully retrieved an analysis",
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
                    "message": "Анализ не найден",
                    "data": None,
                    "error": "Not Found"
                }, 404
            return jsonify({
                "message": "Successfully deleted an analysis"
            })
        except Exception as e:
            return jsonify({
                "message": "Something went wrong",
                "error": str(e),
                "data": None
            }), 500


@app.route("/auth/login", methods=["POST"])  # логин
def login():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        is_validated = validate_email_and_password(data.get('email'), data.get('password'))
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        user = User().login(
            data["email"],
            data["password"]
        )
        if user:
            try:
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


@app.route("/auth/register", methods=["POST"])  # регистрация
def register():
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
                "message": "Пользователь уже существует",
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
