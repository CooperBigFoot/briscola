from typing import List, Optional
from pydantic import BaseModel, Field
from .deck import Card


class Player(BaseModel):
    name: str
    hand: List[Card] = Field(default_factory=list)
    score: int = 0
    team: Optional[int] = None
    is_ai: bool = False

    def play_card(self, card: Card) -> Card:
        """Remove and return the specified card from the player's hand."""
        if card in self.hand:
            self.hand.remove(card)
            return card
        raise ValueError("Card not in player's hand")

    def add_card(self, card: Card) -> None:
        """Add a card to the player's hand."""
        self.hand.append(card)

    def add_to_score(self, points: int) -> None:
        """Add points to the player's score."""
        self.score += points

    def get_hand_size(self) -> int:
        """Return the number of cards in the player's hand."""
        return len(self.hand)

    def has_briscola(self, briscola_suit: str) -> bool:
        """Check if the player has any briscola cards."""
        return any(card.suit == briscola_suit for card in self.hand)

    def get_playable_cards(self, lead_suit: Optional[str] = None) -> List[Card]:
        """
        Return a list of cards that can be played.
        In Briscola, all cards are playable, but this method can be used for strategy.
        """
        return self.hand.copy()
