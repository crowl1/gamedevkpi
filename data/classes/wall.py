import copy

from data.classes.coordinate import Coordinate


class Wall:
    def __init__(self, coordinates_start, coordinates_end, game_field):
        self.coordinates_start = coordinates_start
        self.coordinates_end = coordinates_end
        self.coordinates_middle = self.set_coordinates_middle()
        self.is_length_correct = self.if_length_correct()
        self.between_two_pares = self._if_between_two_pares(game_field)
        self.is_there_another_wall = self._if_there_another_wall(
            game_field.field)
        self.is_there_path_to_win = None

    def set_coordinates_middle(self):
        if self.coordinates_start.y == self.coordinates_end.y:
            if self.coordinates_start.x > self.coordinates_end.x:
                return Coordinate(self.coordinates_end.x + 1, self.coordinates_start.y)
            else:
                return Coordinate(self.coordinates_start.x + 1, self.coordinates_start.y)
        else:
            if self.coordinates_start.y > self.coordinates_end.y:
                return Coordinate(self.coordinates_start.x, self.coordinates_end.y + 1)
            else:
                return Coordinate(self.coordinates_start.x, self.coordinates_start.y + 1)

    def if_length_correct(self):
        if self.coordinates_start.x == self.coordinates_end.x:
            if self.coordinates_start.y > self.coordinates_end.y:
                return True if len(
                    [num for num in range(self.coordinates_end.y + 1, self.coordinates_start.y)]) == 1 else False
            else:
                return True if len(
                    [num for num in range(self.coordinates_start.y + 1, self.coordinates_end.y)]) == 1 else False
        elif self.coordinates_start.y == self.coordinates_end.y:
            if self.coordinates_start.x > self.coordinates_end.x:
                return True if len(
                    [num for num in range(self.coordinates_end.x + 1, self.coordinates_start.x)]) == 1 else False
            else:
                return True if len(
                    [num for num in range(self.coordinates_start.x + 1, self.coordinates_end.x)]) == 1 else False
        else:
            return False

    def _if_between_two_pares(self, game_field):
        if self.coordinates_start.y == self.coordinates_end.y:
            return True if game_field.field[self.coordinates_start.x][self.coordinates_start.y - 1] in [0, 1, 2] and \
                           game_field.field[self.coordinates_start.x][self.coordinates_start.y + 1] in [0, 1, 2] and \
                           game_field.field[self.coordinates_start.x][self.coordinates_end.y - 1] in [0, 1, 2] and \
                           game_field.field[self.coordinates_start.x][self.coordinates_end.y + 1] in [0, 1,
                                                                                                      2] else False
        elif self.coordinates_start.x == self.coordinates_end.x:
            return True if game_field.field[self.coordinates_start.x - 1][self.coordinates_start.y] in [0, 1, 2] and \
                           game_field.field[self.coordinates_start.x + 1][self.coordinates_start.y] in [0, 1, 2] and \
                           game_field.field[self.coordinates_end.x - 1][self.coordinates_start.y] in [0, 1, 2] and \
                           game_field.field[self.coordinates_end.x + 1][self.coordinates_start.y] in [0, 1, 2] else False

    def _if_there_another_wall(self, game_field):
        return False if game_field[self.coordinates_start.x][self.coordinates_start.y] == 3 and \
                        game_field[self.coordinates_end.x][self.coordinates_end.y] == 3 and \
                        game_field[self.coordinates_middle.x][self.coordinates_middle.y] == 5 else True

    @staticmethod
    def if_there_path_to_win(game_field, player1, player2, wall):
        game_field.graph.cleanup()
        temp_field = copy.deepcopy(game_field)
        temp_field.set_wall(wall)
        temp_field.graph = temp_field.set_graph()
        if temp_field.path_finder([player1, player2]):
            del temp_field
            return True
        else:
            del temp_field
            return False
