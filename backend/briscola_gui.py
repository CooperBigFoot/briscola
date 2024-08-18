import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict
from briscola import BriscolaGame, Card, Player


class BriscolaGUI:
    def __init__(self, master: tk.Tk, game: BriscolaGame):
        """
        Initialize the Briscola GUI.

        Args:
            master (tk.Tk): The root Tkinter window.
            game (BriscolaGame): The Briscola game instance.
        """
        self.master = master
        self.game = game
        self.master.title("Briscola")
        self.master.geometry("900x700")
        self.master.configure(bg="#f0f0f0")  # Light gray background

        self.setup_ui()

    def setup_ui(self):
        """Set up the main UI components."""
        self.info_frame = ttk.Frame(self.master, padding="10", relief="ridge")
        self.info_frame.pack(fill=tk.X, padx=10, pady=10)

        self.player_frames: Dict[str, ttk.Frame] = {}
        for player in self.game.players:
            frame = ttk.Frame(self.master, padding="10", relief="raised")
            frame.pack(fill=tk.X, padx=10, pady=5)
            self.player_frames[player.name] = frame

        self.action_frame = ttk.Frame(self.master, padding="10", relief="sunken")
        self.action_frame.pack(fill=tk.X, padx=10, pady=10)

        self.message_var = tk.StringVar()
        self.message_label = ttk.Label(
            self.master, textvariable=self.message_var, font=("Helvetica", 12)
        )
        self.message_label.pack(pady=10)

        self.update_ui()

    def update_ui(self):
        """Update the UI to reflect the current game state."""
        self.update_info_frame()
        self.update_player_frames()
        self.update_action_frame()

    def update_info_frame(self):
        """Update the information display."""
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        style = ttk.Style()
        style.configure("Info.TLabel", font=("Helvetica", 12))

        ttk.Label(
            self.info_frame,
            text=f"Current Player: {self.game.get_current_player().name}",
            style="Info.TLabel",
        ).pack(pady=2)
        ttk.Label(
            self.info_frame,
            text=f"Briscola: {self.game.briscola_card.rank} of {self.game.briscola_card.suit}",
            style="Info.TLabel",
        ).pack(pady=2)
        ttk.Label(
            self.info_frame,
            text=f"Tricks Played: {self.game.tricks_played}",
            style="Info.TLabel",
        ).pack(pady=2)
        ttk.Label(
            self.info_frame,
            text=f"Cards in Deck: {len(self.game.deck.cards)}",
            style="Info.TLabel",
        ).pack(pady=2)

    def update_player_frames(self):
        """Update the display of players' hands and scores."""
        for player in self.game.players:
            frame = self.player_frames[player.name]
            for widget in frame.winfo_children():
                widget.destroy()

            style = ttk.Style()
            style.configure("PlayerName.TLabel", font=("Helvetica", 14, "bold"))
            style.configure("PlayerCard.TButton", font=("Helvetica", 10))

            ttk.Label(
                frame,
                text=f"{player.name} (Score: {player.score})",
                style="PlayerName.TLabel",
            ).pack(pady=5)

            hand_frame = ttk.Frame(frame)
            hand_frame.pack()

            for card in player.hand:
                btn = ttk.Button(
                    hand_frame,
                    text=f"{card.rank} of {card.suit}",
                    command=lambda p=player, c=card: self.play_card(p, c),
                    style="PlayerCard.TButton",
                )
                btn.pack(side=tk.LEFT, padx=2)
                if player != self.game.get_current_player():
                    btn.state(["disabled"])

    def update_action_frame(self):
        """Update the action buttons and current trick display."""
        for widget in self.action_frame.winfo_children():
            widget.destroy()

        if self.game.is_game_over():
            winner = self.game.get_winner()
            style = ttk.Style()
            style.configure("GameOver.TLabel", font=("Helvetica", 16, "bold"))
            if isinstance(winner, Player):
                ttk.Label(
                    self.action_frame,
                    text=f"Game Over! Winner: {winner.name}",
                    style="GameOver.TLabel",
                ).pack(pady=10)
            elif isinstance(winner, int):
                ttk.Label(
                    self.action_frame,
                    text=f"Game Over! Winning Team: {winner}",
                    style="GameOver.TLabel",
                ).pack(pady=10)
            else:
                ttk.Label(
                    self.action_frame,
                    text="Game Over! It's a tie!",
                    style="GameOver.TLabel",
                ).pack(pady=10)
            ttk.Button(self.action_frame, text="New Game", command=self.new_game).pack(
                pady=5
            )
        else:
            style = ttk.Style()
            style.configure("CurrentTrick.TLabel", font=("Helvetica", 12))
            ttk.Label(
                self.action_frame, text="Current Trick:", style="CurrentTrick.TLabel"
            ).pack(pady=5)
            for card in self.game.current_trick:
                ttk.Label(
                    self.action_frame,
                    text=f"{card.rank} of {card.suit}",
                    style="CurrentTrick.TLabel",
                ).pack()

    def play_card(self, player: Player, card: Card):
        """
        Handle the action of playing a card.

        Args:
            player (Player): The player playing the card.
            card (Card): The card being played.
        """
        if player == self.game.get_current_player():
            self.game.play_turn(card)
            self.update_ui()

            # Automatically play for other players if it's a 2-player game
            if len(self.game.players) == 2 and not self.game.is_game_over():
                other_player = [p for p in self.game.players if p != player][0]
                if other_player.hand:
                    auto_card = other_player.hand[0]  # Play the first card in hand
                    self.game.play_turn(auto_card)
                    self.message_var.set(
                        f"{other_player.name} played {auto_card.rank} of {auto_card.suit}"
                    )
                    self.master.after(3000, self.clear_message)
                self.update_ui()

    def clear_message(self):
        """Clear the message display."""
        self.message_var.set("")

    def new_game(self):
        """Start a new game."""
        player_names = [player.name for player in self.game.players]
        self.game = BriscolaGame(player_names)
        self.message_var.set("New game started!")
        self.master.after(3000, self.clear_message)  
        self.update_ui()


def main():
    root = tk.Tk()
    game = BriscolaGame(["Player 1", "Player 2", "Player 3", "Player 4"])
    BriscolaGUI(root, game)
    root.mainloop()


if __name__ == "__main__":
    main()
