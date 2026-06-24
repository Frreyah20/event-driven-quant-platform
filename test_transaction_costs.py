import unittest
from event import FillEvent
from portfolio import Portfolio

class TestTransactionCosts(unittest.TestCase):
    def test_no_trade_scenario(self):
        portfolio = Portfolio(initial_capital=100000)
        # Snapshot without any trades
        portfolio.snapshot_portfolio_value()
        
        self.assertEqual(portfolio.total_transaction_costs, 0)
        self.assertEqual(portfolio.all_portfolio_values[0], 100000)
        self.assertEqual(portfolio.all_gross_portfolio_values[0], 100000)

    def test_long_entry_fixed_commission(self):
        portfolio = Portfolio(initial_capital=100000, commission=5, slippage_percent=0.001, commission_type="fixed")
        
        # Buy 10 shares at $100
        fill = FillEvent("AAPL", "BUY", 10, 100.0)
        portfolio.update_fill(fill)
        
        # Slippage: 100 * 0.001 = 0.10. Execution price: 100.10
        # Trade value: 10 * 100.10 = 1001.0
        # Commission: 5
        # Total cost deducted from cash: 1006.0
        # Cash remaining: 100000 - 1006 = 98994.0
        # Total transaction costs: slippage (0.10 * 10 = 1.0) + commission (5) = 6.0
        
        self.assertAlmostEqual(portfolio.cash, 98994.0)
        self.assertAlmostEqual(portfolio.total_transaction_costs, 6.0)

    def test_long_exit_percentage_commission(self):
        portfolio = Portfolio(initial_capital=100000, commission=0.01, slippage_percent=0.001, commission_type="percentage")
        
        # Fake having a position
        portfolio.positions["AAPL"] = 10
        portfolio.entry_prices["AAPL"] = 100.0
        
        # Sell 10 shares at $110
        fill = FillEvent("AAPL", "SELL", 10, 110.0)
        portfolio.update_fill(fill)
        
        # Slippage: 110 * 0.001 = 0.11. Execution price: 109.89
        # Trade value: 109.89 * 10 = 1098.90
        # Commission (1%): 1098.90 * 0.01 = 10.989
        # Revenue added to cash: 1098.90 - 10.989 = 1087.911
        # Total transaction costs: slippage (0.11 * 10 = 1.1) + commission (10.989) = 12.089
        
        self.assertAlmostEqual(portfolio.cash, 100000 + 1087.911, places=3)
        self.assertAlmostEqual(portfolio.total_transaction_costs, 12.089, places=3)

    def test_multiple_trades_gross_vs_net(self):
        portfolio = Portfolio(initial_capital=100000, commission=0.001, slippage_percent=0.0005, commission_type="percentage")
        
        fill1 = FillEvent("AAPL", "BUY", 100, 100.0) # Trade 1
        portfolio.update_fill(fill1)
        
        fill2 = FillEvent("MSFT", "BUY", 50, 200.0) # Trade 2
        portfolio.update_fill(fill2)
        
        # We need current prices to snapshot
        portfolio.current_prices["AAPL"] = 105.0
        portfolio.current_prices["MSFT"] = 202.0
        
        portfolio.snapshot_portfolio_value()
        
        net_val = portfolio.all_portfolio_values[-1]
        gross_val = portfolio.all_gross_portfolio_values[-1]
        
        self.assertTrue(gross_val > net_val)
        self.assertAlmostEqual(gross_val, net_val + portfolio.total_transaction_costs)

if __name__ == '__main__':
    unittest.main()
