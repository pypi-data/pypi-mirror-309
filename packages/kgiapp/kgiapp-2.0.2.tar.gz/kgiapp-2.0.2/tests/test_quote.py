
import os
import sys
import time
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
from kgiapp import QuoteAPI


agent = QuoteAPI(debug=False)
time.sleep(1)
agent.login(id_no='A125981258', pwd='2c01cynu')

time.sleep(1)
agent.subscribe("2330", is_match=True, is_depth=True)

time.sleep(1)
agent.subscribe("2330", is_match=True, is_depth=True, is_odd=True)

time.sleep(1)
d = agent.get_t30()
print(d)

time.sleep(1)
agent.get_o30()

time.sleep(1)
agent.get_etf()

agent.get_last_price(stock_no="2330")
time.sleep(1)

agent.get_basic_info(stock_no="2330")

for i in range(20):
    time.sleep(0.5)

agent.conn.Logout()
agent.conn.Finalize()
print('Finished!')
