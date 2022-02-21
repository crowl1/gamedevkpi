class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_correct = self.is_correct()

    def is_correct(self):
        try:
            return True if 0 <= self.x <= 16 and 0 <= self.y <= 16 else False
        except Exception:
            return False
