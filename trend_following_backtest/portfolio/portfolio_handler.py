class PortfolioHandler:
    def __init__(self, initial_cash=100000):
        self.cash = initial_cash
        self.position = 0
        self.portfolio_value = initial_cash
        self.history = []

    def update_portfolio(self, signal, price):
        if signal == 1:  # buy
            self.position = self.cash // price
            self.cash -= self.position * price
        elif signal == -1:  # sell
            self.cash += self.position * price
            self.position = 0
        self.portfolio_value = self.cash + self.position * price
        self.history.append(self.portfolio_value)