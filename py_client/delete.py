import requests

endpoint = "http://127.0.0.1:8000/api/product/delete/14/"
resp = requests.delete(endpoint)
print(resp.status_code)