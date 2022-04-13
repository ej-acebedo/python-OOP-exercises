import random
import sys
import time

class Card:
    def __init__(self, suit, val, is_facedown=False):
        self.suit = suit
        self.val = val
        self.is_facedown = is_facedown

    def get_card_prints(self):
        """  
            Backside pattern:
            ___
           |▲▲▲|
           |▼▼▼|
           |_▲_|

            Frontside pattern:
            ___
           |A  |
           | ♥ |
           |__A|

        """
        if self.is_facedown:
            card_segments = [' ___ ', '|▲▲▲|', '|▼▼▼|', '|_▲_|', '']
            return card_segments

        suits = {
                "HEART": '♥',
                "DIAMOND": '♦',
                "CLUB": '♣',
                "SPADE": '♠'
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
        
    # def show_cards(self):
    #     print('number of cards: ', len(self.cards))

class Player(Card):
    def __init__(self, money=0, bet=0):
        self.hands=[]
        self.money=money
        self.bet=bet

    def draw(self, number_of_cards):
        global DECK
        for i in range(number_of_cards):
            card = DECK.remove_card()
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
        for card in self.hands:
            if card.val in ['K', 'Q', 'J', '10']:
                continue
            elif card.val == 'A':
                raw_score += 1
            else:
                raw_score += int(card.val)

        points = str(raw_score)[-1]
        return int(points)  

    def show_money(self):
        money = list(str(self.money))
        for i in range(len(money), -1,-3):
            if i-3 > 0:
                money.insert(i-3, ',')
        formatted_money=''.join(money)
        print('\nMoney: ${}\n'.format(formatted_money))

# GLOBAL objects
DECK = Deck()
MAX_FUNDS = 10000

def main():
    print(f"\nHow much do you wanna play? (Max: {str(MAX_FUNDS)})\n")
    capital = get_money(min=1,max=MAX_FUNDS)
    player1 = Player()
    dealer = Player()
    player1.money = capital
    #initialize game
    run = True
    while run:
        print('Place your bet:')
        bet = get_money(min=1,max=player1.money)
        player1.draw(2)
        dealer.draw(2)
        show_game_status(player1, dealer) # Initial phase
        action = get_action() 
        if dealer.get_points() < 6:
            print('\n...Dealer hits')
            time.sleep(0.95)
            dealer.draw(1) # Dealer HITS if total points has low chance of winning (i.e 1,2,3,4,5)
        result = handle_action(action, player1, dealer, bet)
        show_game_status(player1, dealer, is_endphase= True)
        print(result)
        if player1.money == 0:
            player1.show_money()
            print("You're out of money. Go home")
            sys.exit(0)
        player1.show_money()
        if not is_continue():
            print('Thanks for playing')
            sys.exit(0)
        reset((player1,dealer))

        
def get_money(min,max):
    while True:
        money = input(chr(8594) + " $" + "").strip()
        if not money.isdecimal():
            continue
        else:
            money = int(money)
            if min <= money <= max:
                return money

def get_action():
    while True:
        print('\nPress [1]: Hit, [2]: Stand')
        action = input(chr(8594) + ' ').strip()
        if action not in ['1','2']:
            continue
        else:
            return action

def handle_action(action, player, dealer, bet):
    
    if action.strip() == '1':
        player.draw(1)  # Draw 1 card when player HITS
        return check_winner(player, dealer, bet)
    elif action.strip() == '2':
        return check_winner(player, dealer, bet)

    
def is_continue():
    while True:
        is_continue = input('continue playing(y/n)?')
        if is_continue == 'n':
            return False
        elif is_continue == 'y':
            return True
        else:
            continue

        
def show_game_status(player, dealer, is_endphase = False):
    if not is_endphase:
        dealer.hands[1].is_facedown = True # Hides one Dealer card
    else:
        dealer.hands[1].is_facedown = False
    print("\nDealer's hand") 
    dealer.show_hands()
    print("\nPlayer's hand")
    player.show_hands()
    
def check_winner(player, dealer, bet):
    player_points = player.get_points()
    dealer_points = dealer.get_points()
    # print('player hands: ', len(player.hands) )
    # print(dealer_points, player_points)
    if player_points == dealer_points:
        return '\nDraw\n'
    elif player_points > dealer_points or player_points == 9:
        player.money += bet
        return '\nYou won!\n'
    else:
        player.money -= bet             
        return '\nYou lose.\n'              

def reset(players):
    DECK.reset()
    for player in players:
        player.hands = []

if __name__ == "__main__":
    main()