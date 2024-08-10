from typing import List, Optional
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
        self.players = [Player(name=name) for name in player_names]
        self.deck = Deck()
        self.deal_initial_cards()
        self.set_briscola()

    def set_briscola(self):
        """Sets the Briscola card and places it at the bottom of the deck."""
        self.briscola_card = self.deck.draw()
        print(
            f"The Briscola card is: {self.briscola_card.rank} of {self.briscola_card.suit}"
        )
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
                print(f"{player.name} draws: {drawn_card.rank} of {drawn_card.suit}")
                if drawn_card == self.briscola_card:
                    print(
                        f"The Briscola card ({self.briscola_card.rank} of {self.briscola_card.suit}) has been drawn!"
                    )

    def play_turn(self, card: Card) -> None:
        """Handles the logic for a player playing a card."""
        current_player = self.get_current_player()
        played_card = current_player.play_card(card)
        self.current_trick.append(played_card)
        print(f"{current_player.name} played: {played_card.rank} of {played_card.suit}")

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

        print(
            f"\n{winning_player.name} wins the trick! Points: +{trick_points}. Total score: {winning_player.score}"
        )

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

    def get_game_state(self) -> dict:
        """Provides a summary of the current game state."""
        return {
            "current_player": self.get_current_player().name,
            "briscola_card": f"{self.briscola_card.rank} of {self.briscola_card.suit}",
            "tricks_played": self.tricks_played,
            "cards_left_in_deck": len(self.deck.cards),
            "current_trick": [
                {"rank": card.rank, "suit": card.suit} for card in self.current_trick
            ],
            "players": [
                {
                    "name": player.name,
                    "score": player.score,
                    "hand_size": player.get_hand_size(),
                }
                for player in self.players
            ],
        }
    
    def get_winner(self) -> Optional[Player]:
        """
        Determines the winner of the game based on the highest score.
        Returns None if the game is not over or if there's a tie.

        Returns:
            Optional[Player]: The player with the highest score, or None if the game isn't over or there's a tie.
        """
        if not self.is_game_over():
            return None
        
        max_score = max(player.score for player in self.players)
        winners = [player for player in self.players if player.score == max_score]
        
        if len(winners) == 1:
            return winners[0]
        else:
            print("The game ended in a tie!")
            return None
