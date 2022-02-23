import unittest
from data.classes.game import GameField
from data.classes.coordinate import Coordinate

class TestGameField(unittest.TestCase):
    def test_field_preparation(self):
        test_list = [[0,0,0,0,0,0,0,0,2],[0,0,0,0,0,0,0,0,1]]

        self.assertEqual(GameField.field_preparation(test_list), test_list)


class TestCoordinate(unittest.TestCase):
    def test_is_correct(self):
        coordinate = Coordinate(1,1)

        self.assertTrue(coordinate.is_correct)
    
    def test_0_is_in(self):
        coordinate = Coordinate(1,1)
        coordinates = [coordinate]

        self.assertEqual(coordinate.is_in(coordinates), 1)
    
    def test_1_is_in(self):
        coordinate = Coordinate(1,1)
        coordinate_2 = Coordinate(2,2)
        coordinates = [coordinate_2, coordinate]

        self.assertEqual(coordinate.is_in(coordinates), 2)
    
    def test_2_is_in(self):
        coordinate = Coordinate(1,1)
        coordinates = []

        self.assertIsNone(coordinate.is_in(coordinates))