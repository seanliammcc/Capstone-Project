from player import Player, Dealer
import random
from Card import Card

ALLRANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
ALLSUITS = ['D', 'H', 'S', 'C']

class Deck:
    def __init__(self):
    """
    Creates a deck of cards in order, stored into cards
    Cards that have been delt are moved from cards to delt_cards
    """
        self.cards = []
        self.delt_cards = []
        for suit in ALLSUITS:
            for rank in ALLRANKS:
                card = Card()
                card.assign_rank(rank)
                card.assign_suit(suit)
                self.cards.append(card)

    def shuffle(self): 
    """
    Currently randomizes the cards that are in the deck.
    TODO - make shuffling physical with dealer
    """
        random.shuffle(self.cards)

    def print_deck(self):
    """
    Prints all cards in deck - for debugging
    """
        for card in self.cards:
            print(card)

    #select random cards, remove them from the deck and add to delt
    #cards. Return them for use.
    def deal_cards(self, no_cards):
        """
        Select random cards from the deck, and return them to be added to hands,
        discarded, or used as community cards.
        Moves cards from self.cards to self.delt_cards
        """
        cards = []
        for _ in range(0,no_cards):
            card = random.choice(self.cards)
            self.cards.remove(card)
            self.delt_cards.append(card)
            cards.append(card)
        return cards

class Game:
    def __init__(self, players: Player, dealer: Dealer, pot, deck: Deck, SB = .25, rounds=3):
        """
        Creates a game with an array of player, the dealer, a pot, a deck, and a 
        specified number of rounds.
        Shuffles the Deck.
        """
        self.players = players
        self.dealer = dealer
        self.pot = pot
        self.rounds = rounds
        self.deck = deck
        self.previous_bet = 0
        self.SB = SB
        #shuffle
        self.deck.shuffle()
        #does not deal cards, doesn't know how many

    def play(self):
        """
        Meant to be redeclared by child classes
        """
        for i in range(0,self.rounds):
            print("Round " + str(i))
            round()

    def round(self):
            pass

    def turn(self, player):
        """#ask for the players input
        #prompt raise amount 
        #subtract that amount, add to pot"""
        pass

class TexasHoldEm(Game):
    def __init__(self, players: Player, dealer: Dealer, pot, deck: Deck, community_cards=None):
        """
        Creates a game of texas hold 'em, same as game but with community cards
        """
        Game.__init__(self, players, dealer, pot, deck)
        if community_cards == None:
            self.community_cards = [] #cards in middle of table
        #deals cards to all the players in the game
        for player in self.players:
            cards = self.deck.deal_cards(2) #2 cards for texas hold em
            for card in cards:
                player.add_card(card) #adds a card to the players hand
        self.community_cards = self.deck.deal_cards(3) #sets the 3 initial community cards
    
    def play(self):
        """
        Plays the game by going through rounds.
        Each round has SB, BB, UTG (Under the Gun), and then Flop, Betting I and II, showdown
        """
        for i in range(0,self.rounds):
            print("Round " + str(i+1))
            round_players = self.players.view() #Players in this round
            self.small_blind()
            self.big_blind()
            self.under_the_gun(round_players)
            self.flop(round_players)
            self.betting(round_players)
            self.betting(round_players)
            self.showdown(round_players)

    def small_blind(self):
        """
        Small Blind - Player 1 (To left of Dealer) bets the SB amount
        AMount is added to pot and subtracted from player
        """
        player = self.players[0] #Player to left of dealer
        print("This is the Small Blind.")
        print("Player " + str(player.player_number()) + ", you have bet " + str(self.SB))
        player.bet(self.SB) #removes amount from player
        self.add_to_pot(self.SB) #adds amount to pot
        
    def big_blind(self):
        """
        Big Blind - Player 2 (To left of SB) bets the BB amount
        Amount is added to pot and subtracted from player
        """
        player = self.players[1] #Player to left of SB
        print("This is the Big Blind.")
        BB = 2*self.SB #set BB amount
        print("Player " + str(player.player_number()) + ", you have bet " + str(BB))
        player.bet(BB) #removes amount from player
        self.add_to_pot(BB) #adds amount to pot

    def under_the_gun(self,round_players):
        """
        Complete the round before the flop, each player between BB and dealer goes
        Should be everything before Flop
        TODO - Fix issues with end - should continue until all players call or fold
        """
        if len(round_players) > 2:
            for i in range(2,len(round_players())): #Only players that weren't SB and BB
                self.turn(round_players,round_players[i],True)
            self.call(self.dealer()) #Dealer just calls for now - no AI
            self.previous_bet = 0 #Make it so that Player 1 can check for 1st round
            self.call(self.dealer) #Dealer calls

    def flop(self, round_players):
        """
        Reveals community cards, betting until all players have folded or called last raise
        TODO - betting until all players have folded or called last raise
        """
        print("The community cards are: ")
            for card in self.community_cards:
                suit, rank = card.identify_card()
                print(suit + rank)
        pass

    def betting(self, round_players):
        """
        Deal additional community card, betting until all players have folded or called last raise
        TODO - betting until all players have folded or called last raise
        """
        card = self.deck.deal_cards(1)
        self.community_cards.append(card)
        for card in self.community_cards:
                suit, rank = card.identify_card()
                print(suit + rank)
        pass

    def showdown(self,round_players):
        """
        Evaluate the best hand
        """
        pass

    """#Todo - set restrictions on how to end round
    def round(self, round_players):
        #play a round until a player has won
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
            self.community_cards.append(card)"""

    def turn(self, round_players, player, UTG):
        """
        Prompt player for input, call the correct function to implement their choice
        """
        print("Player " + str(player.player_number()) + ", please type the number for your choice.")
        if not(UTG):  #Only show player their cards if its not the first round
            print("Your cards are:")
            cards = player.player_cards()
            for card in cards:
                suit, rank = card.identify_card()
                print(suit+rank)
        options = "Would you like to:\n1 - Bet\n2 - Fold\n3 - Call\n" #present options
        if self.previous_bet > 0: #Only allow for check if the previous bet was zero
            options = options + "4 - Check\n"
        choice = input(options) #Complete player input
        if choice == "1":
            self.bet(player)
        elif choice == "2":
            self.fold(player, round_players)
        elif choice == "3":
            self.call(player)
        elif choice == "4":
            self.check(player)

    
    def fold(self, player, round_players):
        """
        Remove player from this round
        """
        round_players.remove(player)
        

    def call(self, player: Player):
        """
        Match the previous bet if possible, or go all in otherwise
        """
        if player.balance() - self.previous_bet < 0: #if player does not have enough money to call
            print("You do not have enough money to call, so you go all in.")
            player.bet(player.balance())
            self.add_to_pot(player.balance())
        else: #Otherwise, just call
            player.bet(self.previous_bet) 
            self.add_to_pot(self.previous_bet)

    def bet(self, player: Player):
        """
        Ask player how much they will bet - must be greater than previous amount
        """
        print("You have " + str(player.balance()))
        amt = float(input("Input how much would you like to bet: "))
        while not(player.bet(amt)) and amt < self.previous_bet: 
        #will remove money in player.bet if amt is valid, otherwise prompts again
            print("Invalid amount.")
            amt = float(input("Input how much would you like to bet: "))
        print("You have " + str(player.balance()))
        self.previous_bet = amt
        self.add_to_pot(amt)

    #I dont know what this does yet
    def check(self, player):
        pass

    def add_to_pot(self, amt):
        self.pot = self.pot + amt


    #call raise or fold - calling when bet is zero is check