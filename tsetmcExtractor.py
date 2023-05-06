import finpy_tse as fpy
import pandas as pd
from mongodb.mongoBuilder import MongoBuilder
from mongodb.queryUtils import QueryUtils
from stocks.stocksHandler import stockIndexing
import jdatetime
import signal
import threading

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

        self.stock_error_list = []

    def run(self):

        for stock in self.stk_idx_lst:
            stk_name = self.stock_indexing.idx2stock(stock)
            try:
                signal.alarm(30)
                stk_lst_data = self.query_utils.StockLastData(stk_name)
                if len(stk_lst_data) == 0:
                    self.__initInsert(stk_name)
                else:
                    self.__insert(stk_name, stk_lst_data)
            except:
                print(stk_name, " error")
                self.stock_error_list.append(stk_name)
        return

    def __initInsert(self, stk_name):
        init_args = self.init_args.copy()
        init_args.update({"stock": stk_name})
        df = self.Extractor_Func(**init_args)
        df['Jdate'] = df.index
        self.query_utils.inserertDF(df)
        print("first inserted: ", stk_name, len(df))

    def __insert(self, stk_name, stk_lst_data):
        stk_lst_date = stk_lst_data[0]['Jdate']
        current_date = jdatetime.date.today()
        if stk_lst_date != str(current_date):
            start_date = str((jdatetime.datetime.strptime(stk_lst_date, "%Y-%m-%d") + jdatetime.timedelta(days=1)).date())
            end_date = str(current_date - jdatetime.timedelta(days=1))
            update_args = self.update_args.copy()
            update_args.update({"stock": stk_name, "start_date": start_date, "end_date": end_date})
            df = self.Extractor_Func(**update_args)
            if len(df) > 0:
                df['Jdate'] = df.index
                self.query_utils.inserertDF(df)
                print("update: ", stk_name, len(df))
            else:
                print("today not found: ", stk_name, len(df))
        else:
            print(stk_name, " is existing")

