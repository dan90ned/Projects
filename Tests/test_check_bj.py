import unittest
from Projects import BlackJack


class TestCheckBj(unittest.TestCase):
    def test_check_bj(self):
        hand = ['10', '9', '4']

        result = BlackJack.check_bj(hand)[0]
        result2 = BlackJack.check_bj(hand)[1]
        try:
            self.assertEqual(result, 'Should be 21')

        except AssertionError:
            self.assertFalse(result2, 'Should be False')


if __name__ == '__main__':
    unittest.main()
