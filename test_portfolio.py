import unittest
import numpy as np
from portfolio import Portfolio

class TestPortfolioSharpeRatio(unittest.TestCase):
    def setUp(self):
        self.portfolio = Portfolio()

    def test_positive_returns(self):
        self.portfolio.all_portfolio_values = [100.0, 101.0, 103.02]
        sharpe = self.portfolio.calculate_sharpe_ratio()
        expected = (0.015 / 0.005) * np.sqrt(252)
        self.assertAlmostEqual(sharpe, expected, places=5)

    def test_negative_returns(self):
        self.portfolio.all_portfolio_values = [100.0, 99.0, 97.02]
        sharpe = self.portfolio.calculate_sharpe_ratio()
        expected = (-0.015 / 0.005) * np.sqrt(252)
        self.assertAlmostEqual(sharpe, expected, places=5)

    def test_zero_volatility(self):
        self.portfolio.all_portfolio_values = [100.0, 101.0, 102.01]
        sharpe = self.portfolio.calculate_sharpe_ratio()
        self.assertEqual(sharpe, 0)

    def test_empty_returns(self):
        self.portfolio.all_portfolio_values = [100.0] 
        sharpe = self.portfolio.calculate_sharpe_ratio()
        self.assertEqual(sharpe, 0)

        self.portfolio.all_portfolio_values = []
        sharpe = self.portfolio.calculate_sharpe_ratio()
        self.assertEqual(sharpe, 0)

if __name__ == '__main__':
    unittest.main()
