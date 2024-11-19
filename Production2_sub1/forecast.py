#===== Standard Library
#===== 3rd party
import numpy as np
#===== Reader
from ftx_futures_exchange_helper import Ftx_Futures_Exchange_Helper as Ftx_Helper
#=====
class Forecast:
    def __init__(self, acc_type):
        self.helper = Ftx_Helper(acc_type=acc_type)
    
    def ema_fast_slow(self, ticker, fast, slow):
        df_fast = self.helper.get_kline(ticker=ticker, interval='1h', since=None, limit=int(24*fast))
        ewma_fast = df_fast['close'].ewm(span=int(24*fast)).mean().iloc[-1]
        df_slow = self.helper.get_kline(ticker=ticker, interval='1h', since=None, limit=int(24*slow))
        ewma_slow = df_slow['close'].ewm(span=int(24*slow)).mean().iloc[-1]
        crossover = ewma_fast - ewma_slow
        std_df = self.helper.get_kline(ticker=ticker, interval='1h', since=None, limit=600)
        std = std_df['close'].ewm(span=864).std().iloc[-1] * np.sqrt(24)
        return crossover / std
    
    def normalize_forecasts(self, forecasts_dict):
        forecasts_arr = np.fromiter(forecasts_dict.values(), dtype=float)
        forecasts_arr = forecasts_arr / np.abs(forecasts_arr).sum()
        new_dict = {}
        for num in range(len(forecasts_dict)):
            key = list(forecasts_dict.keys())[num]
            new_dict[key] = forecasts_arr[num]
        return new_dict
    
    def discretize_forecasts(self, forecasts_dict):
        forecasts_arr = np.fromiter(forecasts_dict.values(), dtype=float)
        forecasts_arr = forecasts_arr * (1 / len(forecasts_arr))
        new_dict = {}
        for num in range(len(forecasts_dict)):
            key = list(forecasts_dict.keys())[num]
            new_dict[key] = forecasts_arr[num]
        return new_dict
