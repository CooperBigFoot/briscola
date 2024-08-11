import requests
import json

# First, create a game
create_url = "http://127.0.0.1:5000/api/games"
create_data = {"players": ["Player1"]}

create_response = requests.post(create_url, json=create_data)
create_result = create_response.json()
game_id = create_result["game_id"]

print("Game created:")
print(json.dumps(create_result, indent=2))

# Now, join the game
join_url = f"http://127.0.0.1:5000/api/games/{game_id}/join"
join_data = {"player": "Player2"}

join_response = requests.post(join_url, json=join_data)

print("\nJoin game result:")
print("Status Code:", join_response.status_code)
print("Response:")
print(json.dumps(join_response.json(), indent=2))
