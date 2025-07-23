from data.data_handler import DataHandler
from strategy.trend_following import TrendFollowingStrategy
from execution.execution_handler import ExecutionHandler
from portfolio.portfolio_handler import PortfolioHandler
from backtest import run_backtest

if __name__ == "__main__":
    dh = DataHandler("data/BTCUSD.csv")
    strategy = TrendFollowingStrategy(short_window=20, long_window=50)
    executor = ExecutionHandler()
    portfolio = PortfolioHandler()

    run_backtest(dh, strategy, portfolio, executor)

    print("Final Portfolio Value:", portfolio.portfolio_value)