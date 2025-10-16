import os
import platform
import sys
import time

from tictactoeplayers import Player
from tictactoeboard import Board


def clear_terminal():
    """Clears the terminal based on Operating System"""

    curr_os = platform.system()

    if curr_os == "Windows":
        os.system('cls')

    elif curr_os in ('Linux', 'Darwin'):
        os.system('clear')


def print_header():
    print('-' * 30)
    print('TIC TAC TOE')
    print('-' * 30)


def show_loading_dots(num_dots):
    """Displays loading dots"""

    for i in range(num_dots):
        print('. ', end='')

        time.sleep(.75)

    print()


class Game:

    def __init__(self, player1: Player, player2: Player):

        self.position = None
        self.players = (player1, player2)
        self.board = Board()
        self.winner_line = None
        self.turns = 0

    def print_board(self):
        self.board.print()

    def player1_mark(self, coordinate, symbol):
        try:
            self.position = self.board.NAMED_COORDINATES[f"{coordinate}"]
            self.board.board[self.position] = symbol
            self.board.print()
            return True
        except KeyError:
            print(f"'{coordinate}' is not a valid input. Please, try again\n")
            self.board.print()
            return False

    def player1_turn(self):
        taking_turn = True
        while taking_turn:
            player1_choice = input("\nPlayer 1, choose a spot (e.g. B3): ").upper()
            try:
                spot = self.board.NAMED_COORDINATES[player1_choice]
                if spot in self.players[0].player1_spots or spot in self.players[1].player2_spots:
                    print("\nThis spot is already taken!\n")
                    return self.board.print(), self.player1_turn()
                self.players[0].player1_spots.append(spot)
                print("\n")
                taking_turn = False
            except KeyError:
                print("\nPlease enter a valid coordinate.")

        self.player1_mark(player1_choice, self.players[0].symbol)

        return self.players[0].player1_spots

    def player2_mark(self, coordinate, symbol):
        if self.players[1].name != "Bot":
            try:
                position = self.board.NAMED_COORDINATES[f"{coordinate}"]
                self.board.board[position] = symbol
                self.board.print()
                return True
            except KeyError:
                print(f"'{coordinate}' is not a valid input. Please, try again\n")
                self.board.print()
                return False
        else:
            print("Bot is thinking")
            show_loading_dots(5)

    def player2_turn(self):
        taking_turn = True
        while taking_turn:
            if self.players[1].name == "Bot":
                sys.exit()
            else:
                player2_choice = input("\nPlayer 2, choose a spot (e.g. B3): ").upper()
                try:
                    spot = self.board.NAMED_COORDINATES[player2_choice]

                    if spot in self.players[0].player1_spots or spot in self.players[1].player2_spots:
                        print("\nThis spot is already taken!\n")
                        return self.board.print(), self.player2_turn()
                    self.players[1].player2_spots.append(spot)
                    print("\n")
                    taking_turn = False
                except KeyError:
                    print("\nPlease enter a valid coordinate.")

            self.player2_mark(player2_choice, self.players[1].symbol)

            return self.players[1].player2_spots
