import Camera
from game import Deck, Game, TexasHoldEm
import Card
import motor
from player import Player, Dealer

def create_players(no_players):
    """
    Create an array of players for the game
    Each player recieves number
    """
    players = []
    for i in range(0,no_players):
        player_1 = Player(i+1)
        players.append(player_1)
    return players

def main():
    game_deck = Deck() #Create Deck
    players = create_players(2) #Create players for game
    dealer = Dealer() #Create Dealer
    g = TexasHoldEm(players,dealer,0,game_deck) #Create Game
    g.play()

if __name__ == "__main__":
    main()