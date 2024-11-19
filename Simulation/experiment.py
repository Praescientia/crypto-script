#===== Standard Library
#===== 3rd party
import time
#===== Reader
from ftx_futures_exchange_helper import Ftx_Futures_Exchange_Helper as Helper
#===== 
class Experiment:
    def __init__(self, acc_type):
        self.helper = Helper(acc_type=acc_type)
        self.index_list = [
            '1INCH-PERP', 'ETC-PERP', 'DOT-PERP', 'BCH-PERP', 'XLM-PERP', 'LINK-PERP', 'UNI-PERP'
            'BTC-PERP', 'ETH-PERP', 'DOGE-PERP', 'ADA-PERP', 'LTC-PERP', 'BNB-PERP'
        ]
    
    def get_beta(self, ticker):
        current_time = ( int(time.time()) - 2 * 60 * 60 ) * 1000
        kline_df = self.helper.get_kline(ticker=ticker, interval='1m', since=current_time, limit=60)
        kline_df 
        return kline_df