from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

from data.classes.coordinate import Coordinate


class GameField:
    def __init__(self):
        self.field = self.get_start_field()
        self.graph = self.set_graph()

    def game_over(self):
        return True if 1 in self.field[0] or 2 in self.field[-1] else False

    def set_graph(self):
        return Grid(matrix=self.graph_prepare(self.field))

    def path_finder(self, players):
        grid = self.graph
        is_first_player_way = False
        is_second_player_way = False

        for win in players[0].for_win:
            grid.cleanup()
            start = grid.node(
                players[0].current_position.y, players[0].current_position.x)
            end = grid.node(win[1], win[0])

            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            path, runs = finder.find_path(start, end, grid)
            if len(path) >= 2:
                is_first_player_way = True
                break
        for win in players[1].for_win:
            grid.cleanup()
            start = grid.node(
                players[1].current_position.y, players[1].current_position.x)
            end = grid.node(win[1], win[0])

            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            path, runs = finder.find_path(start, end, grid)
            if len(path) >= 2:
                is_second_player_way = True
                break
        if is_first_player_way and is_second_player_way:
            return True
        else:
            return False

    def set_wall(self, wall):
        self.field[wall.coordinates_start.x][wall.coordinates_start.y] = 4
        self.field[wall.coordinates_end.x][wall.coordinates_end.y] = 4
        self.field[wall.coordinates_middle.x][wall.coordinates_middle.y] = 4
        return self.field

    def get_field(self):
        return self.field

    def restore_field(self, old_field):
        self.field = old_field


class Player:
    def __init__(self, player_type, player_number):
        self.player_type = player_type  # False - бот
        self.player_number = player_number
        self.walls_amount = 10
        self.current_position = self._set_start_position()
        self.next_position = None
        self.can_move_here = None
        self.places_to_move = None
        self.action = None
        self.jump_list = None
        self.is_jump = False
        if self.player_number == 2:
            self._for_win = [[16,i] for i in range(0,18,2)]
        else:
            self._for_win = [[0,i] for i in range(0,18,2)]

    def _set_start_position(self):
        return Coordinate(16, 8) if self.player_number == 1 else Coordinate(0, 8)

    def is_win(self):
        if self.player_number == 1:
            if self.current_position.x == 0:
                return True
        if self.player_number == 2:
            if self.current_position.x == 16:
                return True
        return False
