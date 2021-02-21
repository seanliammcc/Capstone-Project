import numpy
from camera import Image

class Card:
    def __init__(self,suits=None,ranks=None):
        self.suit = suits
        self.rank = ranks

    def assign_suit(self, suit):
        #assign suit to card
        self.suit = suit

    def assign_rank(self, rank):
        #assign rank to card
        self.rank = rank

    def identify_card(self):
        return self.suit, self.rank
    