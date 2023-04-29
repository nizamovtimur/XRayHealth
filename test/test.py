# python -i test/test.py

import requests
from timeit import default_timer as timer


def predict(file_path: str, token: str):
    start = timer()
    resp_normal = requests.post("http://localhost:5000/analyzes/predict",
                                data={"patient_id": "1"},
                                files={"image": open(file_path, 'rb')},
                                headers={"Authorization": "Bearer " + token})
    print(resp_normal.json(), timer() - start)


def register(email: str, password: str):
    return requests.post("http://localhost:5000/auth/register",
                         json={"email": email,
                               "password": password,
                               "name": "abc"})


def login(email: str, password: str):
    return requests.post("http://localhost:5000/auth/login",
                         json={"email": email,
                               "password": password})


def get_analyzes(token: str):
    return requests.get("http://localhost:5000/analyzes",
                        headers={"Authorization": "Bearer " + token})


def get_analysis_by_id(token: str, analysis_id: str):
    return requests.get(f"http://localhost:5000/analyzes/{analysis_id}",
                        headers={"Authorization": "Bearer " + token})


def delete_analysis_by_id(token: str, analysis_id: str):
    return requests.delete(f"http://localhost:5000/analyzes/{analysis_id}",
                           headers={"Authorization": "Bearer " + token})
