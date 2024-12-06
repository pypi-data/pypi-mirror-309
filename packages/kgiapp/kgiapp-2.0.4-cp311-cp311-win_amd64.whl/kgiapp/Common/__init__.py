import clr
from kgiapp.log import AppLogger
clr.AddReference("System")
from System import Decimal  # noqa

logger = AppLogger().get_logger(__name__)


def package_decode(package):
    # variables = {prop: getattr(package, prop) for prop in dir(package) if not prop.startswith('_') and isinstance(getattr(package, prop), reserved_type)}
    try:
        variables = {}
        for prop in dir(package):
            match prop:
                case 'Market' | 'StockNo' | 'StockName' | 'LastTradeDate' | 'Match_Time' | 'IndCode' | 'StkType' | 'Source' | 'Status':
                    variables[prop] = getattr(package, prop)
                case 'Bull_Price' | 'Ref_Price' | 'Bear_Price':
                    variables[prop] = float(getattr(package, prop).ToString()) / 10000
                case 'BUY_DEPTH' | 'SELL_DEPTH':
                    variables[prop] = [
                        {
                            'PRICE': float(getattr(package, prop)[i].PRICE.ToString()),
                            'QUANTITY': getattr(package, prop)[i].QUANTITY
                        } for i in range(5)
                    ]
                case 'LastMatchPrice' | 'DayHighPrice' | 'DayLowPrice' | 'FirstMatchPrice' | 'Match_Price' | 'ReferencePrice':
                    variables[prop] = float(getattr(package, prop).ToString())
                case 'FirstMatchQty' | 'LastMatchQty' | 'TotalMatchQty' | 'Match_Qty' | 'Total_Qty':
                    variables[prop] = getattr(package, prop)
                case 'COUNT' | 'IndexNo' | 'IndexTime' | 'LatestIndex':
                    variables[prop] = getattr(package, prop)
    except Exception as e:
        logger.error(f"Unable to parse {package.DT}: {e}")
    else:
        logger.debug(f"[{package.DT}] {variables}")
    finally:
        return variables
