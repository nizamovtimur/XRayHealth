# python -i test/test.py

import requests
from timeit import default_timer as timer

host = "https://xrayhealth.moad.dev"


def predict(token: str, file_path: str):
    start = timer()
    resp_normal = requests.post(host + "/analyzes/predict",
                                data={"patient_id": "1"},
                                files={"image": open(file_path, 'rb')},
                                headers={"Authorization": "Bearer " + token})
    print(resp_normal.json(), timer() - start)


def register(email: str, password: str):
    return requests.post(host + "/auth/register",
                         json={"email": email,
                               "password": password,
                               "name": "abc"}).json()


def login(email: str, password: str):
    return requests.post(host + "/auth/login",
                         json={"email": email,
                               "password": password}).json()


def get_analyzes(token: str):
    return requests.get(host + "/analyzes",
                        headers={"Authorization": "Bearer " + token}).json()


def get_analysis_by_id(token: str, analysis_id: str):
    return requests.get(host + f"/analyzes/{analysis_id}",
                        headers={"Authorization": "Bearer " + token}).json()


def delete_analysis_by_id(token: str, analysis_id: str):
    return requests.delete(host + f"/analyzes/{analysis_id}",
                           headers={"Authorization": "Bearer " + token}).json()
