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
        self.cards.extend(self.delt_cards)
        self.delt_cards = []
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
    def __init__(self, players: Player, dealer: Dealer, pot, deck: Deck, SB = .25, rounds=5):
        """
        Creates a game with an array of player, the dealer, a pot, a deck, and a 
        specified number of rounds.
        Shuffles the Deck.
        """
        self.players = players
        self.dealer = dealer
        self.players.append(self.dealer)
        self.pot = pot
        self.rounds = rounds
        self.deck = deck
        self.round_bet = 0
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
        self.reset_round(0)
    
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
            print("Under the Gun")
            self.under_the_gun(round_players)
            print("Flop")
            self.flop(round_players)
            print("Betting I")
            self.betting(round_players)
            print("Betting II")
            self.betting(round_players)
            print("Showdown")
            self.showdown(round_players)
            self.reset_round(i+1)#reorder the players array so player 1 is in back

    def small_blind(self):
        """
        Small Blind - Player 1 (To left of Dealer) bets the SB amount
        AMount is added to pot and subtracted from player
        """
        player = self.players[0] #Player to left of dealer
        print("This is the Small Blind.")
        print("Player " + str(player.player_number()) + ", you have bet $" + str(round(self.SB,2)))
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
        print("Player " + str(player.player_number()) + ", you have bet $" + str(round(BB,2)))
        player.bet(BB) #removes amount from player
        self.add_to_pot(BB) #adds amount to pot
        self.round_bet = BB
        self.last_raise_player = player.player_number()
        self.BB_player = player.player_number()

    def under_the_gun(self,round_players):
        """
        Complete the round before the flop, each player between BB and dealer goes
        Should be everything before Flop
        """
        if len(round_players) > 2: #only perform this if its needed
            cur_player = 2
            self.round(cur_player,round_players, True)
        elif len(round_players) == 2:
            cur_player = 0
            self.round(cur_player,round_players, True)
        print()

    def flop(self, round_players):
        """
        Reveals community cards, betting until all players have folded or called last raise
        """
        print("The community cards are: ")
        for card in self.community_cards:
            suit, rank = card.identify_card()
            print(suit + rank)
        cur_player = 0
        self.round(cur_player, round_players)
        print()

    def betting(self, round_players):
        """
        Deal additional community card, betting until all players have folded or called last raise
        """
        self.add_community_cards(self.deck.deal_cards(1)) 
        for card in self.community_cards:
                suit, rank = card.identify_card()
                print(suit + rank)
        cur_player = 0
        self.round(cur_player, round_players)
        print()

    def round(self, cur_player, round_players, UTG=False):
        while not(self.evaluate_actions(round_players, cur_player)): #Iterate until all players have folded or called
            choice = self.turn(round_players,round_players[cur_player],UTG)
            print()
            self.update_recent_actions(round_players)
            if choice == "2":
                cur_player = cur_player - 1
            cur_player = cur_player + 1
            if cur_player >= len(round_players):
                #Dealer just calls for now - no AI
                cur_player = 0
        self.round_bet = 0 #Make it so that Player 1 can check for Flop round
        self.reset_recent_actions(round_players) #reset actions so that next round is played
        
    def showdown(self,round_players):
        """
        Evaluate the best hand
        """
        board = create_board(self)
        high_scorer = self.dealer
        hand = create_hand(self.dealer)
        for card in self.dealer.player_cards():
            suit, rank = card.identify_card()
            print(suit + rank)
        min_score = evaluate_player_hand(board,hand) #start with the dealer as the best hand
        for player in round_players:
            hand = create_hand(player) #Find the highest hand and use that as the high scorer
            score = evaluate_player_hand(board,hand)
            if score < min_score:
                min_score = score
                high_scorer = player
        print("Player " + str(high_scorer.player_number()) + " has won!")
        high_scorer.win(self.pot)
        evaluator = Evaluator()
        winning_class = evaluator.get_rank_class(min_score)
        print("The winning hand was " + evaluator.class_to_string(winning_class) + '.')


    def evaluate_actions(self, round_players, cur_player):
        """
        Determine if any actions in the last round have been raises. If so, return false
        If no actions have been a raise, all players have called or folded and round ends
        '1' - raise
        '2' - fold
        '3' - call
        """
        player_no = round_players[cur_player].player_number()
        if (player_no == self.BB_player and self.BB == False):
            self.BB = True
            return False
        for action in self.recent_actions:
            if action == '1' and self.last_raise_player != (player_no):
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
            player.reset_player_round_bet()
        self.update_recent_actions(round_players)
        self.last_raise_player = -1

    def turn(self, round_players, player: Player, UTG):
        """
        Prompt player for input, call the correct function to implement their choice
        """
        if player == self.dealer:
            self.call(player)
            player.assign_recent_action("3")
            return "3"
        print("Player " + str(player.player_number()) + ", you have $" + str(round(player.balance(),2)) + ".")
        print("Player " + str(player.player_number()) + ", please type the number for your choice.")
        print("Your cards are:")
        cards = player.player_cards()
        for card in cards:
            suit, rank = card.identify_card()
            print(suit+rank)
        choice = ""
        while choice != "1" and choice != "2" and choice != "3": 
            options = "Would you like to:\n1 - Raise\n2 - Fold\n3 - Call\n" #present options
            choice = input(options) #Complete player input
            if choice == "1":
                self.Raise(player)
                print("You have $" + str(round(player.balance(),2)))
            elif choice == "2":
                self.fold(player, round_players)
            elif choice == "3":
                self.call(player)
                print("You have $" + str(round(player.balance(),2)))
            else:
                print("Invalid option")
        player.assign_recent_action(choice)
        #print("This player has bet $" + str(round(player.get_player_round_bet(),2)))
        self.display_pot()
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
        call_amt = self.round_bet - player.get_player_round_bet()
        if player.balance() - call_amt < 0: #if player does not have enough money to call
            print("You do not have enough money to call, so you go all in.")
            player.bet(player.balance())
            self.add_to_pot(player.balance())
        else: #Otherwise, just call
            player.bet(call_amt) 
            self.add_to_pot(call_amt)

    def Raise(self, player: Player):
        """
        Ask player how much they will bet - must be greater than previous amount
        Will take the previous bet amount, and RAISE it by the amount input (total amount put into pot
        is sum of previous bet and current raise)
        """
        print("You have $" + str(round(player.balance(),2)))
        amt = float(input("Input how much would you like to raise the previous bet by: "))
        call_amt = self.round_bet - player.get_player_round_bet() # Amount req'd for previous bet
        amt =  call_amt + amt # Previous bet + new raise
        while not(player.bet(amt)): 
        #will remove money in player.bet if amt is valid, otherwise prompts again
            print("Invalid amount.")
            amt = float(input("Input how much would you like to bet: "))
            call_amt = self.round_bet - player.get_player_round_bet()
            amt =  call_amt + amt
        self.round_bet = player.get_player_round_bet()
        self.add_to_pot(amt)
        self.last_raise_player = player.player_number()

    def add_to_pot(self, amt):
        self.pot = self.pot + amt

    def display_pot(self):
        print("The pot has $" + str(round(self.pot,2)))

    def get_community_cards(self):
        return self.community_cards

    def dollar_print(self, num):
        return "$" + round(num,2)

    def update_positions(self):
        prev_sb = self.players.pop(0)
        self.players.insert(len(self.players), prev_sb)

    def reset_round(self, round_no):
        if round_no > 0:
            self.update_positions()
        self.deck.shuffle()
        for player in self.players:
            player.fold()
            cards = self.deck.deal_cards(2) #2 cards for texas hold em
            for card in cards:
                player.add_card(card) #adds a card to the players hand
        self.community_cards = self.deck.deal_cards(3) #sets the 3 initial community cards
        self.recent_actions = []
        self.update_recent_actions(self.players)
        self.pot = 0
        self.BB = False
        self.BB_player = -1
