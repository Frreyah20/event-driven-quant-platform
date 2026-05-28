class Event: #creates a class Event, class = blueprint for objects
    pass #pass means leave empty for now
    

class MarketEvent(Event): #creates a class MarketEvents that inherits from Event
    def __init__(self,symbol, data): #this is called constructor
        #constructor is a special function that runs automatically when an object is created
        self.type = "MARKET" #type is an attribute, like a piece of data stored in object
        #self means store this data in this object
        self.symbol = symbol
        self.data = data #stores actual data from each row
#inheritance means child class, MarketEvent gets its behaviour from parent class Event

class SignalEvent(Event):
    def __init__(self, symbol, direction, confidence=1.0):
        #symbol and direction are parameters values passed in the constructor
        self.type = "SIGNAL"
        self.symbol = symbol
        self.direction = direction 
        self.confidence = confidence 

class OrderEvent(Event):
    def __init__(self, symbol, direction, quantity, price):
        self.type = "ORDER"
        self.symbol = symbol
        self.direction = direction
        self.quantity = quantity
        self.price = price

class FillEvent(Event):
    def __init__(self, symbol, direction, quantity, price):
         #here quantity is the amout of share order executed
         self.type = "FILL"
         self.symbol = symbol
         self.direction = direction
         self.quantity = quantity 
         self.price = price