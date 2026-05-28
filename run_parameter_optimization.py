from strategy_factory import create_strategy
from backtest_runner import run_backtest

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
# Optimization setup
# ---------------------------------------------------

strategy_name = "ma"
short_windows = [3, 5, 10]
long_windows = [15, 20, 50]
optimization_results = []

# ---------------------------------------------------
# Parameter optimization
# ---------------------------------------------------

for short_window in short_windows:
    for long_window in long_windows:
        if short_window >= long_window:
            continue
        print(
            f"\nTesting MA Strategy: "
            f"short={short_window}, "
            f"long={long_window}"
        )
        strategy = create_strategy(strategy_name,short_window=short_window,long_window=long_window)
        results = run_backtest(strategy,csv_files,split="train")
        optimization_results.append({
            "short_window":
                short_window,
            "long_window":
                long_window,
            "sharpe":
                results["sharpe"],
            "max_drawdown":
                results["max_drawdown"]
        })

# ---------------------------------------------------
# Print optimization results
# ---------------------------------------------------

print("\n===== Optimization Results =====")
for result in optimization_results:
    print(f"\nShort Window: " f"{result['short_window']}")
    print(f"Long Window: " f"{result['long_window']}")
    print(f"Sharpe Ratio: " f"{result['sharpe']:.4f}")
    print(f"Max Drawdown: " f"{result['max_drawdown']:.4%}")

# ---------------------------------------------------
# Best parameter selection
# ---------------------------------------------------
best_result = max(optimization_results, key=lambda x: x["sharpe"])
print("\n===== BEST PARAMETERS =====")
print(f"Short Window: " f"{best_result['short_window']}")
print(f"Long Window: " f"{best_result['long_window']}")

# ---------------------------------------------------
# Test best parameters
# ---------------------------------------------------

best_strategy = create_strategy(
    "ma",
    short_window=
        best_result["short_window"],
    long_window=
        best_result["long_window"]
)

test_results = run_backtest(best_strategy, csv_files, split="test")

# ---------------------------------------------------
# Print test performance
# ---------------------------------------------------

print("\n===== TEST PERFORMANCE =====")
print(f"Sharpe Ratio: " f"{test_results['sharpe']:.4f}")
print(f"Max Drawdown: " f"{test_results['max_drawdown']:.4%}")