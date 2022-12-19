# print("Hello")
import random

class Card(object):
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val
    
    def show(self):
        print(f'{self.value} of {self.suit}')
    
class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()
    
    def build(self):
        for s in ['Spades', "Clubs"," Diamonds", "Hearts"]:
            for v in range(1, 14):
                self.cards.append(Card(s, v))
                
    def show(self):
        for c in self.cards:
            c.show()
            
            
    def shuffle(self):
        for i in range(len(self.cards)-1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]
                
    def drawCard(self):
        return self.cards.pop()
    
    
class Player(object):
    def __init__(self, name):
        self.hand = []
        self.name = name
        
    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self


    def showHand(self):
        for card in self.hand:
            card.show()
            
    def discard(self):
        return self.hand.pop()

# card = Card("clubs", 6)
# card.show()

deck = Deck()

deck.shuffle()
# deck.show()


bob = Player('Bob')
bob.draw(deck).draw(deck).draw(deck)
bob.showHand()

bob.draw(deck)

# card = deck.drawCard()
# card.show()


