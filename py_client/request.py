import requests


endpoint = "http://localhost:8000/submit/"

data = {
    "name": "NewField",
    "content": "NOPE"
}

get_response = requests.post(endpoint, json=data)
print(get_response.json())


