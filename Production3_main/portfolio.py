#===== Standard Library
#===== 3rd party
import numpy as np
#===== Reader
from ftx_futures_exchange_helper import Ftx_Futures_Exchange_Helper
#=====
class Portfolio:
    def __init__(self, acc_type):
        self.helper = Ftx_Futures_Exchange_Helper(acc_type=acc_type)
    
    def position_sizing(self, vol_scalar_dict, forecasts_dict):
        tickers_list = list(vol_scalar_dict.keys())
        positions = np.fromiter(vol_scalar_dict.values(), dtype=float) * np.fromiter(forecasts_dict.values(), dtype=float)
        positions_dict = {}
        for num in range(len(tickers_list)):
            key = tickers_list[num]
            positions_dict[key] = positions[num]
        return positions_dict
    
    def round_positions(self, positions_dict):
        tickers_list = list(positions_dict.keys())
        _, market_info = self.helper.get_market_pkg()
        new_dict = {}
        for ticker in tickers_list:
            _, qty = self.helper.cut_price_qty(ticker=ticker, qty=abs(positions_dict[ticker]), cashamt=None, market_info=market_info)
            new_dict[ticker] = qty * np.sign(positions_dict[ticker])
        return new_dict