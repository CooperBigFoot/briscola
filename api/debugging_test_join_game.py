import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"


def print_response(response):
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    print(json.dumps(dict(response.headers), indent=2))
    print("Content:")
    try:
        print(json.dumps(response.json(), indent=2))
    except json.JSONDecodeError:
        print(response.text)
    print("-" * 50)


# Test the hello endpoint
print("Testing /api/hello endpoint:")
hello_response = requests.get(f"{BASE_URL}/hello")
print_response(hello_response)

# Create a game
print("\nCreating a new game:")
create_data = {"players": ["Player1", "Player2"]}
create_response = requests.post(f"{BASE_URL}/games", json=create_data)
print_response(create_response)

if create_response.status_code == 201:
    game_data = create_response.json()
    game_id = game_data.get("game_id")

    if game_id:
        # Join the game
        print(f"\nJoining the game (ID: {game_id}):")
        join_data = {"player": "Player3"}
        join_response = requests.post(
            f"{BASE_URL}/games/{game_id}/join", json=join_data
        )
        print_response(join_response)

        # List all games
        print("\nListing all games:")
        list_response = requests.get(f"{BASE_URL}/games")
        print_response(list_response)
    else:
        print("Error: No game_id in the response")
else:
    print("Error: Failed to create game")

print("Debugging script completed.")
