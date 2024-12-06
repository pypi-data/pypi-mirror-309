import os
import sys
import time
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
from kgiapp import TradeAPI
from kgiapp.Trade.constant import *


agent = TradeAPI(debug=False)
agent.login(id_no='A125981258', pwd='2c01cynu')

time.sleep(3)

# agent.stock_order(action=SecurityAction.NEW_ORDER, broker_no='9228', account_no='0002441', lot_type=LotType.ROUND_LOT, order_type=OrderType.ORDINARY, side=Side.BUY,
#                 symbol='2330', quantity=1, price=570, price_flag=SecurityPriceFlag.FIX, time_in_force=TimeInForce.ROD, sub_account_no='', agent_id='', order_id='')
if agent.is_login:
    for acc in agent.get_account_info():
        if acc[2] == 'S':
            broker_no = acc[0]
            account_no = acc[1]
    # logging.debug("Send order by broker_no:{}, account_no:{}".format(broker_no, account_no))
    # agent.stock_order(action=SecurityAction.NEW_ORDER, broker_no=broker_no, account_no=account_no, lot_type=LotType.ROUND_LOT, order_type=OrderType.ORDINARY, side=Side.BUY,
    #                 symbol='6443', quantity=1, price=33.9, price_flag=SecurityPriceFlag.FIX, time_in_force=TimeInForce.ROD, sub_account_no='', agent_id='', order_id='')

    time.sleep(2)
    agent.realized_profit(broker_no=broker_no, account_no=account_no, format_type='D', symbol='', data_type='T', days=60)

    time.sleep(2)
    agent.stock_inventory_summary(broker_no=broker_no, account_no=account_no)

    time.sleep(2)
    agent.balance_statement(broker_no=broker_no, account_no=account_no, format_type='D', symbol='', data_type='T', days=60)


print(eval("TimeInForce.ROD").value)
time.sleep(5)
