from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from infinity import inf

from data.classes.coordinate import Coordinate
import data.classes.minimaxai as minimaxai
from data.classes.wall import Wall


class AI:
    def __init__(self, act, coord):
        self.action = act
        self.coord = coord

    def move(self, player) -> int:
        for index, step in enumerate(player.places_to_move):
            if step.x == self.coord.x and step.y == self.coord.y:
                return index + 1

    def get_wall(self) -> str:
        return f"{self.coord.coordinates_start.x} {self.coord.coordinates_start.y} {self.coord.coordinates_end.x} {self.coord.coordinates_end.y}"

    @minimaxai.timer
    def choose(self, player, game_field, list_of_players):
        player_two = list_of_players[1] if list_of_players[0].player_number == player.player_number else list_of_players[0]
        bot_doing = minimaxai.run_minimax(game_field, depth=2, alpha=-inf, beta=+
                                         inf, maxPlayer=True, first_player=player, second_player=player_two)
        if type(bot_doing) == Wall or type(bot_doing) == Wall:
            self.action = "2"
            self.coord = bot_doing
        else:
            self.action = "1"
            self.coord = bot_doing
        return self.action

class GameField:
    def __init__(self):
        self.field = self.get_start_field()
        self.graph = self.set_graph()

    def game_over(self) -> bool:
        return True if 1 in self.field[0] or 2 in self.field[-1] else False

    def set_graph(self):
        return Grid(matrix=self.gen_graph(self.field))

    def path_finder(self, players) -> bool:
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

    def move_player(self, player):
        self.field[player.current_position.x][player.current_position.y] = 0
        self.field[player.next_position.x][player.next_position.y] = player.player_number
        player.current_position = player.next_position

    def get_start_field(self):
        return self.field_preparation(self.fill())

    @staticmethod
    def gen_graph(field) -> list:
        temp_field = []
        for i in range(len(field[0])):
            temp_field.append([])
            for j in range(len(field[1])):
                if field[i][j] == 0:
                    temp_field[i].append(100)  # порожня клітка
                elif field[i][j] == 3:
                    temp_field[i].append(100)  # порожня клітка
                elif field[i][j] == 4:
                    temp_field[i].append(0)  # стіна
                elif field[i][j] == 5:
                    temp_field[i].append(0)  # стіна
                elif field[i][j] == 1:
                    temp_field[i].append(49)  # геймер
                elif field[i][j] == 2:
                    temp_field[i].append(49)  # геймер

        return temp_field

    @staticmethod
    def get_conn_points(field) -> list:
        conn_points = []
        for i in range(0, len(field), 2):
            for j in range(0, len(field[i]), 2):
                if i != len(field) - 1 and j != len(field) - 1:
                    if field[i][j + 1] == 3:
                        conn_points.append(
                            ((i / 2, j / 2), (i / 2, (j + 2) / 2)))
                    if field[i + 1][j] == 3:
                        conn_points.append(
                            ((i / 2, j / 2), ((i + 2) / 2, j / 2)))
                else:
                    if i == len(field) - 1 and j != len(field) - 1:
                        if field[i][j + 1] == 3:
                            conn_points.append(
                                ((i / 2, j / 2), (i / 2, (j + 2) / 2)))
                    if j == len(field) - 1 and i != len(field) - 1:
                        if field[i + 1][j] == 3:
                            conn_points.append(
                                ((i / 2, j / 2), ((i + 2) / 2, j / 2)))
        return conn_points

    @staticmethod
    def fill() -> list:
        field = []

        for row_index in range(9):
            if row_index != 8:
                row_items = []
                for row_item_index in range(9):
                    if row_item_index != 8:
                        row_items.append(0)
                        row_items.append(3)
                    else:
                        row_items.append(0)
                field.append(row_items)
                field.append([3 for i in range(17)])
            else:
                row_items = []
                for row_item_index in range(9):
                    if row_item_index != 8:
                        row_items.append(0)
                        row_items.append(3)
                    else:
                        row_items.append(0)
                field.append(row_items)
        for i in range(16):
            for j in range(16):
                if i % 2 == 1 and j % 2 == 1:
                    field[i][j] = 5
        return field

    @staticmethod
    def field_preparation(field) -> list:
        center_real = 8
        field[0][center_real] = 2
        field[-1][center_real] = 1
        return field


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

    def is_win(self) -> bool:
        if self.player_number == 1:
            if self.current_position.x == 0:
                return True
        if self.player_number == 2:
            if self.current_position.x == 16:
                return True
        return False

    def decrease_wall_amount(self):
        if self.walls_amount != 0:
            self.walls_amount -= 1

    def increase_wall_amount(self):
        self.walls_amount += 1

    def set_next_position(self, coordinate):
        for places in self.places_to_move:
            if coordinate.is_correct and coordinate.x == places.x and coordinate.y == places.y:
                self.next_position = coordinate
                self.can_move_here = True
                break
            else:
                self.next_position = None
                self.can_move_here = False

    def set_places_to_move(self, game_field, list_of_players=None, list_of_possible_moves=None, another_player=None,
                           flag=False) -> list:
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

    def check_up(self, field) -> bool:
        return True if field[self.current_position.x - 1][self.current_position.y] == 3 else False

    def player_check_up(self, second_player) -> bool:
        if self.current_position.x - 2 == second_player.x and self.current_position.y == second_player.y:
            return True
        return False

    def down(self):
        return Coordinate(self.current_position.x + 2, self.current_position.y)

    def check_down(self, field) -> bool:
        return True if field[self.current_position.x + 1][self.current_position.y] == 3 else False

    def player_check_down(self, second_player) -> bool:
        if self.current_position.x + 2 == second_player.x and self.current_position.y == second_player.y:
            return True
        return False

    def left(self):
        return Coordinate(self.current_position.x, self.current_position.y - 2)

    def check_left(self, field) -> bool:
        return True if field[self.current_position.x][self.current_position.y - 1] == 3 else False

    def player_check_left(self, second_player) -> bool:
        if self.current_position.x == second_player.x and self.current_position.y - 2 == second_player.y:
            return True
        return False

    def right(self):
        return Coordinate(self.current_position.x, self.current_position.y + 2)

    def check_right(self, field) -> bool:
        return True if field[self.current_position.x][self.current_position.y + 1] == 3 else False

    def player_check_right(self, second_player) -> bool:
        if self.current_position.x == second_player.x and self.current_position.y + 2 == second_player.y:
            return True
        return False

    @property
    def for_win(self):
        return self._for_win
