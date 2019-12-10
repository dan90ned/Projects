import unittest
from Projects import BlackJack



class Test(unittest.TestCase):
    def test_bet(self):
        balance = 500

        self.assertRaises(BlackJack.bet(balance), ValueError,'ok')
