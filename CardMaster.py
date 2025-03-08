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
        self.root.title("双人卡牌游戏")
        self.root.geometry("500x400")

        self.player1_cards = {}
        self.player2_cards = {}

        self.setup_player1_screen()

    def setup_player1_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="玩家1，请选择四个不同的数字（1-15），且总和为30：").pack()
        self.player1_entries = {}
        for card in ['A', 'B', 'C', 'D']:
            frame = tk.Frame(self.root)
            frame.pack()
            tk.Label(frame, text=f"{card}:").pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.LEFT)
            self.player1_entries[card] = entry

        tk.Button(self.root, text="确认", command=self.validate_player1_input).pack()

    def validate_player1_input(self):
        try:
            # 获取玩家1的卡牌
            for card, entry in self.player1_entries.items():
                value = int(entry.get())
                if value < 1 or value > 15:
                    raise ValueError("数字必须在1到15之间。")
                self.player1_cards[card] = value

            # 验证选择
            if not validate_selection(list(self.player1_cards.values())):
                raise ValueError("玩家1的选择无效，请确保四个数字不重复且总和为30。")

            # 进入玩家2的输入界面
            self.setup_player2_screen()
        except ValueError as e:
            messagebox.showerror("输入错误", str(e))

    def setup_player2_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="玩家2，请选择四个不同的数字（1-15），且总和为30：").pack()
        self.player2_entries = {}
        for card in ['E', 'F', 'G', 'H']:
            frame = tk.Frame(self.root)
            frame.pack()
            tk.Label(frame, text=f"{card}:").pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.LEFT)
            self.player2_entries[card] = entry

        tk.Button(self.root, text="确认", command=self.validate_player2_input).pack()

    def validate_player2_input(self):
        try:
            # 获取玩家2的卡牌
            for card, entry in self.player2_entries.items():
                value = int(entry.get())
                if value < 1 or value > 15:
                    raise ValueError("数字必须在1到15之间。")
                self.player2_cards[card] = value

            # 验证选择
            if not validate_selection(list(self.player2_cards.values())):
                raise ValueError("玩家2的选择无效，请确保四个数字不重复且总和为30。")

            # 初始化玩家对象
            self.player1 = Player("玩家1", self.player1_cards)
            self.player2 = Player("玩家2", self.player2_cards)

            # 进入游戏主界面
            self.setup_game_screen_p1()
        except ValueError as e:
            messagebox.showerror("输入错误", str(e))

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_game_screen_p1(self):
        self.clear_screen()

        tk.Label(self.root, text="游戏进行中").pack()

        tk.Button(self.root, text="玩家1：比较单张卡牌", command=lambda: self.compare_cards(self.player1, self.player2)).pack()
        tk.Button(self.root, text="玩家1：比较两张卡牌之和", command=lambda: self.compare_sums(self.player1, self.player2)).pack()

        tk.Button(self.root, text="退出游戏", command=lambda: quit_game()).pack()

    def setup_game_screen_p2(self):
        self.clear_screen()

        tk.Label(self.root, text="游戏进行中").pack()

        tk.Button(self.root, text="玩家2：比较单张卡牌", command=lambda: self.compare_cards(self.player2, self.player1)).pack()
        tk.Button(self.root, text="玩家2：比较两张卡牌之和", command=lambda: self.compare_sums(self.player2, self.player1)).pack()

        tk.Button(self.root, text="退出游戏", command=lambda: quit_game()).pack()

    def compare_cards(self, player1, player2):
        self.clear_screen()

        tk.Label(self.root, text=f"{player1.name}，请选择你的卡牌：").pack()
        self.card1_var = tk.StringVar()
        frame = tk.Frame(self.root)
        frame.pack()
        for card in player1.cards.keys():
            tk.Radiobutton(frame, text=card, variable=self.card1_var, value=card).pack()

        tk.Label(self.root, text=f"{player1.name}，请选择对方的卡牌：").pack()
        self.card2_var = tk.StringVar()
        frame = tk.Frame(self.root)
        frame.pack()
        for card in player2.cards.keys():
            tk.Radiobutton(frame, text=card, variable=self.card2_var, value=card).pack()

        tk.Button(self.root, text="确认比较", command=lambda: self.show_card_comparison(player1, player2)).pack()

    def show_card_comparison(self, player1, player2):
        card1 = self.card1_var.get()
        card2 = self.card2_var.get()

        value1 = player1.get_card_value(card1)
        value2 = player2.get_card_value(card2)

        if value1 > value2:
            result = f"{card1}大于{card2}"
        elif value1 < value2:
            result = f"{card1}小于{card2}"
        else:
            result = f"{card1}等于{card2}"

        messagebox.showinfo("比较结果", result)

        match self.flag:
            case 1:
                self.setup_game_screen_p2()
                self.flag = 2
            case 2:
                self.setup_game_screen_p1()
                self.flag = 1

    def compare_sums(self, player1, player2):
        self.clear_screen()
        self.step = 1  # 初始化步骤
        self.selected_cards = []  # 存储选择的卡牌

        self.show_sum_selection(player1, player2)

    def show_sum_selection(self, player1, player2):
        if self.step == 1:
            # 第一步：选择自己的两张牌
            tk.Label(self.root, text=f"{player1.name}，请选择你的两张卡牌：").pack()
            self.card1_var = tk.StringVar()
            self.card2_var = tk.StringVar()
            frame = tk.Frame(self.root)
            frame.pack()
            for card in player1.cards.keys():
                tk.Radiobutton(frame, text=card, variable=self.card1_var, value=card).pack(side=tk.LEFT)
                tk.Radiobutton(frame, text=card, variable=self.card2_var, value=card).pack(side=tk.LEFT)

            tk.Button(self.root, text="下一步", command=lambda: self.next_step(player1, player2)).pack()
        elif self.step == 2:
            # 第二步：选择对方的两张牌
            tk.Label(self.root, text=f"{player1.name}，请选择对方的两张卡牌：").pack()
            self.card3_var = tk.StringVar()
            self.card4_var = tk.StringVar()
            frame = tk.Frame(self.root)
            frame.pack()
            for card in player2.cards.keys():
                tk.Radiobutton(frame, text=card, variable=self.card3_var, value=card).pack(side=tk.LEFT)
                tk.Radiobutton(frame, text=card, variable=self.card4_var, value=card).pack(side=tk.LEFT)

            tk.Button(self.root, text="确认比较", command=lambda: self.show_sum_comparison(player1, player2)).pack()

    def next_step(self, player1, player2):
        # 存储玩家1选择的两张牌
        self.selected_cards.append(self.card1_var.get())
        self.selected_cards.append(self.card2_var.get())

        self.step = 2  # 进入第二步
        self.clear_screen()
        self.show_sum_selection(player1, player2)

    def show_sum_comparison(self, player1, player2):
        # 存储玩家2选择的两张牌
        self.selected_cards.append(self.card3_var.get())
        self.selected_cards.append(self.card4_var.get())

        card1, card2, card3, card4 = self.selected_cards

        sum1 = player1.get_sum(card1, card2)
        sum2 = player2.get_sum(card3, card4)

        if sum1 > sum2:
            result = f"{card1}和{card2}之和大于{card3}和{card4}之和"
        elif sum1 < sum2:
            result = f"{card1}和{card2}之和小于{card3}和{card4}之和"
        else:
            result = f"{card1}和{card2}之和等于{card3}和{card4}之和"

        messagebox.showinfo("比较结果", result)

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