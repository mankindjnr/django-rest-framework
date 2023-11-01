import requests

endpoint = "http://127.0.0.1:8000/api/"
resp = requests.post(endpoint, params={"NJORO": 940}, json={"title": "hellow mankind"})
print(resp.json())
print(resp.status_code)