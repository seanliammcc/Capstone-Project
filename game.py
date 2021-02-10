import player

class Game:
    def __init__(self, players, dealer, pot):
        #create the game
        self.players = players
        self.dealer = dealer
        self.pot = pot
        #shuffle
        #does not deal cards, doesn't know how many

    def play(self):
        #play the game
        for player in self.players:
            #take a turn
            #check if a player has won
            #end if won, continue if not
            pass

    def turn(self, player):
        #ask for the players input
        #prompt raise amount 
        #subtract that amount, add to pot

class TexasHoldEm(Game):
    def __init__(self, players, dealer, pot, community_cards):
        Game.__init__(self, players, dealer, pot)
        self.cards = community_cards #cards in middle of table
        #deal cards

    def turn(self):
        #promt player for input
    
    def fold(self):
        pass

    def call(self):
        pass

    def bet(self, amt):
        pass

    def check(self):
        pass

