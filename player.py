import Card
from Camera import Image
import numpy

START_AMOUNT = 5.00

class Player:
    def __init__(self,number,starting_hand = None,betting=START_AMOUNT):
        """
        Create player with an empty hand, an initial amount of money, and a number
        """
        if starting_hand == None: #THis is a python thing, please dont touch
            self.hand = []
        self.money = betting
        self.number = number
    
    def add_card(self, Card):
        """
        add the card to the hand
        """
        self.hand.append(Card)

    def bet(self, amt):
        """
        If possible, remove money from player and return true
        Otherwise, return false
        """
        if self.money - amt > 0:
            self.money = self.money - amt
            return True
        return False
    
    def fold(self):
        """
        Remove Cards from hand
        """
        self.hand.clear()

    def balance(self):
        return self.money

    def player_number(self):
        return self.number

    def player_cards(self):
        return self.hand

class Dealer(Player):
    def __init__(self,rigged=False, number=0,starting_hand = None,betting=START_AMOUNT):
        Player.__init__(self,number,starting_hand = None,betting=START_AMOUNT)
        self.rigged = rigged



