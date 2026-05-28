from base_strategy import BaseStrategy
from event import SignalEvent


class BreakoutStrategy(BaseStrategy):

    def __init__(self):

        # stores price history separately for each symbol
        self.prices = {}

        # tracks whether currently holding the asset
        self.in_market = {}

        # stores breakout levels for analysis/plotting
        self.breakout_values = {}

        # number of previous days to check
        self.lookback = 20

    def calculate_signals(self, event):

        # only process market events
        if event.type != "MARKET":

            return None

        symbol = event.symbol

        close_price = float(event.data["Close"])

        print(f"Current close price {symbol}: {close_price}")

        # initialize symbol state first time seen
        if symbol not in self.prices:

            self.prices[symbol] = []

            self.in_market[symbol] = False

            self.breakout_values[symbol] = []

        # store latest price
        self.prices[symbol].append(close_price)

        # need enough data before breakout calculation
        if len(self.prices[symbol]) < self.lookback:

            return None

        # recent window excluding current price
        recent_prices = self.prices[symbol][-self.lookback:-1]

        # highest and lowest prices in recent window
        recent_high = max(recent_prices)

        recent_low = min(recent_prices)

        # store breakout level
        self.breakout_values[symbol].append(recent_high)

        print(f"{symbol} Recent High: {recent_high}")

        print(f"{symbol} Recent Low: {recent_low}")

        # BUY breakout signal
        if (
            close_price > recent_high
            and not self.in_market[symbol]
        ):

            print(f"BREAKOUT BUY: {symbol}")

            self.in_market[symbol] = True

            return SignalEvent(symbol, "BUY")

        # SELL breakdown signal
        elif (
            close_price < recent_low
            and self.in_market[symbol]
        ):

            print(f"BREAKOUT SELL: {symbol}")

            self.in_market[symbol] = False

            return SignalEvent(symbol, "SELL")

        return None