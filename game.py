from player import Player, Dealer
import random
from Card import Card

ALLRANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
ALLSUITS = ['D', 'H', 'S', 'C']

class Deck:
    def __init__(self):
    #Creates a deck of cards in order
        self.cards = []
        self.delt_cards = []
        for suit in ALLSUITS:
            for rank in ALLRANKS:
                card = Card()
                card.assign_rank(rank)
                card.assign_suit(suit)
                self.cards.append(card)

    def shuffle(self): 
    #temporary function, randomized cards in the deck
    #will later be performed by Dealer
        random.shuffle(self.cards)

    def print_deck(self):
    #prints all cards in the deck
        for card in self.cards:
            print(card)

    #select random cards, remove them from the deck and add to delt
    #cards. Return them for use.
    def deal_cards(self, no_cards):
        cards = []
        for _ in range(0,no_cards):
            card = random.choice(self.cards)
            self.cards.remove(card)
            self.delt_cards.append(card)
            cards.append(card)
        return cards

class Game:
    def __init__(self, players: Player, dealer: Dealer, pot, deck: Deck, rounds=3):
        #create the game
        self.players = players
        self.dealer = dealer
        self.pot = pot
        self.rounds = rounds
        self.deck = deck
        #shuffle
        self.deck.shuffle()
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
    def __init__(self, players: Player, dealer: Dealer, pot, deck: Deck, community_cards=None):
        Game.__init__(self, players, dealer, pot, deck)
        if community_cards == None:
            self.community_cards = [] #cards in middle of table
        #deal cards
        for player in players:
            cards = deck.deal_cards(2)
            for card in cards:
                player.add_card(card)
        self.community_cards = deck.deal_cards(3)
    
    def play(self):
        #play the game
        for i in range(0,self.rounds):
            print("Round " + str(i))
            self.small_blind()
            self.round()
    
    def small_blind(self):
        for player in self.players:
            self.bet(player)

    def round(self):
        #play a round until a player has won
        round_players = self.players
        print("The community cards are: ")
        for card in self.community_cards:
            suit, rank = card.identify_card()
            print(suit + rank)
        while len(round_players) > 1:
            for player in round_players:
                self.turn(player)
                #take a turn
                #check if a player has won
                #end if won, continue if not
                pass

    def turn(self, player):
        #prompt player for input
        #augment player and pot based off of response
        print("Please type the number for your choice.")
        choice = input("Would you like to:\n1 - Bet\n2 - Fold\n3 - Call")
        if choice == "1":
            self.bet(player)
        elif choice == "2":
            self.fold(player)
        elif choice == "3":
            self.call(player)

    
    def fold(self, player):
        #remove player from round
        pass

    def call(self, player):
        pass

    #add money to the pot, remove from player
    def bet(self, player: Player):
        print("You have " + str(player.balance()))
        amt = int(input("Input how much would you like to bet: "))
        if player.bet(amt):
            self.pot = self.pot + amt
        else:
            print("Invalid amount. Next player.")

    def check(self, player):
    #I dont know what this does yet
        pass

