from strategy_factory import create_strategy
from backtest_runner import run_backtest
from performance import Performance

# ---------------------------------------------------
# Market data files
# ---------------------------------------------------

csv_files = {
    "AAPL": "data/AAPL_data.csv",
    "MSFT": "data/MSFT_data.csv",
    "GOOG": "data/GOOG_data.csv",
    "AMZN": "data/AMZN_data.csv",
    "SPY": "data/SPY_data.csv"
}

# ---------------------------------------------------
# Strategies to compare
# ---------------------------------------------------

strategy_names = ["ma", "rsi", "momentum", "breakout"]

# ---------------------------------------------------
# Run comparison
# ---------------------------------------------------

all_results = []
performance = Performance()
for strategy_name in strategy_names:
    print(f"\nRunning strategy: "f"{strategy_name}")
    strategy = create_strategy(strategy_name)
    results = run_backtest(strategy, csv_files, split="test")
    all_results.append({
        "strategy":
            strategy_name,
        "sharpe":
            results["sharpe"],
        "max_drawdown":
            results["max_drawdown"],
        "equity_curve":
            results["equity_curve"]
    })

# ---------------------------------------------------
# Print results
# ---------------------------------------------------

print("\n===== Strategy Comparison =====")
for result in all_results:
    print(
        f"\nStrategy: "
        f"{result['strategy']}"
    )
    print(
        f"Sharpe Ratio: "
        f"{result['sharpe']:.4f}"
    )
    print(
        f"Max Drawdown: "
        f"{result['max_drawdown']:.4%}"
    )

performance.plot_multiple_equity_curves(all_results)