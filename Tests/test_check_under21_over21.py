import unittest

from Projects import BlackJack

hand1 = ['10', '7', '7']
hand2 = ['10', '7', '2']


class TestCheckUnder21(unittest.TestCase):
    def test_check_under21(self):

        result = BlackJack.check_under21(hand1)[0]
        result2 = BlackJack.check_under21(hand1)[1]
        try:
            self.assertTrue(result, 'under21 Should be True')
        except AssertionError:
            self.assertLess(result2, 21, 'under21 Should be less than 21')

    def test_check_over21(self):
        result = BlackJack.check_over21(hand2)[0]
        result2 = BlackJack.check_over21(hand2)[1]
        try:
            self.assertTrue(result, 'over21 Should be True')
        except AssertionError:
            self.assertGreater(result2, 21, 'over21 Should be grater than 21')


if __name__ == '__main__':
    unittest.main()
