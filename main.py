from tsetmcExtractor import DataExtractor
import finpy_tse as fpy

if __name__=="__main__":

    init_price_args = {'ignore_date':True,'adjust_price':False,'show_weekday':False,'double_date':True}
    update_price_args = {'ignore_date':False,'adjust_price':False,'show_weekday':False,'double_date':True}
    Get_Price_History = fpy.Get_Price_History

    init_IR_args = {'ignore_date':True, 'show_weekday':False, 'double_date':True}
    update_IR_args = {'ignore_date':False, 'show_weekday':False, 'double_date':True}
    Get_IR_History = fpy.Get_RI_History

    p_e = DataExtractor(collection_name='price', Extractor_Func=Get_Price_History, init_args=init_price_args, update_args=update_price_args)
    ir_e = DataExtractor(collection_name='IR', Extractor_Func=Get_IR_History, init_args=init_IR_args, update_args=update_IR_args)

    p_e.start()
    ir_e.start()

    p_e.join()
    ir_e.join()

    print("Price:", p_e.stock_error_list)
    print("IR:", ir_e.stock_error_list)

