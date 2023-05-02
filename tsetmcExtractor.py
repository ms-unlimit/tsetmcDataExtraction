import finpy_tse as fpy
import pandas as pd
from mongodb.mongoBuilder import MongoBuilder
from mongodb.queryUtils import QueryUtils
from stocks.stocksHandler import stockIndexing
import jdatetime
import signal

def signal_handler(signum, frame):
    raise Exception("Timed out!")
signal.signal(signal.SIGALRM, signal_handler)

class priceExtractor():

    def __init__(self, collection_name):

        self.stock_indexing = stockIndexing()
        self.stk_idx_lst = self.stock_indexing.stocks_list["Idx"].to_list()[500:]

        mongo_builder = MongoBuilder()
        self.collection = mongo_builder.get_mongodb_collection(collection_name=collection_name)

        self.query_utils = QueryUtils(self.collection)


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

    def __initInsert(self, stk_name):
        init_price_args = {'stock':stk_name,'ignore_date':True,'adjust_price':False,'show_weekday':False,'double_date':True}
        df = fpy.Get_Price_History(**init_price_args)
        df['Jdate'] = df.index
        self.query_utils.inserertDF(df)
        print("first inserted: ", stk_name, len(df))

    def __insert(self, stk_name, stk_lst_data):
        stk_lst_date = stk_lst_data[0]['Jdate']
        current_date = jdatetime.date.today()
        if stk_lst_date != str(current_date):
            start_date = str((jdatetime.datetime.strptime(stk_lst_date, "%Y-%m-%d") + jdatetime.timedelta(days=1)).date())
            end_date = str(current_date)
            update_price_args = {'stock':stk_name,'ignore_date':False,'adjust_price':False,'show_weekday':False,'double_date':True, 'start_date':start_date, 'end_date':end_date}
            df = fpy.Get_Price_History(**update_price_args)
            if len(df) > 0:
                df['Jdate'] = df.index
                self.query_utils.inserertDF(df)
                print("update: ", stk_name, len(df))
            else:
                print("today not found: ", stk_name, len(df))
        else:
            print(stk_name, " is existing")

