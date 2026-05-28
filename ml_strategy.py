from base_strategy import BaseStrategy
from event import SignalEvent
import pandas as pd

class MLStrategy(BaseStrategy):
    def __init__(self, model):
        self.model = model
        self.prices = {}
        self.in_,arket = {}

    def calculate_signals(self, event):
        if event.type != "MARKET":
            return None
        symbol = event.symbol
        close_price = float(event.data["Close"])
        if symbol not in self.prices:
            self.prices[symbol] = []
            self.in_market = False
        self.prices[symbol].append(close_price)
        if len(self.prices[symbol]) < 20:
            return None
        prices = pd.Series(self.prices[symbol])
        returns = prices.pct_change().iloc[-1]
        ma_short = (prices.rolling(window=5).mean().iloc[-1])
        ma_long = (prices.rolling(window=20).mean().iloc[-1])
        volatility = prices.pct_change().rolling(window=20).std().iloc[-1]
        momentum = (prices.pct_change(periods=20).iloc[-1])
        features = pd.DataFrame([returns, ma_short, ma_long, volatility, momentum])
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        confidence = probabilities[1]
        print(f"{symbol} ML Prediction: {prediction}, Confidence: {confidence:.4%}")
        if(prediction == 1 and not self.in_market[symbol]):
            print(f"ML BUY SIGNAL: {symbol}")
            self.in_market[symbol] = True
            return SignalEvent(symbol, "BUY", confidence = confidence)
        elif(prediction == 0 and self.in_market[symbol]):
            print(f"ML SELL SIGNAL: {symbol}")
            self.in_market[symbol] = False
            return SignalEvent(symbol, "SELL", confidence = confidence)
        return None