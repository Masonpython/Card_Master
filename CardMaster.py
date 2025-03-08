import tkinter as tk
from tkinter import messagebox
import sys

def quit_game():
    sys.exit()

class Player:
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards

    def get_card_value(self, card):
        return self.cards[card]

    def get_sum(self, card1, card2):
        return self.get_card_value(card1) + self.get_card_value(card2)

def validate_selection(cards):
    if len(cards) != 4:
        return False
    if len(set(cards)) != 4:
        return False
    if sum(cards) != 30:
        return False
    return True

class CardGameGUI:
    def __init__(self, root):
        self.flag = 1
        self.root = root
        self.root.title("Two-Player Card Game")
        self.root.geometry("500x400")

        self.player1_cards = {}
        self.player2_cards = {}

        self.setup_rules_screen()

    def setup_rules_screen(self):
        self.clear_screen()

        rules = (
            "Game Rules:\n"
            "1. Each player selects four different numbers from 1 to 15.\n"
            "2. The selected numbers must be unique and their sum must equal 30.\n"
            "3. The selected numbers are represented by A, B, C, D for Player 1 and 甲, 乙, 丙, 丁 for Player 2.\n"
            "4. Players take turns asking questions to compare either a single card or the sum of two cards with the opponent's cards.\n"
            "5. The program should provide the result of the comparison."
        )

        # Display rules in a label with proper wrapping
        rules_label = tk.Label(self.root, text=rules, justify=tk.LEFT, wraplength=450, font=("Arial", 10))
        rules_label.pack(pady=20)

        # Add a start button
        tk.Button(self.root, text="Start Game", command=self.setup_player1_screen).pack(pady=10)

    def setup_player1_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Player 1, please select four different numbers (1-15) that sum to 30:").pack()
        self.player1_entries = {}
        for card in ['A', 'B', 'C', 'D']:
            frame = tk.Frame(self.root)
            frame.pack()
            tk.Label(frame, text=f"{card}:").pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.LEFT)
            self.player1_entries[card] = entry

        tk.Button(self.root, text="Confirm", command=self.validate_player1_input).pack()

    def validate_player1_input(self):
        try:
            # Get Player 1's cards
            for card, entry in self.player1_entries.items():
                value = int(entry.get())
                if value < 1 or value > 15:
                    raise ValueError("Numbers must be between 1 and 15.")
                self.player1_cards[card] = value

            # Validate selection
            if not validate_selection(list(self.player1_cards.values())):
                raise ValueError("Invalid selection for Player 1. Ensure four different numbers that sum to 30.")

            # Proceed to Player 2's input screen
            self.setup_player2_screen()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def setup_player2_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Player 2, please select four different numbers (1-15) that sum to 30:").pack()
        self.player2_entries = {}
        for card in ['A', 'B', 'C', 'D']:
            frame = tk.Frame(self.root)
            frame.pack()
            tk.Label(frame, text=f"{card}:").pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.LEFT)
            self.player2_entries[card] = entry

        tk.Button(self.root, text="Confirm", command=self.validate_player2_input).pack()

    def validate_player2_input(self):
        try:
            # Get Player 2's cards
            for card, entry in self.player2_entries.items():
                value = int(entry.get())
                if value < 1 or value > 15:
                    raise ValueError("Numbers must be between 1 and 15.")
                self.player2_cards[card] = value

            # Validate selection
            if not validate_selection(list(self.player2_cards.values())):
                raise ValueError("Invalid selection for Player 2. Ensure four different numbers that sum to 30.")

            # Initialize player objects
            self.player1 = Player("Player 1", self.player1_cards)
            self.player2 = Player("Player 2", self.player2_cards)

            # Proceed to the main game screen
            self.setup_game_screen_p1()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_game_screen_p1(self):
        self.clear_screen()

        tk.Label(self.root, text="Game in Progress").pack()

        tk.Button(self.root, text="Player 1: Compare Single Card", command=lambda: self.compare_cards(self.player1, self.player2)).pack()
        tk.Button(self.root, text="Player 1: Compare Sum of Two Cards", command=lambda: self.compare_sums(self.player1, self.player2)).pack()

        tk.Button(self.root, text="Quit Game", command=lambda: quit_game()).pack()

    def setup_game_screen_p2(self):
        self.clear_screen()

        tk.Label(self.root, text="Game in Progress").pack()

        tk.Button(self.root, text="Player 2: Compare Single Card", command=lambda: self.compare_cards(self.player2, self.player1)).pack()
        tk.Button(self.root, text="Player 2: Compare Sum of Two Cards", command=lambda: self.compare_sums(self.player2, self.player1)).pack()

        tk.Button(self.root, text="Quit Game", command=lambda: quit_game()).pack()

    def compare_cards(self, player1, player2):
        self.clear_screen()

        tk.Label(self.root, text=f"{player1.name}, please select your card:").pack()
        self.card1_var = tk.StringVar()
        frame = tk.Frame(self.root)
        frame.pack()
        for card in player1.cards.keys():
            tk.Radiobutton(frame, text=card, variable=self.card1_var, value=card).pack(side=tk.LEFT)

        tk.Label(self.root, text=f"{player1.name}, please select the opponent's card:").pack()
        self.card2_var = tk.StringVar()
        frame = tk.Frame(self.root)
        frame.pack()
        for card in player2.cards.keys():
            tk.Radiobutton(frame, text=card, variable=self.card2_var, value=card).pack(side=tk.LEFT)

        tk.Button(self.root, text="Confirm Comparison", command=lambda: self.show_card_comparison(player1, player2)).pack()

    def show_card_comparison(self, player1, player2):
        card1 = self.card1_var.get()
        card2 = self.card2_var.get()

        value1 = player1.get_card_value(card1)
        value2 = player2.get_card_value(card2)

        if value1 > value2:
            result = f"{card1} is greater than {card2}"
        elif value1 < value2:
            result = f"{card1} is less than {card2}"
        else:
            result = f"{card1} is equal to {card2}"

        messagebox.showinfo("Comparison Result", result)

        match self.flag:
            case 1:
                self.setup_game_screen_p2()
                self.flag = 2
            case 2:
                self.setup_game_screen_p1()
                self.flag = 1

    def compare_sums(self, player1, player2):
        self.clear_screen()

        # Player 1 selects their two cards
        tk.Label(self.root, text=f"{player1.name}, please select your two cards:").pack()
        self.card1_var = tk.StringVar()
        self.card2_var = tk.StringVar()
        frame1 = tk.Frame(self.root)
        frame1.pack()
        for card in player1.cards.keys():
            tk.Radiobutton(frame1, text=card, variable=self.card1_var, value=card).pack(side=tk.LEFT)
        frame2 = tk.Frame(self.root)
        frame2.pack()
        for card in player1.cards.keys():
            tk.Radiobutton(frame2, text=card, variable=self.card2_var, value=card).pack(side=tk.LEFT)

        # Player 1 selects the opponent's two cards
        tk.Label(self.root, text=f"{player1.name}, please select the opponent's two cards:").pack()
        self.card3_var = tk.StringVar()
        self.card4_var = tk.StringVar()
        frame3 = tk.Frame(self.root)
        frame3.pack()
        for card in player2.cards.keys():
            tk.Radiobutton(frame3, text=card, variable=self.card3_var, value=card).pack(side=tk.LEFT)
        frame4 = tk.Frame(self.root)
        frame4.pack()
        for card in player2.cards.keys():
            tk.Radiobutton(frame4, text=card, variable=self.card4_var, value=card).pack(side=tk.LEFT)

        tk.Button(self.root, text="Confirm Comparison", command=lambda: self.show_sum_comparison(player1, player2)).pack()

    def validate_chosen_cards(self, player):
        card1 = self.card1_var.get()
        card2 = self.card2_var.get()
        card3 = self.card3_var.get()
        card4 = self.card4_var.get()

        if card1 == card2 or card3 == card4:
            return False
        return True

    def show_sum_comparison(self, player1, player2):
        card1 = self.card1_var.get()
        card2 = self.card2_var.get()
        card3 = self.card3_var.get()
        card4 = self.card4_var.get()

        if not self.validate_chosen_cards(player1):
            messagebox.showerror("Selection Error", "Ensure the selected cards are not duplicated.")
            return

        sum1 = player1.get_sum(card1, card2)
        sum2 = player2.get_sum(card3, card4)

        if sum1 > sum2:
            result = f"The sum of {card1} and {card2} is greater than the sum of {card3} and {card4}"
        elif sum1 < sum2:
            result = f"The sum of {card1} and {card2} is less than the sum of {card3} and {card4}"
        else:
            result = f"The sum of {card1} and {card2} is equal to the sum of {card3} and {card4}"

        messagebox.showinfo("Comparison Result", result)

        match self.flag:
            case 1:
                self.setup_game_screen_p2()
                self.flag = 2
            case 2:
                self.setup_game_screen_p1()
                self.flag = 1

def main():
    root = tk.Tk()
    app = CardGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()