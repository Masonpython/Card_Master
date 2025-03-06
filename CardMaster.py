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

def compare_cards(player1, player2, card1, card2):
    value1 = player1.get_card_value(card1)
    value2 = player2.get_card_value(card2)
    if value1 > value2:
        return f"{card1}大于{card2}"
    elif value1 < value2:
        return f"{card1}小于{card2}"
    else:
        return f"{card1}等于{card2}"

def compare_sums(player1, player2, card1, card2, card3, card4):
    sum1 = player1.get_sum(card1, card2)
    sum2 = player2.get_sum(card3, card4)
    if sum1 > sum2:
        return f"{card1}和{card2}之和大于{card3}和{card4}之和"
    elif sum1 < sum2:
        return f"{card1}和{card2}之和小于{card3}和{card4}之和"
    else:
        return f"{card1}和{card2}之和等于{card3}和{card4}之和"

def get_player_cards(player_name, card_names):
    cards = {}
    print(f"{player_name}，请选择四个不同的数字（1-15），且总和为30：")
    for card in card_names:
        while True:
            try:
                value = int(input(f"请输入{card}的值："))
                if value < 1 or value > 15:
                    print("数字必须在1到15之间，请重新输入。")
                elif value in cards.values():
                    print("数字不能重复，请重新输入。")
                else:
                    cards[card] = value
                    break
            except ValueError:
                print("输入无效，请输入一个整数。")
    
    while not validate_selection(list(cards.values())):
        print("选择的数字总和不为30，请重新选择。")
        cards = {}
        for card in card_names:
            while True:
                try:
                    value = int(input(f"请输入{card}的值："))
                    if value < 1 or value > 15:
                        print("数字必须在1到15之间，请重新输入。")
                    elif value in cards.values():
                        print("数字不能重复，请重新输入。")
                    else:
                        cards[card] = value
                        break
                except ValueError:
                    print("输入无效，请输入一个整数。")
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    return cards

def get_valid_card(player, prompt, valid_cards):
    while True:
        card = input(prompt).upper()
        if card in valid_cards:
            return card
        else:
            print(f"输入的卡牌无效，请重新输入（有效卡牌：{', '.join(valid_cards)}）。")

def main():
    # 玩家1选择
    player1_cards = get_player_cards("玩家1", ['A', 'B', 'C', 'D'])
    player1 = Player("玩家1", player1_cards)

    # 玩家2选择
    player2_cards = get_player_cards("玩家2", ['E', 'F', 'G', 'H'])
    player2 = Player("玩家2", player2_cards)

    # 游戏开始
    while True:
        print("\n玩家1，请选择操作：")
        print("1. 比较单张卡牌")
        print("2. 比较两张卡牌之和")
        choice = input("请输入选择：")
        if choice == '1':
            card1 = get_valid_card(player1, "请输入你的卡牌（A/B/C/D）：", player1.cards.keys())
            card2 = get_valid_card(player2, "请输入对方的卡牌（E/F/G/H）：", player2.cards.keys())
            result = compare_cards(player1, player2, card1, card2)
            print(result)
        elif choice == '2':
            card1 = get_valid_card(player1, "请输入你的第一张卡牌（A/B/C/D）：", player1.cards.keys())
            card2 = get_valid_card(player1, "请输入你的第二张卡牌（A/B/C/D）：", player1.cards.keys())
            card3 = get_valid_card(player2, "请输入对方的第一张卡牌（E/F/G/H）：", player2.cards.keys())
            card4 = get_valid_card(player2, "请输入对方的第二张卡牌（E/F/G/H）：", player2.cards.keys())
            result = compare_sums(player1, player2, card1, card2, card3, card4)
            print(result)
        else:
            print("无效选择，请重新输入。")

        # 玩家2的回合
        print("\n玩家2，请选择操作：")
        print("1. 比较单张卡牌")
        print("2. 比较两张卡牌之和")
        choice = input("请输入选择：")
        if choice == '1':
            card1 = get_valid_card(player2, "请输入你的卡牌（E/F/G/H）：", player2.cards.keys())
            card2 = get_valid_card(player1, "请输入对方的卡牌（A/B/C/D）：", player1.cards.keys())
            result = compare_cards(player2, player1, card1, card2)
            print(result)
        elif choice == '2':
            card1 = get_valid_card(player2, "请输入你的第一张卡牌（E/F/G/H）：", player2.cards.keys())
            card2 = get_valid_card(player2, "请输入你的第二张卡牌（E/F/G/H）：", player2.cards.keys())
            card3 = get_valid_card(player1, "请输入对方的第一张卡牌（A/B/C/D）：", player1.cards.keys())
            card4 = get_valid_card(player1, "请输入对方的第二张卡牌（A/B/C/D）：", player1.cards.keys())
            result = compare_sums(player2, player1, card1, card2, card3, card4)
            print(result)
        else:
            print("无效选择，请重新输入。")

if __name__ == "__main__":
    main()