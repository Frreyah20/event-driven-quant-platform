from queue import Queue

from portfolio import Portfolio
from execution import ExecutionHandler
from data_handler import DataHandler


def run_backtest(strategy, csv_files, split = "train"):

    # event queue
    events = Queue()

    # core engine components
    portfolio = Portfolio(
        initial_capital=100000
    )

    execution = ExecutionHandler()

    data_handler = DataHandler(
        events,
        csv_files,
        split=split
    )

    # main event-driven loop
    while data_handler.continue_backtest():

        # stream one bar for all symbols
        data_handler.stream_next()

        # process all events currently in queue
        while not events.empty():

            event = events.get()

            # MARKET EVENT
            if event.type == "MARKET":

                # update latest market prices
                portfolio.update_market_value(event)
                if hasattr(strategy, "prices"):
                    if event.symbol in strategy.prices:
                        portfolio.update_asset_volatility(event.symbol, strategy.prices[event.symbol]) 

                # ask strategy for signal
                signal = strategy.calculate_signals(
                    event
                )

                # if strategy generated signal
                if signal is not None:

                    events.put(signal)

            # SIGNAL EVENT
            elif event.type == "SIGNAL":

                order = portfolio.generate_order(
                    event
                )

                if order is not None:

                    events.put(order)

            # ORDER EVENT
            elif event.type == "ORDER":

                fill = execution.execute_order(
                    event
                )

                if fill is not None:

                    events.put(fill)

            # FILL EVENT
            elif event.type == "FILL":

                portfolio.update_fill(event)

        # snapshot portfolio ONCE per timestep
        portfolio.snapshot_portfolio_value()

    trade_statistics = (portfolio.calculate_trade_statistics())

    # final performance results
    results = {
        "equity_curve":
            portfolio.all_portfolio_values,
        "sharpe":
            portfolio.calculate_sharpe_ratio(),
        "max_drawdown":
            portfolio.calculate_maximum_drawdown(),
        "cagr":
            portfolio.calculate_cagr(),
        "volatility":
            portfolio.calculate_volatility(),
        "calmar":
            portfolio.calculate_calmar_ratio(),
        "trade_statistics": trade_statistics,
        "returns":
            portfolio.calculate_returns()
    }

    return results