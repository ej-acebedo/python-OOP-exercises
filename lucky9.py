import random
import time

class Card:
    def __init__(self, suit, val, facedown=False):
        self.suit = suit
        self.val = val
        self.facedown = facedown

    def get_card_prints(self):
        if self.facedown:
            card_segments = [' ___ ', f'|{3*chr(9650)}|', f'|{3*chr(9660)}|', f'|_{chr(9650)}_|', '']
            return card_segments
        suits = {
                "HEART": chr(9829),
                "DIAMOND": chr(9830),
                "CLUB": chr(9827),
                "SPADE": chr(9824)
            }
        card_segments = [' ___ ', '', '', '', '', '']
        card_segments[1] = '|' + '{}'.format(self.val).ljust(3, ' ') + '|'
        card_segments[2] = '| {} |'.format(suits[self.suit])
        card_segments[3] = '|_' + '{}'.format(self.val).rjust(2, '_') +'|'

        return card_segments
        
class Deck:
    
    def __init__(self):
        self.cards=[]
        self._build()

    def _build(self):
        for suit in ['HEART', 'DIAMOND', 'CLUB', 'SPADE']:
            for val in range(1,15):
                if val == 11:
                    card = Card(suit, 'J')
                    self.cards.append(card)
                elif val == 12:
                    card = Card(suit, 'Q')
                    self.cards.append(card)
                elif val == 13:
                    card = Card(suit, 'K')
                    self.cards.append(card)
                elif val == 14:
                    card = Card(suit, 'A')
                    self.cards.append(card)
                else:
                    card = Card(suit, str(val))
                    self.cards.append(card)
        # Shuffle Deck
        for idx in range(len(self.cards)-1,-1,-1):
            random_idx = random.randint(0,idx)
            self.cards[idx], self.cards[random_idx] = self.cards[random_idx], self.cards[idx]
        return None
   
    def remove_card(self):
        card_drawn = self.cards.pop()
        return card_drawn

    def reset(self):
        self.cards = []
        self._build()
    def show_cards(self):
        print('number of cards: ', len(self.cards))
        print(self.cards)

class Player(Card):
    def __init__(self, money=0, bet=0):
        # self.name = name
        self.hands=[]
        self.money=money
        self.bet=bet

    def draw(self, number_of_cards):
        global deck
        for i in range(number_of_cards):
            card = deck.remove_card()
            self.hands.append(card)

    def show_hands(self):
        y=["","","",""]
        for card in self.hands:
                card_print = card.get_card_prints()
                y[0] += card_print[0]
                y[1] += card_print[1]
                y[2] += card_print[2]
                y[3] += card_print[3]
        for i in y:
            print("".join(i))
            
    def get_points(self):
        raw_score=0
        for suit, val in self.hands:
            if val in ['K', 'Q', 'J', '10']:
                continue
            elif val == 'A':
                raw_score += 1
            else:
                raw_score += int(val)

        points = str(raw_score)[-1]
        return int(points)  

    def reset_hands(self):
        self.hands = []

    def show_money(self):
        money = list(str(self.money))
        for i in range(len(money), -1,-3):
            if i-3 > 0:
                money.insert(i-3, ',')
        formatted_money=''.join(money)
        print('\nMoney: ${}\n'.format(formatted_money))

deck = Deck()
p1 = Player()
dealer = Player()

print("\nDealer's hand")
dealer.draw(2)
dealer.hands[1].facedown = True
dealer.show_hands()
print("\nCaloy\t(Money: $5,000)")
p1.draw(2)
p1.show_hands()
print("\nPress [1]: Hit, [2]: Stand, [Q]: Quit")

# deck = Deck()
# max_funds = 10000
# def main():
#     print("\nHow much do you wanna play? (Max: $10,000)\n")
#     capital = get_money(min=1,max=max_funds)
#     player1 = Player()
#     dealer = Player(dealer=True)
#     player1.money = capital
#     #initialize game
#     while True:
#         player1.show_money()
#         # Continue playing if player money is not zero
#         if player1.money:
#             deck.show_cards()
#             print('Place your bet:')
#             bet = get_money(min=1,max=player1.money)
#             player1.draw(2)
#             dealer.draw(2)
#             if dealer.get_points() < 6:
#                 print('Dealer drew a card')
#                 dealer.draw(1)
#             handle_action(player1, dealer, bet)
#             reset((player1, dealer))
#         else:
#             print("You're out of money")
#             print('Thanks for playing...')
#             break

# def get_money(min,max):
#     while True:
#         money = input(chr(8594) + " $" + "").strip()
#         if not money.isdecimal():
#             continue
#         else:
#             money = int(money)
#             if min <= money <= max:
#                 return money

# def handle_action(player, dealer, bet):
#     player.show_hand()
#     action = input('\nPress (H)it, (S)tand: ')
#     if action.lower().strip() == 'h': # Draw 1 card when (H)it is pressed
#         player.draw(1)
#         check_winner(player, dealer, bet)
#     elif action.lower().strip() == 's':
#         check_winner(player, dealer, bet)
#     else:
#         print('Try again') 

# def check_winner(player, dealer, bet):
#     player_points = player.get_points()
#     dealer_points = dealer.get_points()
#     player.show_hand()
#     dealer.show_hand()
#     if player_points > dealer_points:
#         print('You won!\n')
#         player.money += bet
#         player.show_money()
#     elif player_points == dealer_points:
#         print('Draw')
#         player.show_money()
#         # check for natural 9
#     elif player_points == 9:
#         player.money += bet
#         player.show_money()
#     else:
#         print('You lose.')
#         player.money -= bet
#         player.show_money()                                 

# def reset(players):
#     deck.reset()
#     for player in players:
#         player.reset_hands()

# if __name__ == "__main__":
#     main()