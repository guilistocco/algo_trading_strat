import pandas as pd

class DataHandler:
    def __init__(self, filepath: str):
        self.data = pd.read_csv(filepath, index_col='datetime', parse_dates=True)
        self.current_index = 0

    def get_next_bar(self):
        if self.current_index < len(self.data):
            bar = self.data.iloc[self.current_index]
            self.current_index += 1
            return bar
        else:
            return None