import sys


from data.classes.console_tools import Tools, game_mode_selection, send_wall, print_field, send_move, send_jump, print_places_to_move
from data.classes.coordinate import Coordinate
from data.classes.game import GameField, Player
from data.classes.user import User
from data.classes.wall import Wall


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


def build_wall(player, game_field, list_of_players, counter=0):
    Tools.clear_console() #перша лаба
    # print_field(game_field.field) #перша лаба
    if counter < 5:
        if player.walls_amount > 0:
            # place_the_wall_message() #перша лаба
            wall_input = User.enter(player, "wall")
            if wall_input == "back":
                game(player, game_field, list_of_players)
            else:
                coordinates_split = wall_input.split(" ")
                if len(coordinates_split) == 4:
                    try:
                        coordinates = [int(coordinate)
                                       for coordinate in coordinates_split]
                        wall = Wall(Coordinate(coordinates[0], coordinates[1]), Coordinate(
                            coordinates[2], coordinates[3]), game_field)
                        first = wall.if_there_path_to_win(
                            game_field, list_of_players[0], list_of_players[1], wall)
                        second = wall.between_two_pares
                        third = wall.is_there_another_wall
                        if first and second and not third:
                            game_field.set_wall(wall)
                            player.decrease_wall_amount()
                            if player.player_type is False:
                                send_wall(wall)
                        else:
                            build_wall(player, game_field,
                                     list_of_players, counter + 1)
                    except Exception as e:
                        build_wall(player, game_field,
                                 list_of_players, counter + 1)
                else:
                    build_wall(player, game_field, list_of_players, counter + 1)
        else:
            game(player, game_field, list_of_players)


def move_player(player, game_field, list_of_players):
    Tools.clear_console() #перша лаба
    print_field(game_field.field) #перша лаба
    player.set_places_to_move(game_field, list_of_players)
    print_places_to_move(player.places_to_move) #перша лаба
    try:
        move_player_input = User.enter(player, "move")
        if player.action is not None:
            move_player_input = move_player_input.is_in(player.places_to_move)
        if move_player_input == "back":
            game(player, game_field, list_of_players)
        player.set_next_position(
            player.places_to_move[int(move_player_input) - 1])
        if player.can_move_here:
            game_field.move_player(player)
            if player.is_jump and player.player_type is False and player.current_position.is_in(
                    player.jump_list) is not None:
                send_jump(player)
            elif player.player_type is False:
                send_move(player)
            player.is_jump = False
            player.jump_list = None
            player.action = None
        else:
            move_player(player, game_field, list_of_players)
    except Exception as e:
        pass


def game():
    pass


if __name__ == '__main__':
    start_game()
