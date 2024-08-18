# File: main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from briscola import BriscolaGame, Player, Card 
import uuid

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# In-memory storage for active games
games = {}


class GameCreate(BaseModel):
    player_names: List[str]


class CardInfo(BaseModel):
    rank: str
    suit: str
    value: int


class PlayerInfo(BaseModel):
    name: str
    team: Optional[int]
    score: int
    hand_size: int


class GameState(BaseModel):
    game_id: str
    current_player: str
    briscola_card: CardInfo
    tricks_played: int
    cards_left_in_deck: int
    current_trick: List[CardInfo]
    players: List[PlayerInfo]


class CardPlay(BaseModel):
    rank: str
    suit: str


class PlayCard(BaseModel):
    player_name: str
    card: CardPlay


@app.post("/games", response_model=str)
async def create_game(game_create: GameCreate):
    """Create a new Briscola game."""
    game_id = str(uuid.uuid4())
    games[game_id] = BriscolaGame(game_create.player_names)
    return game_id


@app.get("/games/{game_id}", response_model=GameState)
async def get_game_state(game_id: str):
    """Get the current state of a game."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    game = games[game_id]
    game_state = game.get_game_state()
    return GameState(
        game_id=game_id,
        current_player=game_state["current_player"],
        briscola_card=CardInfo(**game_state["briscola_card"]),
        tricks_played=game_state["tricks_played"],
        cards_left_in_deck=game_state["cards_left_in_deck"],
        current_trick=[CardInfo(**card) for card in game_state["current_trick"]],
        players=[PlayerInfo(**player) for player in game_state["players"]],
    )


@app.post("/games/{game_id}/play")
async def play_card(game_id: str, play: PlayCard):
    """Play a card in the game."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    game = games[game_id]
    current_player = game.get_current_player()
    if current_player.name != play.player_name:
        raise HTTPException(status_code=400, detail="It's not your turn")

    card_to_play = next(
        (
            c
            for c in current_player.hand
            if c.rank == play.card.rank and c.suit == play.card.suit
        ),
        None,
    )
    if not card_to_play:
        raise HTTPException(status_code=400, detail=f"Invalid card, the valid cards are: {current_player.hand}")

    game.play_turn(card_to_play)
    return {"message": "Card played successfully"}


@app.get("/games/{game_id}/winner")
async def get_winner(game_id: str):
    """Get the winner of the game."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    game = games[game_id]
    winner = game.get_winner()
    if winner is None:
        return {"message": "Game is not over yet"}
    elif isinstance(winner, Player):
        return {"winner": winner.name}
    else:
        return {"winner": f"Team {winner}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
