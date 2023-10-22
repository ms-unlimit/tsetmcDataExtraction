from tsetmcExtractor import DataExtractor
import finpy_tse as fpy

if __name__=="__main__":

    init_price_args = {'ignore_date':True,'adjust_price':False,'show_weekday':True,'double_date':True}
    update_price_args = {'ignore_date':False,'adjust_price':False,'show_weekday':True,'double_date':True}
    Get_Price_History = fpy.Get_Price_History

    init_IR_args = {'ignore_date':True, 'show_weekday':True, 'double_date':True}
    update_IR_args = {'ignore_date':False, 'show_weekday':True, 'double_date':True}
    Get_IR_History = fpy.Get_RI_History

    price_extractor = DataExtractor(collection_name='price', Extractor_Func=Get_Price_History, init_args=init_price_args, update_args=update_price_args)
    ir_extractor = DataExtractor(collection_name='IR', Extractor_Func=Get_IR_History, init_args=init_IR_args, update_args=update_IR_args)

    price_extractor.start()
    ir_extractor.start()

    price_extractor.join()
    ir_extractor.join()

#test2
