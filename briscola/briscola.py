from typing import List, Optional
from pydantic import BaseModel, Field
from .player import Player
from .deck import Deck, Card


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

    players: List[Player] = Field(default_factory=list)
    deck: Deck = Field(default_factory=Deck)
    briscola_card: Optional[Card] = None
    current_player_index: int = 0
    current_trick: List[Card] = Field(default_factory=list)
    tricks_played: int = 0

    class Config:
        arbitrary_types_allowed = True  # This allows the model to accept any type

    def __init__(self, player_names: List[str], **data):
        """
        Initializes a new game of Briscola.

        Params:
            player_names (List[str]): List of player names.
            **data: Additional data to initialize the game.

        Returns:
            None
        """
        super().__init__(**data)
        self.players = [Player(name=name) for name in player_names]
        self.deck = Deck()
        self.deal_initial_cards()
        self.briscola_card = self.deck.draw()

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

        print(f"\n{current_player.name}'s hand before playing:")
        print(", ".join([f"{c.rank} of {c.suit}" for c in current_player.hand]))

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
        Determines the winning card for the current trick based on the Briscola rules.

        The winning card is determined by these rules:
        1. If any Briscola cards are played, the highest value Briscola card wins.
        2. If no Briscola cards are played, the highest value card of the lead suit wins.
        3. If no cards of the lead suit or Briscola suit are played, the lead card wins.
        4. Cards are ranked by their point value, not by their face value.

        Returns:
            Card: The winning card for the trick.
        """
        lead_card = self.current_trick[0]
        lead_suit = lead_card.suit
        briscola_cards = [
            card for card in self.current_trick if card.suit == self.briscola_card.suit
        ]
        lead_suit_cards = [
            card for card in self.current_trick if card.suit == lead_suit
        ]

        print(f"\nDetermining winning card:")
        print(f"Lead card: {lead_card.rank} of {lead_card.suit}")
        print(f"Briscola suit: {self.briscola_card.suit}")
        print(
            f"Cards in trick: {', '.join([f'{card.rank} of {card.suit}' for card in self.current_trick])}"
        )
        print(
            f"Briscola cards in trick: {', '.join([f'{card.rank} of {card.suit}' for card in briscola_cards])}"
        )
        print(
            f"Lead suit cards in trick: {', '.join([f'{card.rank} of {card.suit}' for card in lead_suit_cards])}"
        )

        if briscola_cards:
            winning_card = max(
                briscola_cards,
                key=lambda card: (card.value, Deck.RANKS.index(card.rank)),
            )
            print(f"Briscola card wins: {winning_card.rank} of {winning_card.suit}")
            return winning_card
        elif lead_suit_cards:
            winning_card = max(
                lead_suit_cards,
                key=lambda card: (card.value, Deck.RANKS.index(card.rank)),
            )
            print(f"Lead suit card wins: {winning_card.rank} of {winning_card.suit}")
            return winning_card
        else:
            print(f"Lead card wins by default: {lead_card.rank} of {lead_card.suit}")
            return lead_card

    def replenish_hands(self) -> None:
        """
        Replenishes each player's hand with one card after a trick, if cards are available in the deck.
        """
        for player in self.players:
            if self.deck.cards:  # Check if there are cards left in the deck
                player.add_card(self.deck.draw())

        print("\nHands after replenishing:")
        for player in self.players:
            print(
                f"{player.name}'s hand: {', '.join([f'{card.rank} of {card.suit}' for card in player.hand])}"
            )

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
