#===== Standard Library
import math
#===== 3rd Party Library
import ccxt
import pandas as pd
#===== Reader Files
#=====
class Ftx_Futures_Exchange_Helper:
    def __init__(self, acc_type):
        if acc_type=='main':
            self.public_key = ""
            self.private_key = ""
        elif acc_type=='sub1':
            self.public_key = ""
            self.private_key = ""
        else:
            print("specify right account type")
        
        if acc_type=='main':
            self.ftx = ccxt.ftx({
                'apiKey':self.public_key,
                'secret':self.private_key,
                'timeout': 30000,
                'enableRateLimit': True,
            })
        elif acc_type=='sub1':
            self.ftx = ccxt.ftx({
                'apiKey':self.public_key,
                'secret':self.private_key,
                'timeout': 30000,
                'enableRateLimit': True,
                'headers': {
                    'FTX-SUBACCOUNT':'BAB',
                }
            })
        else:
            print('specify right acc type')
        resp = self.ftx.private_post_account_leverage({'leverage': 5})
    
    def change_leverage(self, leverage):
        resp = self.ftx.private_post_account_leverage({'leverage': leverage})
        return resp
    
    def get_all_tickers(self):
        tickers_list = [part for part in list(self.ftx.load_markets().keys()) if part.endswith('-PERP')] 
        return tickers_list
    
    def get_market_pkg(self):
        market_info = self.ftx.load_markets()
        tickers_list = [part for part in list(market_info.keys()) if part.endswith('-PERP')]
        return tickers_list, market_info
    
    def create_marketprice_order(self, ticker, qty, order_type, reduce_only=False):
        if order_type=='buy':
            resp = self.ftx.create_market_buy_order(ticker, qty, params={'reduceOnly':reduce_only})
        elif order_type=='sell':
            resp = self.ftx.create_market_sell_order(ticker, qty, params={'reduceOnly':reduce_only})
        else:
            raise Exception('Neither')
        return resp
        
    def get_kline(self, ticker, interval, since, limit):
        if since is not None:
            kline = self.ftx.fetch_ohlcv(symbol=ticker, timeframe=interval, since=since, limit=limit)
        else:
            kline = self.ftx.fetch_ohlcv(symbol=ticker, timeframe=interval, limit=limit)
        kline_df = pd.DataFrame(kline, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume'
        ])
        kline_df['timestamp'] = (kline_df['timestamp'] / 1000).astype(int)
        kline_df = kline_df.set_index('timestamp')
        return kline_df
    
    def get_ma(self, ticker, lookback):
        kline_df = self.get_kline(ticker, '15m', None, lookback * 96)
        ma = kline_df['close'].to_numpy().mean()
        return ma

    def get_custom_ma(self, ticker, lookback_tick_num, tick_type):
        kline_df = self.get_kline(ticker, tick_type, None, lookback_tick_num)
        ma = kline_df['close'].to_numpy().mean()
        return ma

    def get_ticker_std(self, ticker):
        kline_df = self.get_kline(ticker, '1d', None, 25)
        std = kline_df['close'].to_numpy().std()
        return std

    def get_instrument_value_volatility(self, ticker):
        std = self.get_ticker_std(ticker)
        leverage = 1
        return leverage * std
    
    def get_wallet_balance(self):
        return float(self.ftx.fetch_balance()['total']['USD'])
    
    def get_position(self, ticker):
        positions = self.ftx.fetch_positions()
        market = self.ftx.market(ticker)
        indexed = self.ftx.index_by(positions, 'future')
        position = self.ftx.safe_value(indexed, market['id'])
        if position is None:
            return float(0)
        return float(position['netSize'])
    
    def get_position_summary(self):
        position_df = pd.DataFrame(self.ftx.fetch_positions())
        return position_df
    
    def get_orderbook(self, ticker):
        return self.ftx.fetch_order_book(ticker)
    
    def get_current_price(self, ticker):
        return float(self.ftx.fetch_ticker(ticker)['info']['price'])
    
    def cut_price_qty(self, ticker, cashamt, qty, market_info):
        ticker_price = self.get_current_price(ticker)
        ticker_info = market_info[ticker]
        if qty is None:
            qty = cashamt / ticker_price
        if cashamt is None:
            cashamt = qty * ticker_price
        min_qty = ticker_info['precision']['amount']
        min_price = ticker_info['precision']['price']
        qty_precision = int(round(-math.log(min_qty, 10), 0))
        price_precision = int(round(-math.log(min_price, 10), 0))
        new_qty = float(round(qty, qty_precision))
        new_price = float(round(ticker_price, price_precision))
        if ticker_price * new_qty > cashamt:
            new_qty -= 10.0 ** -qty_precision
            new_qty = float(round(new_qty, qty_precision))
        if new_qty < market_info[ticker]['limits']['amount']['min']:
            new_qty = 0
        return new_price, new_qty
