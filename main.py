import camera
from game import Deck, Game, TexasHoldEm
import card
import motor
from player import Player, Dealer

def create_players(no_players,START_AMOUNT):
    """
    Create an array of players for the game
    Each player recieves number
    """
    players = []
    for i in range(0,no_players):
        player_1 = Player(i+1,START_AMOUNT)
        players.append(player_1)
    return players

def main():
    START_AMOUNT = 5.00
    game_deck = Deck() #Create Deck
    no_players = int(input("Please input the number of players:\n"))
    players = create_players(no_players,START_AMOUNT) #Create players for game
    dealer = Dealer() #Create Dealer
    g = TexasHoldEm(players,dealer,0,game_deck) #Create Game
    g.play()

if __name__ == "__main__":
    main()