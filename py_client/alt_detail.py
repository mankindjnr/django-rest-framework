import requests

endpoint = "http://127.0.0.1:8000/api/product/alt/"
resp = requests.get(endpoint)
print(resp.json())
print(resp.status_code)