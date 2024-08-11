from flask import Flask, jsonify, request
from json import JSONEncoder
import sys
import os
from uuid import uuid4

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from briscola import BriscolaGame, Player, Card

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Player):
            return {
                "name": obj.name,
                "team": obj.team,
                "score": obj.score,
                "hand_size": obj.get_hand_size()
            }
        elif isinstance(obj, BriscolaGame):
            return {
                "players": obj.players,
                "current_player": obj.get_current_player().name if obj.get_current_player() else None,
                "briscola_card": obj.briscola_card.to_dict() if obj.briscola_card else None,
                "tricks_played": obj.tricks_played,
                "cards_left_in_deck": len(obj.deck.cards)
            }
        elif isinstance(obj, Card):
            return obj.to_dict()
        return super().default(obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

# In-memory storage for our games
games = {}

@app.route('/api/hello', methods=['GET'])
def hello_world():
    """A simple endpoint to test our API."""
    return jsonify({"message": "Hello, Briscola World!"})

@app.route('/api/games', methods=['GET', 'POST'])
def handle_games():
    if request.method == 'POST':
        return create_game()
    else:  # GET request
        return list_games()

def create_game():
    """Create a new Briscola game."""
    data = request.get_json()
    
    if not data or 'players' not in data:
        return jsonify({"error": "Players data is required"}), 400
    
    players = data['players']
    
    if not isinstance(players, list) or len(players) not in [2, 4]:
        return jsonify({"error": "Invalid number of players. Must be 2 or 4."}), 400

    game_id = str(uuid4())  # Generate a unique ID for the game
    game = BriscolaGame(players)
    games[game_id] = game

    return jsonify({
        "game_id": game_id,
        "message": "Game created successfully",
        "initial_state": game.get_game_state()
    }), 201

def list_games():
    """List all current games."""
    game_list = [{"game_id": game_id, "game": game} for game_id, game in games.items()]
    return jsonify({"message": "List of current games", "games": game_list})

@app.route('/api/games/<game_id>/join', methods=['POST'])
def join_game(game_id):
    """Allow a player to join an existing game."""
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    game = games[game_id]
    data = request.get_json()

    if not data or 'player' not in data:
        return jsonify({"error": "Player name is required"}), 400

    player_name = data['player']

    # Check if the game is already full
    if len(game.players) >= 4:
        return jsonify({"error": "Game is already full"}), 400

    # Check if the player is already in the game
    if player_name in [p.name for p in game.players]:
        return jsonify({"error": "Player is already in the game"}), 400

    # Add the player to the game
    new_player = Player(name=player_name, team=len(game.players) % 2 + 1)
    game.add_player(new_player)

    return jsonify({
        "message": f"Player {player_name} joined the game successfully",
        "game_state": game.get_game_state()
    }), 200

if __name__ == '__main__':
    app.run(debug=True)