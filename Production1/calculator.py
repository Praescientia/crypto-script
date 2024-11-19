#===== Standard Library
#===== 3rd party
import pandas as pd
import statsmodels.api as sm
from scipy import stats
import numpy as np
#===== Reader
from ftx_helper import Ftx_Helper
#=====
class Calculator:
    def __init__(self, acc_type):
        self.helper = Ftx_Helper(acc_type=acc_type)
    
    def round_positions(self, positions_dict):
        tickers_list = list(positions_dict.keys())
        _, market_info = self.helper.get_market_pkg()
        new_dict = {}
        for ticker in tickers_list:
            _, qty = self.helper.cut_price_qty(ticker=ticker, qty=abs(positions_dict[ticker]), cashamt=None, market_info=market_info)
            new_dict[ticker] = qty * np.sign(positions_dict[ticker])
        return new_dict
    