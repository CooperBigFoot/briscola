from typing import List, Optional
from pydantic import BaseModel
from player import Player
from deck import Deck, Card


class BriscolaGame(BaseModel):
    """
    Manages the game logic for Briscola, including handling player turns,
    resolving tricks, and tracking the game state.

    Attributes:
        players (List[Player]): The list of players in the game.
        deck (Deck): The deck of cards used in the game.
        briscola_card (Card): The card determining the trump suit (briscola).
        current_player_index (int): The index of the player whose turn it is.
        current_trick (List[Card]): The cards currently played in the trick.
        tricks_played (int): The number of tricks that have been played.
    """

    players: List[Player]
    deck: Deck
    briscola_card: Card
    current_player_index: int = 0
    current_trick: List[Card] = []
    tricks_played: int = 0

    class Config:
        arbitrary_types_allowed = True  # This allows the model to accept any type

    def __init__(self, player_names: List[str]):
        """
        Initializes a new game of Briscola.

        Params:
            player_names (List[str]): List of player names.

        Returns:
            None
        """
        self.deck = Deck()
        self.players = [Player(name=name) for name in player_names]
        self.deal_initial_cards()
        self.briscola_card = self.deck.draw()
        self.current_player_index = 0

    def deal_initial_cards(self):
        """
        Deals the initial three cards to each player.

        Params:
            None

        Returns:
            None
        """
        for _ in range(3):
            for player in self.players:
                player.add_card(self.deck.draw())

    def play_turn(self, card: Card) -> None:
        """
        Handles the logic for a player playing a card.

        Params:
            card (Card): The card to be played by the current player.

        Returns:
            None
        """
        current_player = self.players[self.current_player_index]
        played_card = current_player.play_card(card)
        self.current_trick.append(played_card)

        if len(self.current_trick) == len(self.players):
            self.resolve_trick()
        else:
            self.current_player_index = (self.current_player_index + 1) % len(
                self.players
            )

    def resolve_trick(self) -> None:
        """
        Resolves the current trick by determining the winner, updating scores,
        and preparing for the next trick. Handles team scoring if applicable.

        This method:
        1. Determines the winning card and player
        2. Updates the score for the winning player or team
        3. Sets the next player to the trick winner
        4. Replenishes players' hands
        5. Resets the current trick and increments the tricks played counter

        Params:
            None

        Returns:
            None
        """
        winning_card = self.determine_winning_card()
        winning_player = self.players[self.current_trick.index(winning_card)]
        trick_points = sum(card.value for card in self.current_trick)

        if winning_player.team is not None:
            # Add points to the team's score
            for player in self.players:
                if player.team == winning_player.team:
                    player.add_to_score(trick_points)
        else:
            # Add points to the individual player's score
            winning_player.add_to_score(trick_points)

        self.current_player_index = self.players.index(winning_player)
        self.replenish_hands()
        self.current_trick = []
        self.tricks_played += 1

    def determine_winning_card(self) -> Card:
        """
        Determines the winning card for the current trick based on the briscola suit
        and the lead suit.

        Params:
            None

        Returns:
            Card: The winning card for the trick.
        """
        lead_suit = self.current_trick[0].suit
        briscola_cards = [
            card for card in self.current_trick if card.suit == self.briscola_card.suit
        ]

        if briscola_cards:
            return max(briscola_cards, key=lambda card: card.value)
        else:
            lead_cards = [card for card in self.current_trick if card.suit == lead_suit]
            return max(lead_cards, key=lambda card: card.value)

    def replenish_hands(self) -> None:
        """
        Replenishes each player's hand by drawing cards from the deck until
        each player has three cards. The replenishment is done clockwise,
        starting from the winner of the last trick.

        This method:
        1. Determines the starting player (winner of the last trick)
        2. Iterates through players in clockwise order
        3. Adds cards to each player's hand if needed and if cards are available in the deck

        Params:
            None

        Returns:
            None
        """
        start_index = self.current_player_index
        for i in range(len(self.players)):
            player_index = (start_index + i) % len(self.players)
            player = self.players[player_index]
            while len(player.hand) < 3 and len(self.deck.cards) > 0:
                player.add_card(self.deck.draw())

    def is_game_over(self) -> bool:
        """
        Checks if the game is over by determining if the required number of
        tricks have been played.

        Params:
            None

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self.tricks_played == 40 // len(self.players)

    def get_winner(self) -> Optional[Player]:
        """
        Determines the winner of the game based on the highest score.

        Params:
            None

        Returns:
            Optional[Player]: The player with the highest score, or None if the game is not over.
        """
        if not self.is_game_over():
            return None
        return max(self.players, key=lambda player: player.score)

    def get_current_player(self) -> Player:
        """
        Returns the player whose turn it is to play.

        Params:
            None

        Returns:
            Player: The current player.
        """
        return self.players[self.current_player_index]

    def get_game_state(self) -> dict:
        """
        Provides a summary of the current game state, including the current player,
        briscola suit, number of tricks played, and the players' scores and hands.

        Params:
            None

        Returns:
            dict: A dictionary containing the current game state.
        """
        return {
            "current_player": self.get_current_player().name,
            "briscola_suit": self.briscola_card.suit,
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
