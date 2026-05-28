import pandas as pd 
from event import MarketEvent

class DataHandler:
    def __init__(self, events, csv_files, split = "train"):
        self.events = events
        self.symbol_data = {}
        self.current_index = 0 #tracks which row are we currently processing
        for symbol, file in csv_files.items():
            data = pd.read_csv(file)
            split_index = int(len(data)*0.7)
            if split == "train": #uses first 70% for training
                data = data.iloc[:split_index]
            elif split == "test": #uses last 30% for testing
                data = data.iloc[split_index:]
            data = data.reset_index(drop = True) #reset index after slicing
            self.symbol_data[symbol] = data.reset_index(drop = True) #store processed data
        

    def stream_next(self):
        for symbol, data in self.symbol_data.items():
            if self.current_index < len(data):
                row = data.iloc[self.current_index] #iloc means select row by index
                market_event = MarketEvent(symbol, row)
                self.events.put(market_event)
        self.current_index += 1 
    
    def continue_backtest(self):
        for data in self.symbol_data.values():
            if self.current_index < len(data):
                return True
        return False