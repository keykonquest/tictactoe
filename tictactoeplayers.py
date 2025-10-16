import random
from collections import defaultdict


class Player:
    player1_spots = []
    player2_spots = []

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
