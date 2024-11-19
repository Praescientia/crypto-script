from ftx_futures_exchange_helper import Ftx_Futures_Exchange_Helper as Helper
import numpy as np
helper = Helper(acc_type='sub1')
tickers_list, market_info = helper.get_market_pkg()
for ticker in tickers_list:
    position_qty = helper.get_position(ticker)
    if position_qty is None or position_qty==0:
        continue
    else:
        order_type = 'buy' if np.sign(position_qty) < 0 else 'sell'
        resp = helper.create_marketprice_order(ticker=ticker, qty=abs(position_qty), order_type=order_type, reduce_only=True)
    print(ticker)
