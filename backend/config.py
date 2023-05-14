from os import environ

from dotenv import load_dotenv
load_dotenv()


class Config:
    MONGO_URI = environ.get("MONGO_URI") or "mongodb://localhost:27017/xrayhealth"
    SECRET_KEY = environ.get("SECRET_KEY") or "secret"
