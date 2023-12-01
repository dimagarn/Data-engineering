import json
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/10")
print(response.json())
