from typing import List
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
            self._for_win = [[16, i] for i in range(0, 18, 2)]
        else:
            self._for_win = [[0, i] for i in range(0, 18, 2)]

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

    def set_places_to_move(self, game_field, list_of_players=None, list_of_possible_moves=None, another_player=None,
                           flag=False) -> List:
        if not flag:
            if self.player_number == list_of_players[0].player_number:
                another_player = list_of_players[1]
            else:
                another_player = list_of_players[0]
        if not flag:
            list_of_possible_moves = []
        if self.current_position.x - 2 >= 0:  # UP
            if self.check_up(game_field.field):
                if not self.player_check_up(game_field.field, another_player.current_position):
                    list_of_possible_moves.append(self.up())
                elif self.current_position.x - 3 >= 0 and game_field.field[self.current_position.x - 3][self.current_position.y] == 4 and flag is False:
                    self.is_jump = True
                    list_of_possible_moves = another_player.set_places_to_move(game_field,
                                                                               list_of_possible_moves=list_of_possible_moves,
                                                                               another_player=self, flag=True)
                elif self.current_position.x - 4 >= 0 and not game_field.field[self.current_position.x - 3][
                        self.current_position.y] == 4:
                    list_of_possible_moves.append(Coordinate(
                        self.current_position.x - 4, self.current_position.y))
                    self.is_jump = True
                elif self.current_position.x - 2 == 0:
                    self.is_jump = True
                    list_of_possible_moves = another_player.set_places_to_move(game_field,
                                                                               list_of_possible_moves=list_of_possible_moves,
                                                                               another_player=self, flag=True)

        if self.current_position.y + 2 <= 16:  # RIGHT
            if self.check_right(game_field.field):
                if not self.player_check_right(game_field.field, another_player.current_position):
                    list_of_possible_moves.append(self.right())
                elif self.current_position.y + 3 <= 16 and game_field.field[self.current_position.x][self.current_position.y + 3] == 4 and flag is False:
                    self.is_jump = True
                    list_of_possible_moves = another_player.set_places_to_move(game_field,
                                                                               list_of_possible_moves=list_of_possible_moves,
                                                                               another_player=self, flag=True)
                elif self.current_position.y + 4 <= 16 and not game_field.field[self.current_position.x][
                        self.current_position.y + 3] == 4:
                    list_of_possible_moves.append(Coordinate(
                        self.current_position.x, self.current_position.y + 4))
                    self.is_jump = True
                elif self.current_position.y + 2 == 16:
                    self.is_jump = True
                    list_of_possible_moves = another_player.set_places_to_move(game_field,
                                                                               list_of_possible_moves=list_of_possible_moves,
                                                                               another_player=self, flag=True)

        if self.current_position.x + 2 <= 16:  # DOWN
            if self.check_down(game_field.field):
                if not self.player_check_down(game_field.field, another_player.current_position):
                    list_of_possible_moves.append(self.down())
                elif self.current_position.x + 3 <= 16 and game_field.field[self.current_position.x + 3][self.current_position.y] == 4 and flag is False:
                    self.is_jump = True
                    list_of_possible_moves = another_player.set_places_to_move(game_field,
                                                                               list_of_possible_moves=list_of_possible_moves,
                                                                               another_player=self, flag=True)
                elif self.current_position.x + 4 <= 16 and not game_field.field[self.current_position.x + 3][
                        self.current_position.y] == 4:
                    list_of_possible_moves.append(Coordinate(
                        self.current_position.x + 4, self.current_position.y))
                    self.is_jump = True
                elif self.current_position.x + 2 == 16:
                    self.is_jump = True
                    list_of_possible_moves = another_player.set_places_to_move(game_field,
                                                                               list_of_possible_moves=list_of_possible_moves,
                                                                               another_player=self, flag=True)

        if self.current_position.y - 2 >= 0:  # LEFT
            if self.check_left(game_field.field):
                if not self.player_check_left(game_field.field, another_player.current_position):
                    list_of_possible_moves.append(self.left())
                elif self.current_position.y - 3 >= 0 and game_field.field[self.current_position.x][self.current_position.y - 3] == 4 and flag is False:
                    self.is_jump = True
                    list_of_possible_moves = another_player.set_places_to_move(game_field,
                                                                               list_of_possible_moves=list_of_possible_moves,
                                                                               another_player=self, flag=True)
                elif self.current_position.y - 4 >= 0 and not game_field.field[self.current_position.x][
                        self.current_position.y - 3] == 4:
                    list_of_possible_moves.append(Coordinate(
                        self.current_position.x, self.current_position.y - 4))
                    self.is_jump = True

                elif self.current_position.y - 2 == 0:
                    self.is_jump = True
                    list_of_possible_moves = another_player.set_places_to_move(game_field,
                                                                               list_of_possible_moves=list_of_possible_moves,
                                                                               another_player=self, flag=True)

        self.places_to_move = list_of_possible_moves
        if not flag:
            jump_list = [Coordinate(another_player.current_position.x + 2, another_player.current_position.y),
                         Coordinate(another_player.current_position.x -
                                    2, another_player.current_position.y),
                         Coordinate(another_player.current_position.x,
                                    another_player.current_position.y - 2),
                         Coordinate(another_player.current_position.x, another_player.current_position.y + 2)]
            self.jump_list = jump_list
        return list_of_possible_moves

    def up(self):
        return Coordinate(self.current_position.x - 2, self.current_position.y)

    def check_up(self, field):
        return True if field[self.current_position.x - 1][self.current_position.y] == 3 else False

    def player_check_up(self, second_player):
        if self.current_position.x - 2 == second_player.x and self.current_position.y == second_player.y:
            return True
        return False

    def down(self):
        return Coordinate(self.current_position.x + 2, self.current_position.y)

    def check_down(self, field):
        return True if field[self.current_position.x + 1][self.current_position.y] == 3 else False

    def player_check_down(self, second_player):
        if self.current_position.x + 2 == second_player.x and self.current_position.y == second_player.y:
            return True
        return False

    def left(self):
        return Coordinate(self.current_position.x, self.current_position.y - 2)

    def check_left(self, field):
        return True if field[self.current_position.x][self.current_position.y - 1] == 3 else False

    def player_check_left(self, second_player):
        if self.current_position.x == second_player.x and self.current_position.y - 2 == second_player.y:
            return True
        return False

    def right(self):
        return Coordinate(self.current_position.x, self.current_position.y + 2)

    def check_right(self, field):
        return True if field[self.current_position.x][self.current_position.y + 1] == 3 else False

    def player_check_right(self, second_player):
        if self.current_position.x == second_player.x and self.current_position.y + 2 == second_player.y:
            return True
        return False

    @property
    def for_win(self):
        return self._for_win
