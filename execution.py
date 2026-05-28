from event import FillEvent

class ExecutionHandler:
    def execute_order(self, order):
        if order.type == "ORDER":
            fill = FillEvent(
                order.symbol,
                order.direction,
                order.quantity,
                order.price
            )
            return fill