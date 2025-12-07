from tictactoegame import Game, clear_terminal, print_header, show_loading_dots
from tictactoeplayers import Player


def print_menu():
    clear_terminal()

    print_header()

    print('\nChoose a game mode:\n')
    print('1. Player vs Player')
    print('2. Player vs Computer \n')
    user_choice = input(">>> ")
    try:
        int(user_choice)
    except ValueError:
        return "Please enter '1' or '2'"
    return int(user_choice)


def get_game(game_type):
    if game_type == 1:
        current_game = Game(player1=Player('Player 1', 'X'), player2=Player('Player 2', 'O'))
    elif game_type == 2:
        current_game = Game(player1=Player('Player', 'X'), player2=Player('Bot', 'O'))
    else:
        print("Invalid input. Please enter '1' or '2'\n")
        return get_game(print_menu())
    return current_game


def main():
    tictactoe = get_game(print_menu())
    player1 = tictactoe.players[0]
    player2 = tictactoe.players[1]
    tictactoe.print_board()

    continue_game = True
    while continue_game:
        tictactoe.player1_turn()
        tictactoe.turns += 1
        for value in range(len(tictactoe.board.LINES)):
            win_combo = list(tictactoe.board.LINES[value][1])
            if len(player1.player1_spots) >= 3 and set(win_combo).issubset(player1.player1_spots):
                print(f"\nPLayer 1 has completed {tictactoe.board.LINES[value][0]}! That's a win!")
                continue_game = False
                break
        if tictactoe.turns == 9:
            print("\nCat's game. Well played!")
            continue_game = False
        elif continue_game:
            tictactoe.player2_turn()
            tictactoe.turns += 1
        for value in range(len(tictactoe.board.LINES)):
            win_combo = list(tictactoe.board.LINES[value][1])
            if len(player2.player2_spots) >= 3 and set(win_combo).issubset(player2.player2_spots):
                print(f"\nPLayer 2 has completed {tictactoe.board.LINES[value][0]}! That's a win!")
                continue_game = False
                break

    play_again = input("\nWould you like to play again? (Y)es or (N)o\n").upper()

    if play_again in ["Y", "YES"]:
        tictactoe.players[0].player1_spots.clear()
        tictactoe.players[1].player2_spots.clear()
        main()
    elif play_again not in ["N", "NO"]:
        tictactoe.players[0].player1_spots.clear()
        tictactoe.players[1].player2_spots.clear()
        print("\nI'll take that as a yes!\n")
        main()


if __name__ == '__main__':
    main()