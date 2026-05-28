from strategy_factory import create_strategy
from backtest_runner import run_backtest
from performance import Performance

# ---------------------------------------------------
# Market data
# ---------------------------------------------------

csv_files = {
    "AAPL": "data/AAPL_data.csv", #consumer tech
    "MSFT": "data/MSFT_data.csv", #enterprise tech
    "GOOG": "data/GOOG_data.csv", #internet.ads
    "AMZN": "data/AMZN_data.csv", #E-commerce/Cloud
    "SPY": "data/SPY_data.csv" #ETF, like a benchmark
}

# ---------------------------------------------------
# Choose strategy
# ---------------------------------------------------

strategy_name = "ensemble"
strategy = create_strategy(strategy_name)

# ---------------------------------------------------
# Run backtest
# ---------------------------------------------------

results = run_backtest(strategy, csv_files, split="test")

# ---------------------------------------------------
# Print results
# ---------------------------------------------------

print(f"\nStrategy: {strategy_name}")
print(f"Sharpe Ratio: " f"{results['sharpe']:.4f}")
print(f"Max Drawdown: " f"{results['max_drawdown']:.4%}")
print(f"CAGR: " f"{results['cagr']:.4f}")
print(f"Volatility: " f"{results['volatility']:.4f}")
print(f"Calmar Ratio: " f"{results['calmar']:.4f}")

trade_stats = results["trade_statistics"]

print("\n===== Trade Statistics =====")
for key, value in trade_stats.items():
    print(f"{key}: {value}")

# ---------------------------------------------------
# Plotting
# ---------------------------------------------------

performance = Performance()
performance.plot_equity_curve(results
["equity_curve"])
performance.plot_drawdown_curve(results["equity_curve"])