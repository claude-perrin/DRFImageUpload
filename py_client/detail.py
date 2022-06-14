import requests


endpoint = "http://localhost:8000/submit/"



get_response = requests.get(endpoint)
print(get_response.json())


