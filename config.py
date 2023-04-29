from os import environ


class Config:
    MONGO_URI = environ.get("MONGO_URI")
    SECRET_KEY = environ.get("SECRET_KEY")
