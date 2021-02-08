import Card
from Camera import Image
import numpy

START_AMOUNT = 5

class Player:
    def __init__(self,starting_hand = None,betting=START_AMOUNT):
        if starting_hand == None:
            self.hand = []
        self.money = betting
    
    def add_card(self, Card):
        #add the card to the hand
        self.hand.append(Card)
        pass

class Dealer(Player):
    def __init__(self,starting_hand = None,betting=START_AMOUNT, rigged=False):
        Player.__init__(self,starting_hand = None,betting=START_AMOUNT)
        self.cheating = rigged

    



