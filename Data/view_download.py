#===== Standard Library
#===== 3rd party
import pymysql
#===== Reader
from downloader import Downloader
#=====
conn = pymysql.connect( user='root',
                        password='',
                        host='localhost',
                        cursorclass=pymysql.cursors.DictCursor)
#=====                
downloader = Downloader(conn)
downloader.create_hourly_database()
downloader.create_hourly_table('BTC-PERP')
downloader.download_hourly_ticker('BTC-PERP')
#=====