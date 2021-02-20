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
        self.previous_bet = 0
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
        for player in self.players:
            cards = self.deck.deal_cards(2)
            for card in cards:
                player.add_card(card)
        self.community_cards = self.deck.deal_cards(3)
    
    def play(self):
        #play the game
        for i in range(0,self.rounds):
            print("Round " + str(i+1))
            self.small_blind()
            self.big_blind()
            if len(self.players) > 2:
                self.under_the_gun()
            self.round()

    #todo - set SB amount
    def small_blind(self):
        player = self.players[0] #Player to left of dealer
        print("This is the Small Blind.")
        print("Player " + str(player.player_number()) + ", please input your bet.")
        self.bet(player)
    
    #todo - set BB amount
    def big_blind(self):
        player = self.players[1] #Player to left of SB
        print("This is the Big Blind.")
        print("Player " + str(player.player_number()) + ", please input your bet.")
        self.bet(player)

    def under_the_gun(self):
        round_players = self.players
        for i in range(2,len(round_players())): #Only players that were'nt SB and BB
            self.turn(round_players[i],True)
        self.call(self.dealer()) #Dealer just calls for now - no AI
        self.previous_bet = 0 #Make it so that Player 1 can check for 1st round

    #Todo - set restrictions on how to end round
    def round(self):
        #play a round until a player has won
        round_players = self.players
        while len(round_players) > 1: #not true condition, must be improved
            print("The community cards are: ")
            for card in self.community_cards:
                suit, rank = card.identify_card()
                print(suit + rank)
            for player in round_players:
                self.turn(round_players,player,False)
                #take a turn
                #check if a player has won
                #end if won, continue if not
            self.call(self.dealer)
            card = self.deck.deal_cards(1)
            self.community_cards.append(card)

    def turn(self, round_players, player, UTG):
        #prompt player for input
        #augment player and pot based off of response
        print("Player " + str(player.player_number()) + ", please type the number for your choice.")
        if not(UTG):
            print("Your cards are:")
            cards = player.player_cards()
            for card in cards:
                suit, rank = card.identify_card()
                print(suit+rank)
        choice = input("Would you like to:\n1 - Bet\n2 - Fold\n3 - Call\n")
        if choice == "1":
            self.bet(player)
        elif choice == "2":
            self.fold(player, round_players)
        elif choice == "3":
            self.call(player)

    
    def fold(self, player, round_players):
        round_players.remove(player)
        

    def call(self, player: Player):
        if player.balance() - self.previous_bet < 0:
            print("You do not have enough money to call, so you go all in.")
            player.bet(player.balance())
        else:
            player.bet(self.previous_bet)

    #add money to the pot, remove from player
    def bet(self, player: Player):
        print("You have " + str(player.balance()))
        amt = float(input("Input how much would you like to bet: "))
        while not(player.bet(amt)) and amt < self.previous_bet:
            print("Invalid amount.")
            amt = float(input("Input how much would you like to bet: "))
        print("You have " + str(player.balance()))
        self.previous_bet = amt

    #I dont know what this does yet
    def check(self, player):
        pass

