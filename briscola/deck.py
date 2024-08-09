from typing import List
from pydantic import BaseModel
import random

class Card(BaseModel):
    """Represents a single card in the Neapolitan Briscola deck."""
    rank: str
    suit: str
    value: int

    class Config:
        frozen = True  # Makes the card immutable

class Deck:
    """Represents a deck of Neapolitan Briscola cards."""
    
    RANKS = ['Due', 'Quattro', 'Cinque', 'Sei', 'Sette', 'Fante', 'Cavallo', 'Re', 'Tre', 'Asso']
    SUITS = ['Denari', 'Spade', 'Coppe', 'Bastoni']
    VALUES = {
        'Due': 0, 'Quattro': 0, 'Cinque': 0, 'Sei': 0, 'Sette': 0,
        'Fante': 2, 'Cavallo': 3, 'Re': 4, 'Tre': 10, 'Asso': 11
    }

    def __init__(self):
        self.cards: List[Card] = [
            Card(rank=rank, suit=suit, value=self.VALUES[rank])
            for suit in self.SUITS
            for rank in self.RANKS
        ]
        self.shuffle()

    def shuffle(self) -> None:
        """Shuffles the deck of cards."""
        random.shuffle(self.cards)

    def draw(self) -> Card:
        """Draws a card from the top of the deck."""
        if not self.cards:
            raise ValueError("No cards left in the deck")
        return self.cards.pop()

    def __len__(self) -> int:
        """Returns the number of cards left in the deck."""
        return len(self.cards)