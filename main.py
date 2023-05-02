from tsetmcExtractor import priceExtractor
import finpy_tse as fpy

if __name__=="__main__":
    p_e = priceExtractor(collection_name='price')
    p_e.run()


