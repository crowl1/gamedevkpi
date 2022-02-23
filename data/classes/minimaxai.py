import copy
import time

from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from infinity import inf

from data.classes.coordinate import Coordinate
from data.classes.wall import Wall


count = 0


class MinimaxAI:
    def __init__(self, game_field, first_player, second_player, action=None, depth=+inf):
        self.game_field = game_field
        self.first_player = first_player
        self.second_player = second_player
        self.action = action
        self.depth = depth
        self.minimax_eval = None
        self.children = []
        self.parrent = None
        self.player_one_path = None
        self.player_two_path = None


def minimax_ai(obj_minimax, depth, alpha, beta, maximizingPlayer, player_one, player_two):
    global count
    count += 1
    if depth == 0:
        path_first, path_second = get_paths_to_win(
            obj_minimax.game_field, player_one, player_two)  # список шляхів для виграшу
        path_first = min(path_first, key=len)  # min пріоритет для першого
        path_second = min(path_second, key=len)  # min пріоритет для другого
        obj_minimax.player_one_path = path_first
        obj_minimax.player_two_path = path_second

        obj_minimax.minimax_eval = len(
            obj_minimax.player_one_path) - len(obj_minimax.player_two_path)
        return obj_minimax.minimax_eval, obj_minimax

    if type(obj_minimax) != MinimaxAI:
        obj_minimax = MinimaxAI(obj_minimax, player_one,
                                player_two, action=None, depth=depth)
    path_first, path_second = get_paths_to_win(
        obj_minimax.game_field, player_one, player_two)
    path_first = min(path_first, key=len)
    path_second = min(path_second, key=len)
    obj_minimax.player_one_path = path_first
    obj_minimax.player_two_path = path_second
    walls = get_all_walls(obj_minimax.game_field,
                          player_one, player_two, path_second)
    for wall in walls:
        obj_minimax.children.append(
            MinimaxAI(wall[0], wall[1], wall[2], wall[3], depth))
    next_move_one_player = get_all_moves(
        obj_minimax.game_field, player_one, player_two, path_first)
    obj_minimax.children.append(
        MinimaxAI(next_move_one_player[0][0], next_move_one_player[0][1], next_move_one_player[0][2], next_move_one_player[0][3]))

    if maximizingPlayer:
        max_eval = -inf
        for child_local in obj_minimax.children:
            eval, act = minimax_ai(
                child_local, depth - 1, alpha, beta, False, player_two, player_one)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            obj_minimax.minimax_eval = alpha
            if beta <= alpha:
                break
        return max_eval, obj_minimax

    else:
        min_eval = +inf
        for child_local in obj_minimax.children:
            eval, act = minimax_ai(
                child_local, depth - 1, alpha, beta, True, player_one, player_two)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            obj_minimax.minimax_eval = beta
            if beta <= alpha:
                break
        return min_eval, obj_minimax


def get_all_moves(game_field, first_player, second_player, path):
    game_fields = []
    temp_field = copy.deepcopy(game_field)
    temp_player = copy.deepcopy(first_player)
    temp_second_player = copy.deepcopy(second_player)
    temp_player.set_places_to_move(
        game_field, [temp_player, temp_second_player])
    index = get_all_step(temp_player, path)
    temp_player.set_next_position(temp_player.places_to_move[index])
    if temp_player.can_move_here:
        temp_field.move_player(temp_player)
        game_fields.append(
            (temp_field, temp_player, temp_second_player, temp_player.next_position))
    return game_fields


def get_all_step(player, path):
    index = -1
    for index, step in enumerate(player.places_to_move):
        if step.x == path[2][1] and step.y == path[2][0]:
            index = index
            break

    return index


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


def timer(func):
    """
    Декоратор для заміру часу виконання функції.
    """
    def calc_spend_time(*args, **kw):
        start_time = time.time()
        result = func(*args, **kw)
        print(f"Алгоритм думав: {time.time() - start_time} сек.")
        return result

    return calc_spend_time


def run_minimax(field_obj, depth, alpha, beta, maxPlayer, first_player, second_player):
    eval, acting = minimax_ai(field_obj, depth, alpha, beta,
                              maxPlayer, first_player, second_player)
    global count
    count = 0
    for kid in acting.children:
        if kid.minimax_eval == eval:
            return kid.action
