from data.classes.coordinate import Coordinate


class Wall:
    def __init__(self, coordinates_start, coordinates_end, game_field):
        self.coordinates_start = coordinates_start
        self.coordinates_end = coordinates_end
        self.coordinates_middle = self.set_coordinates_middle()
        self.is_length_correct = self.if_length_correct()
        self.between_two_pares = self._if_between_two_pares(game_field)

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
                           game_field.field[self.coordinates_end.x + 1][self.coordinates_start.y] in [0, 1,
