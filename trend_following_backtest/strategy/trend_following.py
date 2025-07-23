class TrendFollowingStrategy:
    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, data: pd.DataFrame):
        short_ma = data['close'].rolling(window=self.short_window).mean()
        long_ma = data['close'].rolling(window=self.long_window).mean()
        signal = (short_ma > long_ma).astype(int).diff().fillna(0)
        return signal  # 1: buy, -1: sell, 0: hold