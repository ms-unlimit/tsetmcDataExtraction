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


# def run_func(func):
#     def inner (args):
#         return func(args)
#     return inner

# @run_func
def GetPrice(args):
    df = fpy.Get_Price_History(**args)
    return df


if __name__=="__main__":

    stock_indexing = stockIndexing()
    stk_idx_lst = stock_indexing.stocks_list["Idx"].to_list()

    mongo_builder = MongoBuilder()
    collection = mongo_builder.get_mongodb_collection(collection_name="price")

    query_utils = QueryUtils(collection)

    for stock in stk_idx_lst:
        stk_name = stock_indexing.idx2stock(stock)
        try:
            signal.alarm(30)
            stk_lst_data = query_utils.StockLastData(stk_name)
            if len(stk_lst_data) == 0:
                init_price_args = {'stock':stk_name,'ignore_date':True,'adjust_price':False,'show_weekday':False,'double_date':True}
                df = GetPrice(init_price_args)
                df['Jdate'] = df.index
                query_utils.inserertDF(df)
                print("first inserted: ", stk_name, len(df))
            else:
                stk_lst_date = stk_lst_data[0]['Jdate']
                current_date = jdatetime.date.today()
                if stk_lst_date != str(current_date):
                    start_date = str((jdatetime.datetime.strptime(stk_lst_date, "%Y-%m-%d") + jdatetime.timedelta(days=1)).date())
                    end_date = str(current_date)
                    update_price_args = {'stock':stk_name,'ignore_date':False,'adjust_price':False,'show_weekday':False,'double_date':True, 'start_date':start_date, 'end_date':end_date}
                    df = GetPrice(update_price_args)
                    if len(df) > 0:
                        df['Jdate'] = df.index
                        query_utils.inserertDF(df)
                        print("update: ", stk_name, len(df))
                    else:
                        print("today not found: ", stk_name, len(df))

                else:
                    print(stk_name, " is existing")
        except:
            print(stk_name, " error")



