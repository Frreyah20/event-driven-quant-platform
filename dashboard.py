import streamlit as st
import matplotlib.pyplot as plt

from strategy_factory import create_strategy
from backtest_runner import run_backtest
from performance import Performance


# ---------------------------------------------------
# Page Title
# ---------------------------------------------------

st.title(
    "Quant + ML Backtesting Dashboard"
)


# ---------------------------------------------------
# Strategy Selection
# ---------------------------------------------------

strategy_name = st.selectbox(

    "Choose Strategy",

    [
        "ma",
        "rsi",
        "momentum",
        "breakout",
        "ensemble"
    ]
)


# ---------------------------------------------------
# Market Data Files
# ---------------------------------------------------

csv_files = {

    "AAPL": "data/AAPL_data.csv",

    "MSFT": "data/MSFT_data.csv",

    "GOOG": "data/GOOG_data.csv",

    "AMZN": "data/AMZN_data.csv",

    "SPY": "data/SPY_data.csv"
}


# ---------------------------------------------------
# Run Button
# ---------------------------------------------------

run_button = st.button(
    "Run Backtest"
)


# ---------------------------------------------------
# Main Execution
# ---------------------------------------------------

if run_button:

    # -----------------------------------------------
    # Create Strategy
    # -----------------------------------------------

    strategy = create_strategy(
        strategy_name
    )


    # -----------------------------------------------
    # Run Backtest
    # -----------------------------------------------

    results = run_backtest(

        strategy,

        csv_files,

        split="test"
    )


    # -----------------------------------------------
    # Performance Metrics
    # -----------------------------------------------

    st.subheader(
        "Performance Metrics"
    )

    st.write(
        f"Sharpe Ratio: "
        f"{results['sharpe']:.4f}"
    )

    st.write(
        f"Max Drawdown: "
        f"{results['max_drawdown']:.4%}"
    )

    st.write(
        f"CAGR: "
        f"{results['cagr']:.4%}"
    )

    st.write(
        f"Volatility: "
        f"{results['volatility']:.4%}"
    )

    st.write(
        f"Calmar Ratio: "
        f"{results['calmar']:.4f}"
    )


    # -----------------------------------------------
    # Trade Statistics
    # -----------------------------------------------

    trade_stats = results[
        "trade_statistics"
    ]

    st.subheader(
        "Trade Statistics"
    )

    for key, value in trade_stats.items():

        if isinstance(value, float):
            st.write(f"{key}: {value:.2f}")

        else:
            st.write(f"{key}: {value}")


    # -----------------------------------------------
    # Equity Curve
    # -----------------------------------------------

    st.subheader(
        "Equity Curve"
    )

    fig, ax = plt.subplots()

    ax.plot(
        results["equity_curve"]
    )

    ax.set_title(
        "Equity Curve"
    )

    ax.set_xlabel(
        "Time"
    )

    ax.set_ylabel(
        "Portfolio Value"
    )

    ax.grid(True)

    st.pyplot(fig)


    # -----------------------------------------------
    # Drawdown Curve
    # -----------------------------------------------

    drawdowns = []

    peak = results["equity_curve"][0]

    for value in results["equity_curve"]:

        if value > peak:

            peak = value

        drawdown = (
            peak - value
        ) / peak

        drawdowns.append(drawdown)

    st.subheader(
        "Drawdown Curve"
    )

    fig, ax = plt.subplots()

    ax.plot(drawdowns)

    ax.set_title(
        "Drawdown Curve"
    )

    ax.set_xlabel(
        "Time"
    )

    ax.set_ylabel(
        "Drawdown"
    )

    ax.grid(True)

    st.pyplot(fig)


    # -----------------------------------------------
    # Strategy vs Benchmark
    # -----------------------------------------------
    if hasattr(strategy, "prices"):
        if "SPY" in strategy.prices:

            performance = Performance()

            benchmark_curve = (

            performance.calculate_benchmark_curve(

                strategy.prices["SPY"]
            )
        )

        st.subheader(
            "Strategy vs Benchmark"
        )

        fig, ax = plt.subplots()

        ax.plot(

            results["equity_curve"],

            label="Strategy"
        )

        ax.plot(

            benchmark_curve,

            label="Benchmark"
        )

        ax.set_title(
            "Strategy vs Benchmark"
        )

        ax.set_xlabel(
            "Time"
        )

        ax.set_ylabel(
            "Portfolio Value"
        )

        ax.legend()

        ax.grid(True)

        st.pyplot(fig)