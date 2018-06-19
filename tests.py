import calculator
import unittest

class CanInstantiate(unittest.TestCase):
    def basic_test(self):
        Lulu = calculator.Champion("Lulu")
        self.assertEqual(Lulu.hp_bonus, 0)