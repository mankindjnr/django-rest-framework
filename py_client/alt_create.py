import requests

endpoint = "http://127.0.0.1:8000/api/product/alt/"

data = {
    "title": "A Product in create function view",
    "price": 123.45
}
resp = requests.post(endpoint, json=data)
print(resp.json())
print(resp.status_code)