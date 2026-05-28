from base_strategy import BaseStrategy
from event import SignalEvent
from ma_strategy import MovingAverageStrategy
from rsi_strategy import RSIStrategy
from momentum_strategy import MomentumStrategy
from breakout_strategy import BreakoutStrategy

class EnsembleStrategy(BaseStrategy):
    def __init__(self):
        self.strategies = [MovingAverageStrategy(), RSIStrategy(), MomentumStrategy(), BreakoutStrategy()]
        self.in_market = {}
    
    def calculate_signals(self, event):
        if event.type != "MARKET":
            return None
        symbol = event.symbol
        if symbol not in self.in_market:
            self.in_market[symbol] = False
        buy_votes = 0
        sell_votes = 0
        for strategy in self.strategies:
            signal = strategy.calculate_signals(event)
            if signal is None:
                continue
            if signal.direction == "BUY":
                buy_votes+=1
            elif signal.direction == "SELL":
                sell_votes+=1
        print(
            f"{symbol} Votes-> "
            f"BUY: {buy_votes}, "
            f"SELL: {sell_votes}"
        )
        if (buy_votes >= 1 and not self.in_market[symbol]):
            self.in_market[symbol] = True
            print(f"ENSEMBLE BUY: {symbol}")
            return SignalEvent(symbol, "BUY")
        elif (sell_votes >= 1 and self.in_market[symbol]):
            self.in_market[symbol] = False
            print(f"ENSEMBLE SELL: {symbol}")
            return SignalEvent(symbol, "SELL")
        


