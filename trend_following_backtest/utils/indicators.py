def moving_average(series, window):
    return series.rolling(window=window).mean()

def atr(high, low, close, window):
    tr = (high - low).abs().combine((high - close.shift()).abs(), max).combine((low - close.shift()).abs(), max)
    return tr.rolling(window=window).mean()