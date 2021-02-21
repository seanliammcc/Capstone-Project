from player import Player, Dealer
import random
from card import Card
from treys import Card as tCard
from treys import Evaluator

ALLRANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
ALLSUITS = ['D', 'H', 'S', 'C']

def create_board(game):
    """
    Reformat the cards into this library's syntax
    """
    cards = game.get_community_cards()
    board = []
    for card in cards:
        suit, rank = card.identify_card()
        new_card = rank+suit.lower()
        board.append(tCard.new(new_card))
    return board

def create_hand(player):
    """
    Reformat the cards into this library's syntax
    """
    cards = player.player_cards()
    hand = []
    for card in cards:
        suit, rank = card.identify_card()
        new_card = rank+suit.lower()
        hand.append(tCard.new(new_card))
    return hand

def evaluate_player_hand(board, hand):
    evaluator = Evaluator()
    return evaluator.evaluate(board,hand)

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
        cards = self.deck.deal_cards(2) #2 cards for texas hold em
        for card in cards:
            self.dealer.add_card(card) #adds a card to the players hand
        self.community_cards = self.deck.deal_cards(3) #sets the 3 initial community cards
        self.recent_actions = []
        self.update_recent_actions(self.players)
    
    def add_community_cards(self, cards):
        for card in cards:
            self.community_cards.append(card)

    def play(self):
        """
        Plays the game by going through rounds.
        Each round has SB, BB, UTG (Under the Gun), and then Flop, Betting I and II, showdown
        """
        for i in range(0,self.rounds):
            print("Round " + str(i+1))
            round_players = self.players.copy() #Players in this round
            self.small_blind()
            self.big_blind()
            print("Utg")
            self.under_the_gun(round_players)
            print("Flop")
            self.flop(round_players)
            print("Betting I")
            self.betting(round_players)
            print("Betting II")
            self.betting(round_players)
            print("Showdown")
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
        if len(round_players) > 2: #only perform this if its needed
            cur_player = 2
            self.round(cur_player,round_players)

    def flop(self, round_players):
        """
        Reveals community cards, betting until all players have folded or called last raise
        TODO - betting until all players have folded or called last raise
        """
        print("The community cards are: ")
        for card in self.community_cards:
            suit, rank = card.identify_card()
            print(suit + rank)
        cur_player = 0
        self.round(cur_player, round_players)


    def betting(self, round_players):
        """
        Deal additional community card, betting until all players have folded or called last raise
        TODO - betting until all players have folded or called last raise
        """
        self.add_community_cards(self.deck.deal_cards(1)) 
        for card in self.community_cards:
                suit, rank = card.identify_card()
                print(suit + rank)
        cur_player = 0
        self.round(cur_player, round_players)

    def round(self, cur_player, round_players):
        while not(self.evaluate_actions()): #Iterate until all players have folded or called
            choice = self.turn(round_players,round_players[cur_player],True)
            self.update_recent_actions(round_players)
            if choice == "2":
                cur_player = cur_player - 1
            cur_player = cur_player + 1
            if cur_player >= len(round_players):
                self.call(self.dealer) #Dealer just calls for now - no AI
                cur_player = 0
        self.previous_bet = 0 #Make it so that Player 1 can check for Flop round
        self.reset_recent_actions(round_players) #reset actions so that next round is played
        
    def showdown(self,round_players):
        """
        Evaluate the best hand
        """
        board = create_board(self)
        high_scorer = 0
        hand = create_hand(self.dealer)
        max_score = evaluate_player_hand(board,hand)
        for player in round_players:
            hand = create_hand(player)
            score = evaluate_player_hand(board,hand)
            if score > max_score:
                max_score = score
                high_scorer = player.player_number()
        print("Player " + str(high_scorer) + " has won!")




    def evaluate_actions(self):
        """
        Determine if any actions in the last round have been raises. If so, return false
        If no actions have been a raise, all players have called or folded and round ends
        '1' - raise
        '2' - fold
        '3' - call
        """
        for action in self.recent_actions:
            if action == '1':
                return False
        return True

    def update_recent_actions(self,round_players):
        """
        Reset recent actions so that the next hand is played without interruption
        """
        self.recent_actions = []
        for player in round_players:
            self.recent_actions.append(player.return_prev_action())

    def reset_recent_actions(self,round_players):
        """
        Reset recent actions so that the next hand is played without interruption
        """
        for player in round_players:
            player.assign_recent_action("1")
        self.update_recent_actions(round_players)

    def turn(self, round_players, player: Player, UTG):
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
        options = "Would you like to:\n1 - Raise\n2 - Fold\n3 - Call\n" #present options
        choice = input(options) #Complete player input
        if choice == "1":
            self.Raise(player)
        elif choice == "2":
            self.fold(player, round_players)
        elif choice == "3":
            self.call(player)
        player.assign_recent_action(choice)
        return choice
    
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

    def Raise(self, player: Player):
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

    def add_to_pot(self, amt):
        self.pot = self.pot + amt

    def get_community_cards(self):
        return self.community_cards
