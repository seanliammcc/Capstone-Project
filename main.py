import Camera
from game import Deck, Game, TexasHoldEm
import Card
import motor
from player import Player, Dealer

def create_players(no_players):
    players = []
    for i in range(0,no_players):
        player_1 = Player(i+1)
        players.append(player_1)
    return players

def main():
    game_deck = Deck()
    players = create_players(2)
    dealer = Dealer()
    g = TexasHoldEm(players,dealer,0,game_deck)
    g.play()

if __name__ == "__main__":
    main()