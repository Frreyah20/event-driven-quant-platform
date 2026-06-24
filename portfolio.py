from event import OrderEvent
import numpy as np

class Portfolio:
    def __init__(self, initial_capital: float = 100_000, 
                 commission: float = 5, #every trade costs 5 rupees or dollars
                 slippage_percent: float = 0.001, #slippage = 0.1%
                 position_size_percent: float = 0.10): #10% portfolio allocation per trade
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.total_portfolio_value = initial_capital
        self.commission = commission
        self.slippage_percent = slippage_percent
        self.position_size_percent = position_size_percent
        self.current_prices: dict[str, float] = {}
        self.positions: dict[str, int] = {}
        self.all_portfolio_values: list[float] = []
        self.completed_trades = []
        self.entry_prices = {}
        self.asset_volatility = {}


    def snapshot_portfolio_value(self) -> float:
        """
        Call ONCE per bar (after the event queue is drained) to record
        total portfolio value: cash + mark-to-market holdings.
        """
        holding_value = self._holding_value()
        total = self.cash + holding_value
        self.total_portfolio_value = total
        self.all_portfolio_values.append(total)
        print(f"  [Portfolio] value={total:.2f}  cash={self.cash:.2f}  "
              f"positions={self.positions}")
        return total
    def _holding_value(self):
        total = 0
        for symbol, quantity in self.positions.items():
            if symbol in self.current_prices:
                total += (quantity *self.current_prices[symbol])

        return total

    def generate_order(self, signal) -> OrderEvent | None:
        if signal.type != "SIGNAL":
            return None 
        if signal.symbol not in self.current_prices:
            return None 
        current_price = self.current_prices[signal.symbol]
        confidence_multplier = (signal.confidence)
        volatility = self.asset_volatility.get(signal.symbol, 0.01) #fallback = 0.01, prevents dividing by 0
        risk_multiplier = 1/volatility
        risk_multiplier = min(risk_multiplier, 5)
        capital_to_use = (self.total_portfolio_value * self.position_size_percent*confidence_multplier * risk_multiplier)
        quantity = int(capital_to_use/current_price)
        if quantity <= 0:
            return None
        order = OrderEvent(
            signal.symbol,
            signal.direction,
            quantity,
            current_price
        )
        return order
    
    def update_fill(self, fill) -> None:
        if fill.direction == "BUY":
            slippage_cost = (fill.price * self.slippage_percent)
            execution_price = (fill.price + slippage_cost)
            cost = (execution_price * fill.quantity) + self.commission
            self.cash -= cost
            self.positions[fill.symbol] = self.positions.get(fill.symbol, 0) + fill.quantity
            self.entry_prices[fill.symbol] = execution_price
            #if fill.symbol in self.positions:
                #self.positions[fill.symbol] += fill.quantity
            #else:
                #self.positions[fill.symbol] = fill.quantity
        
        elif fill.direction == "SELL":
            held = self.positions.get(fill.symbol, 0)
            if held <= 0:
                print(f"  [Portfolio] WARN: SELL received for {fill.symbol} with no position")
            slippage_cost = (fill.price * self.slippage_percent)
            execution_price = (fill.price - slippage_cost)
            revenue = (execution_price * fill.quantity) - self.commission
            entry_price = self.entry_prices[fill.symbol]
            pnl = (execution_price - entry_price) *fill.quantity
            self.cash += revenue
            self.positions[fill.symbol] -= fill.quantity
            if self.positions[fill.symbol] <= 0:
                del self.positions[fill.symbol]
        
            trade = {
                "symbol":fill.symbol,
                "entry_price":entry_price,
                "exit_price":execution_price,
                "quantity":fill.quantity,
                "pnl":pnl
            }
            self.completed_trades.append(trade)

    def update_market_value(self, event):

        symbol = event.symbol

        current_price = float(
        event.data["Close"]
        )

        self.current_prices[symbol] = current_price

    def calculate_returns(self):
        returns = []
        for i in range(1, len(self.all_portfolio_values)):
            previous = self.all_portfolio_values[i-1]
            current = self.all_portfolio_values[i]
            daily_returns = (current - previous)/previous
            returns.append(daily_returns)
        return returns

    def calculate_sharpe_ratio(self):
        """
        Calculates the annualized Sharpe ratio.
        Assumes a risk-free rate of 0% and 252 trading days per year.
        """
        returns = self.calculate_returns()
        if len(returns) == 0:
            return 0
        average_returns = np.mean(returns)
        volatility = np.std(returns)
        if np.isclose(volatility, 0):
            return 0
        sharpe_ratio = (average_returns / volatility) * np.sqrt(252)
        return sharpe_ratio

    def calculate_maximum_drawdown(self):
        portfolio_values = self.all_portfolio_values
        if len(portfolio_values) == 0:
            return 0
        peak = portfolio_values[0]
        max_drawdown = 0
        for value in portfolio_values:
            if value > peak:
                peak = value
            drawdown = (peak - value)/peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        return max_drawdown

    def calculate_cagr(self):
        portfolio_values = self.all_portfolio_values
        initial_value = portfolio_values[0]
        final_value = portfolio_values[-1]
        years = len(portfolio_values)/252
        cagr = (final_value/initial_value)**(1/years) -1
        return cagr

    def calculate_volatility(self):
        returns = self.calculate_returns()
        volatility = np.std(returns) * np.sqrt(252)
        return volatility

    def calculate_calmar_ratio(self):
        cagr = self.calculate_cagr()
        max_drawdown = (self.calculate_maximum_drawdown())
        if max_drawdown == 0:
            return 0
        calmar_ratio = (cagr/max_drawdown)
        return calmar_ratio

    def calculate_trade_statistics(self):
        if len(self.completed_trades) == 0:
            return {}
        pnls = [trade["pnl"] for trade in self.completed_trades]
        winning_trades = [pnl for pnl in pnls if pnl > 0]
        losing_trades = [pnl for pnl in pnls if pnl <= 0]
        win_rate = (len(winning_trades)/len(pnls))
        average_win = (sum(winning_trades)/len(winning_trades)
                       if winning_trades else 0)
        average_loss = (sum(losing_trades)/len(losing_trades)
                       if losing_trades else 0)
        expectancy = (win_rate *average_win + (1-win_rate)*average_loss)
        return{
            "total_trades": len(pnls),
            "win_rate":win_rate,
            "average_win":average_win,
            "average_loss":average_loss,
            "expectancy":expectancy,
        }        

    def update_asset_volatility(self, symbol, prices):
        if len(prices) < 10:
            return
        returns = []
        for i in range(1, len(prices)):
            daily_returns = (prices[i] - prices[i-1])/prices[i-1]
            returns.append(daily_returns)
        volatility = np.std(returns)
        self.asset_volatility[symbol] = volatility   
