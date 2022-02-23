
class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_correct = self.is_correct()

    def is_correct(self) -> bool:
        try:
            return True if 0 <= self.x <= 16 and 0 <= self.y <= 16 else False
        except Exception:
            return False

    def is_in(self, find) -> int: #TODO refactor
        count = 1
        for item in find:
            if item.x == self.x and item.y == self.y:
                return count
            count += 1
        return None
