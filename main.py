from data.classes.console_tools import game_mode_selection
from data.classes.game import GameField, Player


def game():
    game_field = GameField() # створюємо поле
    first_player = Player(True, 1)
    second_player = Player(False, 2)
    game_mode_selection() #перша лаба, вибір для гравця


if __name__=='__main__':
    game()