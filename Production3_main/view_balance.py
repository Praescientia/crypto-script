from ftx_futures_exchange_helper import Ftx_Futures_Exchange_Helper
helper = Ftx_Futures_Exchange_Helper(acc_type='main')
print(helper.get_wallet_balance())