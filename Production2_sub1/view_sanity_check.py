#===== Standard Library
#===== 3rd party
import pickle
import numpy as np
#===== Reader
from forecast import Forecast
from volatility import Volatility
from portfolio import Portfolio
from ftx_futures_exchange_helper import Ftx_Futures_Exchange_Helper
from recorder import Recorder
#===== 
acc_type='sub1'
trade_tickers_list = ['BTC-PERP', 'ETH-PERP', 'DOGE-PERP', 'DOT-PERP', 'ADA-PERP', 'LTC-PERP', 'BCH-PERP', 'XLM-PERP', 'LINK-PERP', 'UNI-PERP']
helper = Ftx_Futures_Exchange_Helper(acc_type=acc_type)
#===== 
forecast = Forecast(acc_type)
forecasts_dict = {}
forecast1s = np.array([forecast.ema_fast_slow(ticker, 2, 8) for ticker in trade_tickers_list])
forecast2s = np.array([forecast.ema_fast_slow(ticker, 4, 16) for ticker in trade_tickers_list])
forecast3s = np.array([forecast.ema_fast_slow(ticker, 8, 32) for ticker in trade_tickers_list])
forecast1s = forecast1s * (np.abs(forecast3s).sum() / np.abs(forecast1s).sum())
forecast2s = forecast2s * (np.abs(forecast3s).sum() / np.abs(forecast2s).sum())
num = 0
for ticker in trade_tickers_list:
    forecast1 = forecast1s[num] * 0.42
    forecast2 = forecast2s[num] * 0.16
    forecast3 = forecast3s[num] * 0.42
    combined_forecast = (forecast1 + forecast2 + forecast3) * 1.12
    print(ticker, combined_forecast, forecast1, forecast2, forecast3)
    forecasts_dict[ticker] = combined_forecast
    num += 1
print(forecasts_dict)
forecasts_dict = forecast.normalize_forecasts(forecasts_dict)
print(forecasts_dict)
#===== 
volatility = Volatility(acc_type)
vol_scalar_dict = {}
for ticker in trade_tickers_list:
    #volatility_scalar = volatility.volatility_scalar(ticker, 0.0158)
    volatility_scalar = volatility.volatility_scalar(ticker, 0.2)
    vol_scalar_dict[ticker] = volatility_scalar
print("===Volatility Scalars===")
print(vol_scalar_dict)
#===== 
portfolio = Portfolio(acc_type)
positions_dict = portfolio.position_sizing(vol_scalar_dict, forecasts_dict)
print("===Calculated Positions===")
print(positions_dict)
positions_dict = portfolio.round_positions(positions_dict)
print("===Final Positions===")
print(positions_dict)
#===== 
print("===Final Daily Cash Volatility===")
total = 0
for key, val in positions_dict.items():
    total += abs(val) * helper.get_ticker_std(key)
print(total)
#===== 
print("===Required Capital===")
total = 0
for key, val in positions_dict.items():
    total += abs(val) * helper.get_current_price(key)
print(total)
#=====
print("===Current Positions===")
current_position_dict = {}
for ticker in trade_tickers_list:
    current_position_dict[ticker] = helper.get_position(ticker)
print(current_position_dict)
#=====
print("===Action Checklist===")
""" Blah Blah"""
#=====
#=====
print("===HWM Recording===")
recorder = Recorder()
current_balance = helper.get_wallet_balance()
recorded_hwm = recorder.read('main_hwm')
if current_balance > recorded_hwm:
    recorder.record(key='main_hwm', value=current_balance)
    print(f"Updated HWM: {current_balance}")
else:
    print(f"HWM Unchanged: {recorded_hwm}")
    print(f"Current Balance: {current_balance}")