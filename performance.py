import matplotlib.pyplot as plt

class Performance:
    def plot_equity_curve(self, portfolio_values):
        plt.figure(figsize = (10, 5)) #width = 10, height = 5
        plt.plot(portfolio_values, linewidth = 2) #creates line graph using portfolio_values
        plt.title("Equity Curve")
        plt.xlabel("Time")
        plt.ylabel("Portfolio Values")
        plt.grid(True)
        plt.show() #to display graph

    def plot_strategy_signals(self, prices, short_ma, long_ma, buy_signals, sell_signals, symbol):
        plt.figure(figsize=(12, 6))
        price_index = range(len(prices))
        short_ma_index = range(len(prices) - len(short_ma), len(prices))
        long_ma_index = range(len(prices) - len(long_ma), len(prices))
        plt.plot(prices, label="Price")
        plt.plot(short_ma_index, short_ma, label = "Short MA")
        plt.plot(long_ma_index, long_ma, label = "Long MA")
        for buy in buy_signals:
            if buy in prices:
                plt.scatter(prices.index(buy), buy, marker = "^", s = 100)
        for sell in sell_signals:
            if sell in prices:
                plt.scatter(prices.index(sell), sell, marker = "v", s = 100)
        plt.title(f"{symbol} Trading Signals")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def calculate_benchmark_curve(self, prices):
        benchmark_values = []
        if len(prices) == 0:
            return []
        initial_price = prices[0]
        initial_capital = 100000
        shares = initial_capital/initial_price
        for price in prices:
            benchmark_value = shares * price
            benchmark_values.append(benchmark_value)
        return benchmark_values

    def plot_strategy_vs_benchmark(self, strategy_curve, benchmark_curve):
        min_length = min(len(strategy_curve), len(benchmark_curve))
        
        strategy_curve = strategy_curve[:min_length]
        benchmark_curve = benchmark_curve[:min_length]
        plt.figure(figsize=(12, 6))
        plt.plot(strategy_curve, label = "Strategy")
        plt.plot(benchmark_curve, label = "Benchmark")
        plt.title("Strategy vs Benchmark")
        plt.xlabel("Time")
        plt.ylabel("Portfolio Values")
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_drawdown_curve(self, portfolio_values): #this is a rolling drawdown curve
        drawdowns = []
        peak = portfolio_values[0]
        for value in portfolio_values:
            if value > peak:
                peak = value
            drawdown = (peak - value)/peak
            drawdowns.append(drawdown)
        plt.figure(figsize = (12, 6))
        plt.plot(drawdowns)
        plt.title("Drawdown Curve")
        plt.xlabel("Time")
        plt.ylabel("Drawdown")
        plt.grid(True)
        plt.show()

    def plot_multiple_equity_curves(self, all_results):
        plt.figure(figsize=(12, 6))
        for result in all_results:
            plt.plot(result["equity_curve"], label = result["strategy"])
        plt.title("Multi-Strategy Comparison")
        plt.xlabel("Time")
        plt.ylabel("Portfolio Value")
        plt.legend()
        plt.grid(True)
        plt.show()


    
