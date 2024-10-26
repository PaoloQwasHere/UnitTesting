import unittest

from src.calculator import sum, substract, multi, division
class CalculatorTests(unittest.TestCase):

    def test_sum(self):
        assert sum(2, 3) == 5
    
    def test_substract(self):
        assert substract(10 , 5) == 5
    
    def test_multi(self):
        assert multi(10 , 5) == 50

    def test_division(self):
        assert division(5 , 1) == 5

    def test_division_by_Zero(self):
        with self.assertRaises(ValueError):
            division (10, 0)

