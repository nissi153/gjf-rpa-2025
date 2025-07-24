# RESTful API 기본 이해 및 요청
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
data = response.json()
print(data["title"])
