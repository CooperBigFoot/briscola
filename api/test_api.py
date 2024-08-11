import requests
import json

url = "http://127.0.0.1:5000/api/games"
data = {
    "players": ["Player1", "Player2"]
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:")
print(json.dumps(response.json(), indent=2))