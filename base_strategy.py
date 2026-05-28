class BaseStrategy:

    def calculate_signals(self, event):

        raise NotImplementedError(
            "Strategy must implement calculate_signals()"
        )