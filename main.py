import sys


from data.classes.console_tools import game_mode_selection
from data.classes.game import GameField, Player
from data.classes.user import User


def start_game():
    game_field = GameField()  # створюємо поле
    first_player = Player(True, 1)
    second_player = Player(False, 2)
    game_mode_selection()  # перша лаба, вибір для гравця
    game_mode = User.ask_game_mode()
    if game_mode == "1":
        first_player = Player(True, 2)
        second_player = Player(True, 1)
    elif game_mode == "2":
        first_player = Player(True, 1)
        second_player = Player(False, 2)
    elif game_mode == "4":
        first_player = Player(False, 1)
        second_player = Player(True, 2)
    elif game_mode == "3":
        first_player = Player(False, 1)
        second_player = Player(False, 2)
    else:
        start_game()

    list_of_players = [first_player, second_player]
    counter = 0
    number_moves = 0  # Кількість ходів


def build_wall():
    pass


def move_player():
    pass


def game():
    pass


if __name__ == '__main__':
    start_game()
