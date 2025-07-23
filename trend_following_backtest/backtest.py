def run_backtest(data_handler, strategy, portfolio, executor):
    while True:
        bar = data_handler.get_next_bar()
        if bar is None:
            break
        current_data = data_handler.data.iloc[:data_handler.current_index]
        signal = strategy.generate_signal(current_data).iloc[-1]
        executor.execute_order(signal, bar['close'])
        portfolio.update_portfolio(signal, bar['close'])