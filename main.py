from data.classes.game import GameField, Player


def game():
    game_field = GameField() # створюємо поле
    first_player = Player(True, 1)
    second_player = Player(False, 2)  


if __name__=='__main__':
    game()