from os import environ


class Config:
    MONGO_URI = environ.get("MONGO_URI")
