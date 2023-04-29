import bson

from config import Config

from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
db = MongoClient(Config().MONGO_URI).xrayhealth


class Analysis:
    def __init__(self):
        return

    def create(self, image_bytes="", prediction="", patient_id="", date="", user_id=""):
        new_analysis = db.analyzes.insert_one(
            {
                "image_bytes": image_bytes,
                "prediction": prediction,
                "patient_id": patient_id,
                "date": date,
                "user_id": user_id
            }
        )
        return self.get_by_id(new_analysis.inserted_id)

    def get_all(self):
        analyzes = db.analyzes.find()
        return [{**analysis, "_id": str(analysis["_id"])} for analysis in analyzes]

    def get_by_id(self, analysis_id):
        analysis = db.analyzes.find_one({"_id": bson.ObjectId(analysis_id)})
        if not analysis:
            return
        analysis["_id"] = str(analysis["_id"])
        return analysis

    def get_by_user_id(self, user_id):
        analyzes = db.books.find({"user_id": user_id})
        return [{**analysis, "_id": str(analysis["_id"])} for analysis in analyzes]

    def get_by_prediction(self, prediction):
        analyzes = db.analyzes.find({"prediction": prediction})
        return [analysis for analysis in analyzes]

    def get_by_user_id_and_prediction(self, user_id, prediction):
        analyzes = db.books.find({"user_id": user_id, "prediction": prediction})
        return [{**analysis, "_id": str(analysis["_id"])} for analysis in analyzes]

    def delete(self, analysis_id):
        analysis = db.analyzes.delete_one({"_id": bson.ObjectId(analysis_id)})
        return analysis

    def delete_by_user_id(self, user_id):
        analysis = db.analyzes.delete_many({"user_id": bson.ObjectId(user_id)})
        return analysis


class User:
    def __init__(self):
        return

    def create(self, name="", email="", password=""):
        user = self.get_by_email(email)
        if user:
            return
        new_user = db.users.insert_one(
            {
                "name": name,
                "email": email,
                "password": generate_password_hash(password),
                "active": True
            }
        )
        return self.get_by_id(new_user.inserted_id)

    def get_all(self):
        users = db.users.find({"active": True})
        return [{**user, "_id": str(user["_id"])} for user in users]

    def get_by_id(self, user_id):
        user = db.users.find_one({"_id": bson.ObjectId(user_id), "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        user.pop("password")
        return user

    def get_by_email(self, email):
        user = db.users.find_one({"email": email, "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user

    def update(self, user_id, name=""):
        data = {}
        if name:
            data["name"] = name
        user = db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": data
            }
        )
        user = self.get_by_id(user_id)
        return user

    def delete(self, user_id):
        Analysis().delete_by_user_id(user_id)
        user = db.users.delete_one({"_id": bson.ObjectId(user_id)})
        user = self.get_by_id(user_id)
        return user

    def disable_account(self, user_id):
        user = db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {"$set": {"active": False}}
        )
        user = self.get_by_id(user_id)
        return user

    def login(self, email, password):
        user = self.get_by_email(email)
        if not user or not check_password_hash(user["password"], password):
            return
        user.pop("password")
        return user
