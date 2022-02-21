class GameField:
    def __init__(self):
        self.field = self.get_start_field()
        self.graph = self.set_graph()