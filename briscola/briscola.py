from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from .player import Player
from .deck import Deck, Card


class BriscolaGame(BaseModel):
    players: List[Player] = Field(default_factory=list)
    deck: Deck = Field(default_factory=Deck)
    briscola_card: Optional[Card] = None
    current_player_index: int = 0
    current_trick: List[Card] = Field(default_factory=list)
    tricks_played: int = 0

    def __init__(self, player_names: List[str], **data):
        super().__init__(**data)
        if len(player_names) not in [2, 4]:
            raise ValueError("Briscola requires either 2 or 4 players")
        self.players = [
            Player(name=name, team=(i % 2) + 1) for i, name in enumerate(player_names)
        ]
        self.deck = Deck()
        self.deal_initial_cards()
        self.set_briscola()

    def add_player(self, player: Player) -> None:
        """Adds a player to the game."""
        if len(self.players) < 4:
            self.players.append(player)
            if len(self.players) == 1:
                self.deal_initial_cards()
                self.set_briscola()

    def set_briscola(self):
        """Sets the Briscola card and places it at the bottom of the deck."""
        self.briscola_card = self.deck.draw()
        self.deck.cards.insert(0, self.briscola_card)

    def deal_initial_cards(self):
        """Deals the initial three cards to each player."""
        for _ in range(3):
            for player in self.players:
                player.add_card(self.deck.draw())

    def replenish_hands(self) -> None:
        """
        Replenishes each player's hand with one card after a trick,
        if cards are available. The winning player draws first, followed
        by others in clockwise order. The last card to be drawn is the Briscola card.
        """
        players_to_draw = (
            self.players[self.current_player_index :]
            + self.players[: self.current_player_index]
        )

        for player in players_to_draw:
            if self.deck.cards:
                drawn_card = self.deck.draw()
                player.add_card(drawn_card)

    def play_turn(self, card: Card) -> None:
        """Handles the logic for a player playing a card."""
        current_player = self.get_current_player()
        played_card = current_player.play_card(card)
        self.current_trick.append(played_card)

        if len(self.current_trick) == len(self.players):
            self.resolve_trick()
        else:
            self.current_player_index = (self.current_player_index + 1) % len(
                self.players
            )

    def resolve_trick(self) -> None:
        """Resolves the current trick and updates game state."""
        winning_card = self.determine_winning_card()
        trick_points = sum(card.value for card in self.current_trick)
        winning_player = next(
            player for player in self.players if winning_card in player.played_cards
        )

        winning_player.add_to_score(trick_points)
        self.current_player_index = self.players.index(winning_player)

        self.tricks_played += 1
        if not self.is_game_over():
            self.replenish_hands()

        self.clear_played_cards()
        self.current_trick = []

    def determine_winning_card(self) -> Card:
        """Determines the winning card for the current trick based on Briscola rules."""
        lead_card = self.current_trick[0]
        briscola_cards = [
            card for card in self.current_trick if card.suit == self.briscola_card.suit
        ]
        lead_suit_cards = [
            card for card in self.current_trick if card.suit == lead_card.suit
        ]

        if briscola_cards:
            return max(
                briscola_cards,
                key=lambda card: (card.value, self.deck.RANKS.index(card.rank)),
            )
        elif lead_suit_cards:
            return max(
                lead_suit_cards,
                key=lambda card: (card.value, self.deck.RANKS.index(card.rank)),
            )
        else:
            return lead_card

    def is_game_over(self) -> bool:
        """Checks if the game is over."""
        return self.tricks_played == 40 // len(self.players)

    def get_current_player(self) -> Player:
        """Returns the current player."""
        return self.players[self.current_player_index]

    def clear_played_cards(self):
        """Clears the played cards for all players."""
        for player in self.players:
            player.played_cards.clear()

    def get_game_state(self) -> Dict:
        """Returns the current state of the game."""
        return {
            "players": [
                {
                    "name": player.name,
                    "team": player.team,
                    "score": player.score,
                    "hand_size": player.get_hand_size(),
                }
                for player in self.players
            ],
            "current_player": (
                self.get_current_player().name if self.get_current_player() else None
            ),
            "briscola_card": (
                self.briscola_card.to_dict() if self.briscola_card else None
            ),
            "current_trick": [card.to_dict() for card in self.current_trick],
            "tricks_played": self.tricks_played,
            "cards_left_in_deck": len(self.deck.cards),
        }

    def get_winner(self) -> Optional[Player | int]:
        """
        Determines the winner of the game based on the highest score.
        For 1v1 games, returns the winning Player.
        For 2v2 games, returns the winning team number.
        Returns None if the game is not over or if there's a tie.

        Returns:
            Optional[Player | int]: The winning Player (1v1) or team number (2v2), or None if the game isn't over or there's a tie.
        """
        if not self.is_game_over():
            return None

        if len(self.players) == 2:
            # 1v1 game
            if self.players[0].score > self.players[1].score:
                return self.players[0]
            elif self.players[1].score > self.players[0].score:
                return self.players[1]
            else:
                return None  # Tie
        else:
            # 2v2 game
            team_scores = {1: 0, 2: 0}
            for player in self.players:
                team_scores[player.team] += player.score

            if team_scores[1] > team_scores[2]:
                return 1
            elif team_scores[2] > team_scores[1]:
                return 2
            else:
                return None  # Tie
