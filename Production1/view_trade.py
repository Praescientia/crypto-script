#===== Standard Library
#===== 3rd party
import numpy as np
#===== Reader
from volatility import Volatility
from recorder import Recorder
from ftx_helper import Ftx_Helper
from tsmom import Tsmom
from calculator import Calculator
#=====
acc_type='sub1'
#=====
helper = Ftx_Helper(acc_type=acc_type)
tsmom = Tsmom(acc_type)
calculator = Calculator(acc_type)
#=====
daily_vol_target = 0.3
wallet_balance = helper.get_wallet_balance()
trade_tickers_list = ['BTC-PERP', 'ETH-PERP', 'DOGE-PERP', 'DOT-PERP', 'ADA-PERP', 'LTC-PERP', 'BCH-PERP', 'XLM-PERP', 'LINK-PERP', 'UNI-PERP']
#                    ,'BNB-PERP', 'SOL-PERP', 'FTM-PERP', 'EOS-PERP', 'FTT-PERP', 'ETC-PERP', 'TRX-PERP', 'SXP-PERP', 'LUNA-PERP', 'CHZ-PERP']
tsmom_period_days = [2, 6, 24]
price_vol_target = wallet_balance * daily_vol_target
#=====
print("===Starting Capital===")
print(wallet_balance)
#=====
print("===Positions Arr===")
positions_arr = np.zeros(len(trade_tickers_list))
for period in tsmom_period_days:
    vol_scalar_dict = {}
    for ticker in trade_tickers_list:
        vol_scalar_dict[ticker] = tsmom.volatility_scalar(period_days=period, ticker=ticker, price_vol_target=price_vol_target)
    forecasts_dict = {}
    for ticker in trade_tickers_list:
        forecasts_dict[ticker] = tsmom.forecast(ticker=ticker, period_days=period)
    positions_arr += np.fromiter(vol_scalar_dict.values(), dtype=float) * (np.fromiter(forecasts_dict.values(), dtype=float) / len(trade_tickers_list))
positions_arr = positions_arr / 3
print(positions_arr)
#=====
print("===Positions Dict===")
positions_dict = {}
for num in range(len(trade_tickers_list)):
    key = trade_tickers_list[num]
    positions_dict[key] = positions_arr[num]
positions_dict = calculator.round_positions(positions_dict)
print(positions_dict)
#=====
print("===Current Positions===")
current_position_dict = {}
for ticker in trade_tickers_list:
    current_position_dict[ticker] = helper.get_position(ticker)
print(current_position_dict)
#=====
print("===Total Invested Cash===")
cash_total = 0
for key, val in positions_dict.items():
    price = helper.get_current_price(key)
    cash_total += abs(val) * price
print(cash_total)
#=====
print("===Action Checklist===")
for ticker in trade_tickers_list:
    if current_position_dict[ticker]==0:
        if np.sign(positions_dict[ticker]) > 0:
            print(f"BUY {ticker}")
            qty = abs(positions_dict[ticker])
            resp = helper.create_marketprice_order(ticker=ticker, qty=qty, order_type='buy', reduce_only=False)
        elif np.sign(positions_dict[ticker]) < 0:
            print(f"SELL {ticker}")
            qty = abs(positions_dict[ticker])
            resp = helper.create_marketprice_order(ticker=ticker, qty=qty, order_type='sell', reduce_only=False)
        else:
            print(f"No delta {ticker}")
    else:
        diff = positions_dict[ticker] - current_position_dict[ticker]
        if abs(diff) > 0.1 * abs(current_position_dict[ticker]):
            _, market_info = helper.get_market_pkg()
            _, qty = helper.cut_price_qty(ticker=ticker, qty=abs(diff), cashamt=None, market_info=market_info)
            if qty == 0:
                print(f"No delta {ticker}")
                continue
            if diff > 0:
                print(f"BUY {ticker}")
                resp = helper.create_marketprice_order(ticker=ticker, qty=qty, order_type='buy', reduce_only=False)
            else:
                print(f"SELL {ticker}")
                resp = helper.create_marketprice_order(ticker=ticker, qty=qty, order_type='sell', reduce_only=False)
        else:
            print(f"No delta {ticker}")
#=====
print("===HWM Recording===")
recorder = Recorder()
current_balance = helper.get_wallet_balance()
recorded_hwm = recorder.read('sub1_hwm')
if current_balance > recorded_hwm:
    recorder.record(key='sub1_hwm', value=current_balance)
    print(f"Updated HWM: {current_balance}")
else:
    print(f"HWM Unchanged: {recorded_hwm}")
    print(f"Current Balance: {current_balance}")
