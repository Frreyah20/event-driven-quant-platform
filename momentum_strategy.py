from base_strategy import BaseStrategy
from event import SignalEvent


class MomentumStrategy(BaseStrategy):

    def __init__(self):
        self.prices = {}
        self.momentum_values = {}
        self.in_market = {}
        self.lookback = 20   # 20-day momentum

    def calculate_signals(self, event):

        if event.type != "MARKET":
            return None

        symbol = event.symbol
        close_price = float(event.data["Close"])

        # Initialize storage for new symbol
        if symbol not in self.prices:
            self.prices[symbol] = []
            self.momentum_values[symbol] = []
            self.in_market[symbol] = False

        # Store latest close price
        self.prices[symbol].append(close_price)

        # Wait until enough data is available
        if len(self.prices[symbol]) < self.lookback:
            return None

        # Calculate momentum
        old_price = self.prices[symbol][-self.lookback]

        momentum = (close_price - old_price) / old_price

        self.momentum_values[symbol].append(momentum)

        print(f"{symbol} Momentum: {momentum}")

        # BUY signal
        if momentum > 0.05 and not self.in_market[symbol]:
            self.in_market[symbol] = True
            return SignalEvent(
                symbol,
                "BUY"
            )

        # SELL signal
        elif momentum < -0.05 and self.in_market[symbol]:
            self.in_market[symbol] = False
            return SignalEvent(
                symbol,
                "SELL"
            )

        return None