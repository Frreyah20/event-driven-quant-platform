from ma_strategy import MovingAverageStrategy
from rsi_strategy import RSIStrategy
from momentum_strategy import MomentumStrategy
from breakout_strategy import BreakoutStrategy
from ensemble_strategy import EnsembleStrategy

def create_strategy(strategy_name, short_window = 3, long_window =5, strategies = None):

    if strategy_name == "ma":
        return MovingAverageStrategy(
            short_window=short_window,
            long_window=long_window,
            stop_loss_percent=0.05
        )

    elif strategy_name == "rsi":
        return RSIStrategy()

    elif strategy_name == "momentum":
        return MomentumStrategy()

    elif strategy_name == "breakout":
        return BreakoutStrategy()
    elif strategy_name == "ensemble":
        return EnsembleStrategy()

    else:

        raise ValueError(
            f"Unknown strategy: {strategy_name}"
        )