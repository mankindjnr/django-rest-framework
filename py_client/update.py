import requests

endpoint = "http://127.0.0.1:8000/api/product/update/2/"

data = {
    "title": "This is a new title",
    "content": "This is a new content",
    "price": 9400.00
}
resp = requests.put(endpoint, json=data)
print(resp.json())
print(resp.status_code)