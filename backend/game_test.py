from typing import List
from briscola import BriscolaGame, Card


def print_game_state(game: BriscolaGame):
    """Print the current state of the game."""
    print(f"\nCurrent player: {game.get_current_player().name}")
    print(f"Briscola card: {game.briscola_card.rank} of {game.briscola_card.suit}")
    print(f"Tricks played: {game.tricks_played}")
    print(f"Cards left in deck: {len(game.deck.cards)}")
    print("\nCurrent trick:")
    for card in game.current_trick:
        print(f"  {card.rank} of {card.suit}")
    print("\nPlayers:")
    for player in game.players:
        print(
            f"  {player.name}: Score = {player.score}, Hand size = {player.get_hand_size()}"
        )


def print_player_hand(player_name: str, hand: List[Card]):
    """Print the cards in a player's hand."""
    print(f"\n{player_name}'s hand:")
    for i, card in enumerate(hand):
        print(f"  {i + 1}. {card.rank} of {card.suit}")


def get_card_choice(player_name: str, hand: List[Card]) -> Card:
    """Get the player's choice of card to play."""
    while True:
        try:
            choice = (
                int(input(f"{player_name}, choose a card to play (1-{len(hand)}): "))
                - 1
            )
            if 0 <= choice < len(hand):
                return hand[choice]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def play_game():
    """Run a test game of Briscola."""
    game = BriscolaGame(["Player 1", "Player 2"])

    while not game.is_game_over():
        print_game_state(game)
        current_player = game.get_current_player()

        if not current_player.hand:
            print(f"{current_player.name} has no cards left to play.")
            game.play_turn(None)  # Pass None to indicate no card can be played
        else:
            print_player_hand(current_player.name, current_player.hand)
            card_to_play = get_card_choice(current_player.name, current_player.hand)
            game.play_turn(card_to_play)

        input("Press Enter to continue...")

        if game.is_game_over():
            break

    winner = game.get_winner()
    print(f"\nGame over! The winner is {winner.name} with a score of {winner.score}.")


if __name__ == "__main__":
    play_game()
