import requests
from timeit import default_timer as timer


def test_predict(file_path: str):
    start = timer()
    resp_normal = requests.post("http://localhost:5000/predict",
                                files={"file": open(file_path, 'rb')})
    print(resp_normal.json(), timer() - start)


test_predict("normal.jpg")
test_predict("bacteria.jpg")
