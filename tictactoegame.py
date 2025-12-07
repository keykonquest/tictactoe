import os
import platform
import random
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

        self.bot_possible = False
        self.human_possible = False
        self.taking_turn = None
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

    def bot_move(self):
        human_spots = []
        bot_spots = []
        # All board coordinates as letter+number (A1, A2, B3, etc.)
        possible_moves = list(self.board.NAMED_COORDINATES.keys())
        for move in possible_moves:
            if self.board.NAMED_COORDINATES[move] in self.players[0].player1_spots:
                human_spots.append(move)
            elif self.board.NAMED_COORDINATES[move] in self.players[1].player2_spots:
                bot_spots.append(move)
        all_spots = bot_spots + human_spots
        all_indexes = self.players[0].player1_spots + self.players[1].player2_spots

        # Helper: check if a player is about to win
        def find_winning_move(player_spots):
            for value in range(len(self.board.LINES)):
                combo = self.board.LINES[value][1]  # e.g. [(0, 1, 2), (0, 3, 6), ...]

                taken_player = [pos for pos in combo if pos in self.players[0].player1_spots]
                taken_bot = [pos for pos in combo if pos in self.players[1].player2_spots]
                empty = [pos for pos in combo if pos not in all_indexes]

                if len(taken_bot) >= 2 and len(empty) == 1:
                    if all(number in self.players[1].player2_spots for number in taken_bot):
                        self.bot_possible = True
                    return empty[0]  # This spot would complete win

                if len(taken_player) == 2 and len(empty) == 1:
                    if all(number in self.players[0].player1_spots for number in taken_player):
                        self.human_possible = True
                    return empty[0]

            return None

        # Can bot win?
        move = find_winning_move(bot_spots)
        if self.bot_possible:
            spot = move
            for move_name in possible_moves:
                if self.board.NAMED_COORDINATES[move_name] == move:
                    spot = move_name
            bot_spots.append(spot)
            self.taking_turn = False

            return spot

        # Block player from winning
        move = find_winning_move(human_spots)
        if self.human_possible and not self.bot_possible:
            spot = move
            for move_name in possible_moves:
                if self.board.NAMED_COORDINATES[move_name] == move:
                    spot = move_name
            bot_spots.append(spot)
            self.taking_turn = False
            return spot

        # Take a corner
        corners = ["A1", "A3", "C1", "C3"]
        open_corners = [c for c in corners if self.board.NAMED_COORDINATES[c] not in all_indexes]
        if open_corners and not (self.human_possible or self.bot_possible):
            choice = random.choice(open_corners)
            spot = choice
            bot_spots.append(spot)
            self.taking_turn = False
            return spot

        # Otherwise, pick any remaining spot
        open_moves = [m for m in possible_moves if self.board.NAMED_COORDINATES[m] not in all_spots]
        choice = random.choice(open_moves)
        spot = choice
        bot_spots.append(spot)
        self.taking_turn = False
        return spot

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
            position = self.board.NAMED_COORDINATES[f"{coordinate}"]
            print("\nBot is thinking")
            show_loading_dots(5)
            print('\n')
            self.board.board[position] = symbol
            self.board.print()
            return True

    def player2_turn(self):
        self.taking_turn = True
        while self.taking_turn:
            if self.players[1].name == "Bot":
                player2_choice = self.bot_move()
                spot = self.board.NAMED_COORDINATES[player2_choice]
                self.players[1].player2_spots.append(spot)
                self.human_possible = False
            else:
                player2_choice = input("\nPlayer 2, choose a spot (e.g. B3): ").upper()
                try:
                    spot = self.board.NAMED_COORDINATES[player2_choice]

                    if spot in self.players[0].player1_spots or spot in self.players[1].player2_spots:
                        print("\nThis spot is already taken!\n")
                        return self.board.print(), self.player2_turn()
                    self.players[1].player2_spots.append(spot)
                    print("\n")
                    self.taking_turn = False
                except KeyError:
                    print("\nPlease enter a valid coordinate.")

            self.player2_mark(player2_choice, self.players[1].symbol)

            return self.players[1].player2_spots
