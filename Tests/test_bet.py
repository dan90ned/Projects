import unittest
from Projects import BlackJack

player1 = 100


class TestBet(unittest.TestCase):
    def test_bet(self):
        self.assertGreater(BlackJack.bet(), player1, 'alo')
