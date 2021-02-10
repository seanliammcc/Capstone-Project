import player

class Game:
    def __init__(self, players, dealer, pot,rounds=10):
        #create the game
        self.players = players
        self.dealer = dealer
        self.pot = pot
        self.rounds = rounds
        #shuffle
        #does not deal cards, doesn't know how many

    def play(self):
        #play the game
        for i in range(0,self.rounds):
            print("Round " + str(i))
            round()

    def round(self):
            pass

    def turn(self, player):
        #ask for the players input
        #prompt raise amount 
        #subtract that amount, add to pot
        pass

class TexasHoldEm(Game):
    def __init__(self, players, dealer, pot, community_cards):
        Game.__init__(self, players, dealer, pot)
        self.cards = community_cards #cards in middle of table
        #deal cards

    def round(self):
        #play a round until a player has won
        for player in self.players:
            self.turn(player)
            #take a turn
            #check if a player has won
            #end if won, continue if not
            pass

    def turn(self, player):
        #promt player for input
        #augment player and pot based off of response
        pass
    
    def fold(self):
        #remove player from round
        pass

    def call(self):
        pass

    def bet(self, amt):
        pass

    def check(self):
        pass

