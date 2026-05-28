from base_strategy import BaseStrategy
from event import SignalEvent

class RSIStrategy(BaseStrategy):
    def __init__(self):
        self.prices = {}
        self.rsi_values = {}
        self.in_market = {}

    def calculate_signals(self, event):
        if event.type != "MARKET":
            return None
        symbol = event.symbol
        close_price = float(
            event.data["Close"]
        )
        if symbol not in self.prices:
            self.prices[symbol] = []
            self.rsi_values[symbol] = []
            self.in_market[symbol] = False
        
        self.prices[symbol].append(close_price)
        if len(self.prices[symbol]) < 15:
            return None
        changes = []
        for i in range(1, len(self.prices[symbol])):
            change = self.prices[symbol][i] - self.prices[symbol][i-1]
            changes.append(change)
        gains = []
        losses = []
        for change in changes[-14:]:#classic rsi uses 14 period window
            if change > 0:
                gains.append(change)
            else:
                losses.append(abs(change))
        average_gains = (
            sum(gains)/14
            if len(gains) > 0
            else 0
        )
        average_loss = (
            sum(losses)/14
            if len(losses) > 0
            else 0
        )
        if average_loss == 0:
            rsi = 100
        else:
            rs = average_gains/average_loss
            rsi = 100 - (100/(1+rs))
        self.rsi_values[symbol].append(rsi)
        print(f"{symbol} RSI: {rsi}")

        if rsi < 30 and not self.in_market[symbol]:
            print(f"RSI BUY SIGNAL: {symbol}")
            self.in_market[symbol] = True
            return SignalEvent(symbol, "BUY")

        elif rsi > 70 and self.in_market[symbol]:
            print(f"RSI SELL SIGNAL: {symbol}")
            self.in_market[symbol] = False
            return SignalEvent(symbol, "SELL")
