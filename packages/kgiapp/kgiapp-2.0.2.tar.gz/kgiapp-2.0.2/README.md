# kgiapp

![PyPI](https://img.shields.io/pypi/v/kgiapp)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kgiapp)
![PyPI - Format](https://img.shields.io/pypi/format/kgiapp)
![PyPI - License](https://img.shields.io/pypi/l/kgiapp)
![PyPI - Downloads](https://img.shields.io/pypi/dm/kgiapp)
![contact](https://img.shields.io/badge/凱基證券)

凱基證券程式下單API整合了.net framework 4.5架構下的交易介面，讓使用者可以輕鬆的運用python執行快速下單。

>kgiapp is a securities, futures, option API, which send orders to Concord Securities Group.
This package integrated with .net framework 4.5, and is compatible with Python 3.5+.
It is distributed under the MIT license.

- [Installation](#installation)
    - [Preinstall](#preinstall)
    - [Binaries](#binaries)
- [Quick Starts](#quick-starts)
    - [Login](#login)
- [Place Order](#place-order)
    - [Stock](#stock)
    - [Futures](#futures)
    - [Foreign Futures](#foreign-futures)
- [Register Event](#register-event)
- [Quote](#quote)
- [Reference](#reference)


## Installation
### Preinstall
>API usage needs application in advance. In order to use this package, please contact us.

### Binaries

simply use pip to install
```
pip install kgiapp
```

## Quick Starts
### Login
```python
from kgiapp import TradeAPI

agent = TradeAPI(debug=False)
agent.login("YOUR_PERSON_ID", "YOUR_PASSWORD")
```

## Place Order
### Stock
```python
from kgiapp.Trade import constant

agent.stock_order(action=SecurityAction.NEW_ORDER, broker_no='YOUR_BROKER_NO', account_no='YOUR_ACCOUNT', lot_type=LotType.ROUND_LOT, order_type=OrderType.ORDINARY, 
                  side=Side.BUY, symbol='2330', quantity=1, price=570, price_flag=SecurityPriceFlag.FIX, time_in_force=TimeInForce.ROD, sub_account_no='', agent_id='', order_id='')

```
### Futures
```python
agent.futures_order(action=Action.NEW_ORDER, branch_no='YOUR_BROKER_NO', account_no='YOUR_ACCOUNT', sub_account_no='', market_type=Market.FUTURES, tb_20_code='MXFB1',
                    time_in_force=TimeInForce.ROD, writeoff=WriteOff.OPEN, order_type=PriceFlag.LIMIT, side=Side.BUY, quantity=1, price=15100, web_id='', orig_net_no='', order_id='')


```



## Reference
