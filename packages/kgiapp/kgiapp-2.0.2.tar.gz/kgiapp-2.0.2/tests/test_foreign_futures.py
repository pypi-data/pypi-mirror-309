
import os, sys, time
from datetime import datetime
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
from kgiapp import FuturesAPI
from kgiapp.Trade.constant import *


agent = FuturesAPI(debug=True)
agent.login(id_no='A125981258', pwd='0000')

time.sleep(3)
agent.foreign_futures_order(action, market_type=Market.FUTURES, branch_no='F004009', account_no='5528687', sub_account_no='', exchange, 
                              symbol, side1=Side.BUY, ComYM1, strike_price1, cp1, symbol2, side2=Side.SELL, ComYM2, strike_price2, cp2,
                              order_type=PriceFlag.LIMIT, daytrade, writeoff=WriteOff.AUTO, time_in_force=TimeInForce.ROD, order_price, stop_price, quantity, isMLeg='N',
                              FCM_idno='', FCM='', FCMAccount='', orig_source='', orig_seq='', orig_net_no='', trade_date='', web_id='', key_in='')
time.sleep(10)