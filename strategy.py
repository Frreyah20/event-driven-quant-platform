#functions inside class are called methods
from event import SignalEvent
import numpy as np
from base_strategy import BaseStrategy

class Strategy(BaseStrategy):
    def __init__(self, short_window = 3, long_window = 5, stop_loss_percent = 0.05):
        #self.prices = [] #a list, works for a single asset
        self.prices = {} #a dictionary, stores price against symbol, works for multiple assets
        self.in_market = {} #means currently not holding stock
        self.buy_signals = {} #to store price at which buy signal triggered
        self.sell_signals = {} #to store price at which sell signal triggered
        self.short_ma_values = {}
        self.long_ma_values = {}
        self.entry_price = {}
        self.stop_loss_percent = stop_loss_percent
        self.short_window = short_window
        self.long_window = long_window
        self.rsi_values = {}
        self.volatility_values = {}

    def calculate_signals(self, event):
        if event.type == "MARKET":

            close_price = float(event.data['Close'])
            symbol = event.symbol
            #first time seeing symbol
            if symbol not in self.prices:
                self.prices[symbol] = []
                self.short_ma_values[symbol] = []
                self.long_ma_values[symbol] = []
                self.buy_signals[symbol] = []
                self.sell_signals[symbol] = []
                self.in_market[symbol] = False
                self.entry_price[symbol] = None
                self.rsi_values[symbol] = []
                self.volatility_values[symbol] = []
            self.prices[symbol].append(close_price)
            print(f"Current close price {symbol}: {close_price}")

            if len(self.prices[symbol]) >= self.long_window:
                #print("Enough prices collected")
                #short_ma = sum(self.prices[symbol][-3:])/3 #-3: last three elements of list
                short_ma = (sum(self.prices[symbol][-self.short_window:])/self.short_window)
                long_ma = (sum(self.prices[symbol][-self.long_window:])/self.long_window)
                self.short_ma_values[symbol].append(short_ma)
                self.long_ma_values[symbol].append(long_ma)

                print(f"{symbol} Short ma:{short_ma}")
                print(f"{symbol} long ma: {long_ma}")

                #stop loss logic
                if self.in_market[symbol]:
                    stop_price = self.entry_price[symbol] * (1-self.stop_loss_percent)
                    #print(f"Stop price: {stop_price}")
                    if close_price <= stop_price:
                        print(f"STOP LOSS TRIGGERED for {symbol}")
                        self.in_market[symbol] = False
                        signal = SignalEvent(symbol, "SELL")
                        return signal
                
                #RSI 
                changes = []
                for i in range(1, len(self.prices[symbol])):
                    change = self.prices[symbol][i] - self.prices[symbol][i-1]
                    changes.append(change)
                gains = []
                losses = []
                for change in changes[-14:]: #classic rsi uses 14 period window
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

                #Volatility
                returns = []
                recent_prices = self.prices[symbol][-15:]
                for i in range (1, len(recent_prices)):
                    daily_returns = (
                        recent_prices[i]
                        - recent_prices[i-1]
                    )/recent_prices[i-1]
                    returns.append(daily_returns)
                volatility = np.std(returns)
                self.volatility_values[symbol].append(volatility)
                print(f"{symbol} Volatility: {volatility}")

                
                
                #BUY SIGNAL
                print(
                f"{symbol} Volatility Filter: "
                f"{volatility < 0.02}"
                )
                if short_ma>long_ma and rsi < 70 and volatility < 0.02 and not self.in_market[symbol]: #“Trend is bullish, but don't buy if already overheated.”
                    print(f"BUY SIGNAL for {symbol}")
                    self.entry_price[symbol] = close_price
                    self.in_market[symbol] = True
                    self.buy_signals[symbol].append(close_price) #appending the price in the buy signal list
                    signal = SignalEvent(symbol, "BUY")
                    return signal
                
                #SELL SIGNAL
                elif ((short_ma<long_ma or rsi > 70) and self.in_market[symbol]): #“Trend is bearish, or overbought, exit the position”
                    print(f"SELL SIGNAL for {symbol}")
                    self.in_market[symbol] = False
                    self.sell_signals[symbol].append(close_price)
                    signal = SignalEvent(symbol, "SELL")
                    return signal

                