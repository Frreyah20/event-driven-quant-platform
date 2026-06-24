# Event-Driven Quant Platform

This is an event-driven backtesting engine I built to learn more about quantitative finance, algorithmic trading, and Python software architecture. I wanted to understand how trading systems process market data and manage portfolios sequentially, rather than just vectorizing operations in pandas.

## What I learned and built
During development, I implemented the core components of an event-driven system:
- **Event Queue:** Processes `MARKET`, `SIGNAL`, `ORDER`, and `FILL` events to mimic a live trading environment.
- **Data Handler:** Simulates real-time market data streaming bar by bar to prevent lookahead bias.
- **Portfolio Management:** Tracks cash, live positions, and calculates equity curves dynamically.
- **Transaction Costs & Slippage:** I added realistic commission modeling (e.g., 0.10% per trade) and slippage adjustments to see how trading fees degrade theoretical performance.

## Strategies I experimented with
I built a modular strategy framework to quickly test different ideas against historical data for assets like AAPL, MSFT, GOOG, AMZN, and SPY:
- **Technical Indicators:** Moving Average Crossover, RSI, Momentum, and Breakout strategies.
- **Machine Learning:** I experimented with a Random Forest classifier (`ml_model.py`) to predict market directions based on engineered features.
- **Ensemble Approach:** I combined multiple signals into an `EnsembleStrategy` to see if aggregating simple technical indicators could yield better risk-adjusted returns.

## Benchmarking & Validation
To rigorously evaluate the strategies, I added several research tools:
- Walk-Forward Validation: I built this to test the machine learning model on rolling time windows. Using a 100-period training window and 20-period testing window, the model achieved an average out-of-sample directional accuracy of approximately 54%, highlighting both the presence of predictive signal and the difficulty of forecasting financial markets.
- **Benchmarking Framework:** I created an automated script (`run_benchmark.py`) to compare all strategies against a simple Buy & Hold baseline. It ranks the strategies by metrics like Sharpe Ratio, Max Drawdown, and Total Return.
- **Performance Analytics:** A dashboard that calculates metrics (CAGR, Volatility) and plots equity curves using `matplotlib`.

## Current Benchmark Results

| Strategy | Sharpe | Max Drawdown |
|-----------|---------|--------------|
| Ensemble | 5.82 | 3.67% |
| MA | 4.46 | 3.67% |
| RSI | 3.67 | 7.73% |
| Breakout | 3.29 | 4.78% |
| Momentum | 2.76 | 5.44% |
| Buy & Hold | 1.35 | 22.64% |

The ensemble strategy achieved the highest risk-adjusted performance on the current dataset, while the moving average strategy produced the lowest drawdown.
These results are specific to the assets, time period, and assumptions used in the backtest and should not be interpreted as evidence of future performance.

## Limitations

This project was built as a learning and research exercise, so it has several limitations:

- Uses historical CSV data rather than live market feeds.
- Uses a simplified execution model.
- Assumes immediate order fills.
- Does not model market impact or liquidity constraints.
- Results are sensitive to the selected assets and time period.

## How to run the project
I structured the repository so that the main components can be easily run and tested from the command line:

```bash
# Run the automated strategy benchmark (outputs to .csv and .md)
python run_benchmark.py

# Compare technical strategies and visualize equity curves
python run_strategy_comparison.py

# Run walk-forward validation on the ML model
python run_walk_forward_validation.py

# Run unit tests to verify portfolio accounting and transaction costs
python -m unittest test_transaction_costs.py
```

Building this project helped me better understand the connection between trading ideas, portfolio management, and software engineering.