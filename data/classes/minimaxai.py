import copy

from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

from data.classes.coordinate import Coordinate
from data.classes.wall import Wall


def get_all_moves(game_field, first_player, second_player, path):
    game_fields = []
    temp_field = copy.deepcopy(game_field)
    temp_player = copy.deepcopy(first_player)
    temp_second_player = copy.deepcopy(second_player)
    temp_player.set_places_to_move(game_field, [temp_player, temp_second_player])
    index = get_all_step(temp_player, path)
    temp_player.set_next_position(temp_player.places_to_move[index])
    if temp_player.can_move_here:
        temp_field.move_player(temp_player)
        game_fields.append(
            (temp_field, temp_player, temp_second_player, temp_player.next_position))
    return game_fields


def get_all_step(player, path):
    ind = -1
    for index, step in enumerate(player.places_to_move):
        if step.x == path[2][1] and step.y == path[2][0]:
            ind = index
            break

    return ind


def get_all_walls(game_field, player_one, player_two, path_to_win):
    game_fields = []
    if player_one.walls_amount > 0:
        walls = []
        del path_to_win[0::2]
        for wall in path_to_win:
            if wall[0] % 2 == 0:
                if wall[0] - 2 >= 0:
                    walls.append(Wall(Coordinate(wall[1], wall[0]), Coordinate(
                        wall[1], wall[0] - 2), game_field))
                if wall[0] + 2 <= 16:
                    walls.append(Wall(Coordinate(wall[1], wall[0]), Coordinate(
                        wall[1], wall[0] + 2), game_field))
            else:
                if wall[1] - 2 >= 0:
                    walls.append(Wall(Coordinate(wall[1], wall[0]), Coordinate(
                        wall[1] - 2, wall[0]), game_field))
                if wall[1] + 2 <= 16:
                    walls.append(Wall(Coordinate(wall[1], wall[0]), Coordinate(
                        wall[1] + 2, wall[0]), game_field))
        game_fields = get_game_fields(
            walls, game_field, player_one, player_two)

    return game_fields


def get_game_fields(walls, game_field, player_one, player_two):
    game_fields = []
    for wall in walls:
        first = wall.if_there_path_to_win(
            game_field, player_one, player_two, wall)
        second = wall.between_two_pares
        third = wall.is_there_another_wall
        four = wall.is_length_correct
        if first and second and not third and four:
            if first and second and not third and four:
                temp_field = copy.deepcopy(game_field)
                temp_field.set_wall(wall)
                temp_player = copy.deepcopy(player_one)
                temp_player.decrease_wall_amount()
                game_fields.append((temp_field, temp_player, player_two, wall))

    return game_fields


def get_paths_to_win(game_field, player_one, player_two):
    grid = game_field.graph
    paths_for_first = []
    paths_for_second = []
    for win_position in player_one.for_win:
        grid.cleanup()
        start = grid.node(player_one.current_position.y,
                          player_one.current_position.x)
        end = grid.node(win_position[1], win_position[0])

        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        if len(path) >= 2:
            paths_for_first.append(path)
    for win_position in player_two.for_win:
        grid.cleanup()
        start = grid.node(player_two.current_position.y,
                          player_two.current_position.x)
        end = grid.node(win_position[1], win_position[0])

        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        if len(path) >= 2:
            paths_for_second.append(path)

    return paths_for_first, paths_for_second