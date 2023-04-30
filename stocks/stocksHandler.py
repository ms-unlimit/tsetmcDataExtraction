import pandas as pd
from pathlib import Path

class stockIndexing:
    def __init__(self):
        stocks_list_file_path = Path(__file__).parent.joinpath("stockList.csv")
        self.stocks_list = pd.read_csv(stocks_list_file_path)

    def stock2idx(self, stock):
        try:
            return self.stocks_list[self.stocks_list["Ticker"] == stock]["Idx"].to_list()[0]
        except:
            return "not found"

    def idx2stock(self, idx):
        try:
            return self.stocks_list[self.stocks_list["Idx"] == idx]["Ticker"].to_list()[0]
        except:
            return "not found"

    def update(self):
        pass

    def add(self):
        pass

    def remove(self):
        pass
