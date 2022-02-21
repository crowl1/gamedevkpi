from data.classes.console_tools import game_mode_selection
from data.classes.game import GameField, Player
from data.classes.user import User


def game():
    game_field = GameField() # створюємо поле
    first_player = Player(True, 1)
    second_player = Player(False, 2)
    game_mode_selection() #перша лаба, вибір для гравця
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
        game()


if __name__=='__main__':
    game()