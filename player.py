import card
from camera import Image
import numpy

class Player:
    def __init__(self,number,betting=5, starting_hand = None):
        """
        Create player with an empty hand, an initial amount of money, and a number
        """
        if starting_hand == None: #THis is a python thing, please dont touch
            self.hand = []
        self.money = betting
        self.number = number
        self.previous_action = "1"
        self.round_bet = 0
    
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
        if self.money - amt >= 0:
            self.money = self.money - amt
            self.set_player_round_bet(amt)
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

    def return_prev_action(self):
        return self.previous_action

    def set_player_round_bet(self, round_bet):
        self.round_bet = round_bet + self.round_bet

    def reset_player_round_bet(self):
        self.round_bet = 0

    def get_player_round_bet(self):
        return self.round_bet

    def assign_recent_action(self, action):
        self.previous_action = action

    def win(self, pot):
        self.money = self.money + pot

class Dealer(Player):
    def __init__(self,rigged=False, number=0,betting=5,starting_hand = None):
        Player.__init__(self,number,betting=5,starting_hand = None)
        self.rigged = rigged

    def bet(self, amt):
        """
        Perform call, and then output to screen
        """
        Player.bet(self, amt)
        print("The dealer has called")


