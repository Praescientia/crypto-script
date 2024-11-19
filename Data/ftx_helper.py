#===== Standard Library
import math
#===== 3rd Party Library
import ccxt
import pandas as pd
#===== Reader Files
#=====
class Ftx_Helper:
    def __init__(self):
        # SUB1 SUBACCOUNT
        self.public_key = ""
        self.private_key = ""
        
        self.ftx = ccxt.ftx({
            'apiKey':self.public_key,
            'secret':self.private_key,
            'timeout': 30000,
            'enableRateLimit': True,
            'headers': {
                'FTX-SUBACCOUNT':'BAB',
            }
        })

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
