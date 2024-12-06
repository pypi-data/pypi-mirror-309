
import os, sys, time, logging
from datetime import datetime
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
from kgiapp import TradeAPI
from kgiapp.Trade.constant import *


agent = TradeAPI(debug=False)
agent.login(id_no='A125981258', pwd='2c01cynu')



time.sleep(3)
product_list = agent.conn.GetProcuctBaseList()
print(product_list)

for acc in agent.Account:
    if acc[2]=='F':
        broker_no = acc[0]
        account_no = acc[1]
logging.debug("Send order by broker_no:{}, account_no:{}".format(broker_no, account_no))
agent.futures_order(action=Action.NEW_ORDER, branch_no=broker_no, account_no=account_no, sub_account_no='', market_type=Market.FUTURES, tb_20_code='MXFB1',
                    time_in_force=TimeInForce.ROD, writeoff=WriteOff.OPEN, order_type=PriceFlag.LIMIT, side=Side.BUY, quantity=1, price=15100, web_id='', orig_net_no='', order_id='')

time.sleep(10)