from pathfinding.core.grid import Grid


class GameField:
    def __init__(self):
        self.field = self.get_start_field()
        self.graph = self.set_graph()

    def game_over(self):
        return True if 1 in self.field[0] or 2 in self.field[-1] else False

    def set_graph(self):
        grid = Grid(matrix=self.graph_prepare(self.field))
        return grid
