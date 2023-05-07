import finpy_tse as fpy
import pandas as pd
from mongodb.mongoBuilder import MongoBuilder
from mongodb.queryUtils import QueryUtils
from stocks.stocksHandler import stockIndexing
import jdatetime
import signal
import threading
import time
def signal_handler(signum, frame):
    raise Exception("Timed out!")
signal.signal(signal.SIGALRM, signal_handler)

class DataExtractor(threading.Thread):

    def __init__(self, collection_name, Extractor_Func, init_args, update_args):
        threading.Thread.__init__(self)
        self.Extractor_Func = Extractor_Func
        self.init_args = init_args
        self.update_args = update_args

        self.stock_indexing = stockIndexing()
        self.stk_idx_lst = self.stock_indexing.stocks_list["Idx"].to_list()

        mongo_builder = MongoBuilder()
        self.collection = mongo_builder.get_mongodb_collection(collection_name=collection_name)

        self.query_utils = QueryUtils(self.collection)

    def run(self):
        sleep_time = 2
        stocks_not_found = self.stk_idx_lst
        while (len(stocks_not_found) != 0 and sleep_time < 100):
            stoks_errors = []
            for stock_idx in stocks_not_found:
                stock_name = self.stock_indexing.idx2stock(stock_idx)
                try:
                    signal.alarm(30)
                    stk_lst_data = self.query_utils.StockLastData(stock_name)
                    if len(stk_lst_data) == 0:
                        self.__initInsert(stock_name)
                    else:
                        self.__insert(stock_name, stk_lst_data)
                except:
                    print(stock_name, " error")
                    stoks_errors.append(stock_idx)
            print("errors num: ",len(stoks_errors))
            stocks_not_found = stoks_errors.copy()
            time.sleep(sleep_time)
            sleep_time += 2

        return

    def __initInsert(self, stk_name):
        init_args = self.init_args.copy()
        init_args.update({"stock": stk_name})
        df = self.Extractor_Func(**init_args)
        df['Jal_Date'] = df.index
        df['Index'] = [self.stock_indexing.stock2idx(stk_name)] * len(df)
        self.query_utils.inserertDF(df)
        print("first inserted: ", stk_name)

    def __insert(self, stk_name, stk_lst_data):
        stk_lst_date = stk_lst_data[0]['Jal_Date']
        current_date = jdatetime.date.today()
        if stk_lst_date != str(current_date):
            start_date = str((jdatetime.datetime.strptime(stk_lst_date, "%Y-%m-%d") + jdatetime.timedelta(days=1)).date())
            end_date = str(current_date)
            # end_date = str(current_date - jdatetime.timedelta(days=1))
            update_args = self.update_args.copy()
            update_args.update({"stock": stk_name, "start_date": start_date, "end_date": end_date})
            df = self.Extractor_Func(**update_args)
            if len(df) > 0:
                df['Jal_Date'] = df.index
                df['Index'] = [self.stock_indexing.stock2idx(stk_name)] * len(df)
                self.query_utils.inserertDF(df)
                print("update: ", stk_name)
            else:
                print("no new value : ", stk_name)
        else:
            print(stk_name, " is existing")

