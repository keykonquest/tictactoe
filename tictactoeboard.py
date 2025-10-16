from collections import namedtuple

Line = namedtuple('Line', 'name indices')


class Board:
    # A tuple of all winning combinations
    LINES = (
        Line('row A', (0, 1, 2)),
        Line('row B', (3, 4, 5)),
        Line('row C', (6, 7, 8)),
        Line('column 1', (0, 3, 6)),
        Line('column 2', (1, 4, 7)),
        Line('column 3', (2, 5, 8)),
        Line('diagonal A', (0, 4, 8)),
        Line('diagonal', (2, 4, 6))
    )

    # Board coordinates
    NAMED_COORDINATES = {
        'A1': 0, 'A2': 1, 'A3': 2,
        'B1': 3, 'B2': 4, 'B3': 5,
        'C1': 6, 'C2': 7, 'C3': 8,
    }

    def __init__(self):

        self.board = [' '] * 9

    def print(self):

        """Prints the game board with current game state."""

        print('     1   2   3')

        print('   -------------')

        for cord, pos in self.NAMED_COORDINATES.items():

            row_letter = f' {cord[0]:1} ' if '1' in cord else ' '

            print(f'{row_letter:1}| {self.board[pos]:1}', end='')

            if pos in (2, 5, 8):
                print(' |\n   -------------')

    def print_coordinates(self):

        """Prints the expected input coordinates for plays."""

        print('     1   2   3')

        print('   -------------')

        for cord, pos in self.NAMED_COORDINATES.items():

            row_letter = f' {cord[0]:1} ' if '1' in cord else ''

            print(f'{row_letter}| {cord}', end='')

            if pos in (2, 5, 8):
                print('|\n   -------------')
