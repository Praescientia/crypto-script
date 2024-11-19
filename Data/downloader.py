#===== Standard Library
from datetime import datetime
#===== 3rd party
#===== Reader
from ftx_helper import Ftx_Helper
from sql_helper import Sql_Helper
#=====
class Downloader:
    def __init__(self, conn):
        self.helper = Ftx_Helper()
        self.sql_helper = Sql_Helper(conn)
    #=====
    def create_hourly_database(self):
        self.sql_helper.create_database(db_name="FTX_HOURLY")
    #=====
    def create_hourly_table(self, ticker):
        column_tuples = [('timestamp', 'int'), ('open', 'double'), ('high', 'double'), ('low', 'double'), ('close', 'double'), ('volume', 'double'), ('time', 'varchar(20)')]
        self.sql_helper.create_table(db_name="FTX_HOURLY", table_name=f"`{ticker}`", column_tuples=column_tuples, primary_key='timestamp')
    #=====
    def download_hourly_ticker(self, ticker):
        kline_df = self.helper.get_kline(ticker, '1h', None, 5000)
        kline_df['time'] = kline_df.index.map(lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
        print(kline_df)