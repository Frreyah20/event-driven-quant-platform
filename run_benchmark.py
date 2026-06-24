import csv
from strategy_factory import create_strategy
from backtest_runner import run_backtest

class MockBuyAndHoldStrategy:
    def __init__(self):
        self.in_market = {}

    def calculate_signals(self, event):
        if event.type == "MARKET":
            if not self.in_market.get(event.symbol, False):
                self.in_market[event.symbol] = True
                from event import SignalEvent
                return SignalEvent(event.symbol, "BUY")
        return None

def main():
    csv_files = {
        "AAPL": "data/AAPL_data.csv",
        "MSFT": "data/MSFT_data.csv",
        "GOOG": "data/GOOG_data.csv",
        "AMZN": "data/AMZN_data.csv",
        "SPY": "data/SPY_data.csv"
    }

    strategies = ["buy_and_hold", "ma", "rsi", "momentum", "breakout", "ensemble"]
    
    all_metrics = []

    for strat_name in strategies:
        print(f"Benchmarking strategy: {strat_name}")
        if strat_name == "buy_and_hold":
            strategy = MockBuyAndHoldStrategy()
        else:
            strategy = create_strategy(strat_name)
            
        results = run_backtest(strategy, csv_files, split="test")
        
        equity_curve = results.get("equity_curve", [])
        initial_equity = equity_curve[0] if equity_curve else 100000
        final_equity = equity_curve[-1] if equity_curve else 100000
        total_return = (final_equity / initial_equity) - 1
        
        trade_stats = results.get("trade_statistics", {})
        trade_count = trade_stats.get("total_trades", 0) if trade_stats else 0
        
        all_metrics.append({
            "Strategy": strat_name,
            "Total Return": total_return,
            "Annualized Return": results.get("cagr", 0),
            "Volatility": results.get("volatility", 0),
            "Sharpe Ratio": results.get("sharpe", 0),
            "Max Drawdown": results.get("max_drawdown", 0),
            "Trade Count": trade_count
        })

    # Write CSV
    with open("benchmark_report.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Strategy", "Total Return", "Annualized Return", "Volatility", "Sharpe Ratio", "Max Drawdown", "Trade Count"])
        writer.writeheader()
        writer.writerows(all_metrics)

    # Generate Markdown
    # Sort by Sharpe
    sharpe_sorted = sorted(all_metrics, key=lambda x: x["Sharpe Ratio"], reverse=True)
    return_sorted = sorted(all_metrics, key=lambda x: x["Total Return"], reverse=True)
    drawdown_sorted = sorted(all_metrics, key=lambda x: x["Max Drawdown"])

    best_sharpe = sharpe_sorted[0]["Strategy"]
    best_return = return_sorted[0]["Strategy"]
    lowest_drawdown = drawdown_sorted[0]["Strategy"]

    md_content = "# Strategy Benchmark Report\n\n"
    
    md_content += "## Strategy Highlights\n"
    md_content += f"- **Best Sharpe Strategy:** {best_sharpe}\n"
    md_content += f"- **Best Return Strategy:** {best_return}\n"
    md_content += f"- **Lowest Drawdown Strategy:** {lowest_drawdown}\n\n"
    
    md_content += "## Performance Comparison Table\n\n"
    md_content += "| Strategy | Total Return | Annualized Return | Volatility | Sharpe Ratio | Max Drawdown | Trade Count |\n"
    md_content += "|---|---|---|---|---|---|---|\n"
    for row in all_metrics:
        md_content += f"| {row['Strategy']} | {row['Total Return']:.2%} | {row['Annualized Return']:.2%} | {row['Volatility']:.4f} | {row['Sharpe Ratio']:.4f} | {row['Max Drawdown']:.2%} | {row['Trade Count']} |\n"
        
    md_content += "\n## Ranking by Sharpe Ratio\n"
    for i, row in enumerate(sharpe_sorted, 1):
        md_content += f"{i}. {row['Strategy']} ({row['Sharpe Ratio']:.4f})\n"

    md_content += "\n## Ranking by Total Return\n"
    for i, row in enumerate(return_sorted, 1):
        md_content += f"{i}. {row['Strategy']} ({row['Total Return']:.2%})\n"

    with open("benchmark_report.md", "w") as f:
        f.write(md_content)
        
    print("Benchmarking completed successfully. Outputs generated: benchmark_report.csv, benchmark_report.md")

if __name__ == "__main__":
    main()
