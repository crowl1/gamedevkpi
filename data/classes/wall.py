from data.classes.coordinate import Coordinate


class Wall:
    def __init__(self, coordinates_start, coordinates_end, game_field):
        self.coordinates_start = coordinates_start
        self.coordinates_end = coordinates_end
        self.coordinates_middle = self.set_coordinates_middle()

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
