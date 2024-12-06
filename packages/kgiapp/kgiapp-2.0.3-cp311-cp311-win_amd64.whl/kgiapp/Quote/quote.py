# -*- coding: utf-8 -*-
import os
import sys
import time
import clr
import pandas as pd
from io import StringIO
from kgiapp.log import AppLogger
from kgiapp.Common import package_decode
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir_path)
clr.AddReference("System")
clr.AddReference("Package")
clr.AddReference("PushClient")
clr.AddReference("QuoteCom")
from .constant import DataType as DT   # noqa
from System import Decimal   # noqa
from Intelligence import QuoteCom, COM_STATUS, RECOVER_STATUS   # noqa

logger = AppLogger().get_logger(__name__)


class QuoteAPI():

    def __init__(self, debug: bool = False):
        self.RecoverMap = {}

        if debug:
            self.ServerHost = "iquotetest.kgi.com.tw"
            self.ServerPort = 8000
        else:
            self.ServerHost = "quoteapi.kgi.com.tw"
            self.ServerPort = 443

        token = 'b6eb'
        sid = 'API'
        self.conn = QuoteCom(self.ServerHost, self.ServerPort, sid, token)
        self.is_login = False

        # register event handler
        self.conn.OnRcvMessage += self.onQuoteRcvMessage  # 資料接收事件
        self.conn.OnGetStatus += self.onQuoteGetStatus  # 狀態通知事件
        self.conn.OnRecoverStatus += self.onRecoverStatus  # 回補狀態通知

        # 登入
    def login(self, id_no: str, pwd: str):
        self.is_login = False

        # login
        logger.info(f"Login with {id_no}")
        self.conn.Connect2Quote(self.ServerHost, self.ServerPort, id_no, pwd, ' ', "")
        # self.conn.ShowLogin()
        for i in range(100):
            if self.is_login:
                break
            time.sleep(0.1)

        return True

    def subscribe(self, topic: str, is_match: bool = True, is_depth: bool = True, is_odd: bool = False):
        # is_match 成交
        # is_depth 五檔
        # is_odd 零股
        if is_match:
            if is_odd:
                status = self.conn.SubQuotesMatchOdd(topic)
            else:
                status = self.conn.SubQuotesMatch(topic)

            if status < 0:
                logger.info(f"成交:{self.conn.GetSubQuoteMsg(status)}")
        if is_depth:
            if is_odd:
                status = self.conn.SubQuotesDepthOdd(topic)
            else:
                status = self.conn.SubQuotesDepth(topic)

            if status < 0:
                logger.info(f"五檔:{self.conn.GetSubQuoteMsg(status)}")

    def unsubscribe(self, topic: str, is_match: bool = True, is_depth: bool = True, is_odd: bool = False):
        if is_match:
            if is_odd:
                self.conn.UnSubQuotesMatchOdd(topic)
            else:
                self.conn.UnSubQuotesMatch(topic)
        if is_depth:
            if is_odd:
                self.conn.UnSubQuotesDepthOdd(topic)
            else:
                self.conn.UnSubQuotesDepth(topic)

    def get_t30(self):
        status = self.conn.RetriveProductTSE()
        if status < 0:
            logger.info(self.conn.GetSubQuoteMsg(status))
        else:
            logger.info("上市商品檔下載完成")
            list_t30 = self.conn.GetProductListTSC()
            if not list_t30:
                logger.warning("無法取得上市商品列表,可能未連線/未下載!!")
            else:
                logger.info("上市商品列表")
                df = pd.read_csv(StringIO("\n".join(list_t30)), delimiter='|', header=None, index_col=False, names=["StockNo", "StockName", "BullPrice", "RefPrice", "BearPrice", "LastTradingDate", "IndCode", "StkType"])
                df['StockName'] = df['StockName'].str.replace('\u3000', '')
                df['LastTradingDate'] = pd.to_datetime(df['LastTradingDate'], format='%Y%m%d')

                return df.to_dict(orient="records")

    def get_o30(self):
        status = self.conn.RetriveProductOTC()
        if status < 0:
            logger.info(self.conn.GetSubQuoteMsg(status))
        else:
            logger.info("上櫃商品檔下載完成")
            list_o30 = self.conn.GetProductListOTC()
            if not list_o30:
                logger.warning("無法取得上櫃商品列表,可能未連線/未下載!!")
            else:
                logger.info("上櫃商品列表")
                df = pd.read_csv(StringIO("\n".join(list_o30)), delimiter='|', header=None, index_col=False, names=["StockNo", "StockName", "BullPrice", "RefPrice", "BearPrice", "LastTradingDate", "IndCode", "StkType"])
                df['StockName'] = df['StockName'].str.replace('\u3000', '')
                df['LastTradingDate'] = pd.to_datetime(df['LastTradingDate'], format='%Y%m%d')

                return df.to_dict(orient="records")

    def get_etf(self, stock_no: str = "0050"):
        status = self.conn.RetriveETFStock()
        if status < 0:
            logger.info(self.conn.GetSubQuoteMsg(status))
        else:
            logger.info("ETF成份股檔下載完成")
            list_stock = self.conn.GetETFStocks(stock_no)
            if not list_stock:
                logger.warning("無法取得成份股商品列表,可能未連線/未下載!!")
            else:
                logger.info("{}成份股商品列表".format(stock_no))
                df = pd.read_csv(StringIO("\n".join(list_stock)), delimiter='|', dtype=str, header=None, names=['StockETF', 'StockNo', 'Name'])

                return df.to_dict(orient="records")

    def get_warrant(self, market_type: str = "TSE"):
        status = self.conn.RetriveWarrantInfo()
        if status < 0:
            logger.info(self.conn.GetSubQuoteMsg(status))
        else:
            logger.info("上櫃商品檔下載完成")
            list_warrant = self.conn.GetWarrantList(market_type)  # PI30002
            if not list_warrant:
                logger.warning("無法取得權證商品列表,可能未連線/未下載!!")
            else:
                df = pd.read_csv(StringIO("\n".join(list_warrant)), delimiter='|', header=None, names=["StockNo", "StockName", "BullPrice", "RefPrice", "BearPrice", "LastTradingDate", "IndCode", "StkType"])

                return df.to_dict(orient="records")

    def get_last_price(self, stock_no: str, is_odd: bool = False):
        if is_odd:
            status = self.conn.RetriveLastPriceStockOdd(stock_no)
        else:
            status = self.conn.RetriveLastPriceStock(stock_no)
        if status < 0:
            logger.info(self.conn.GetSubQuoteMsg(status))

    def get_basic_info(self, stock_no: str):  # PI30001 基本資料
        package = self.conn.GetProductSTOCK(stock_no)
        if not package:
            logger.info("無法取得該商品明細,可能商品檔未下載或該商品不存在!!")
        else:
            row = package_decode(package=package)

            return row

    def onQuoteRcvMessage(self, sender, package):
        logger.debug(f"{sender} {package}.")
        row = {}
        # if package.TOPIC and package.TOPIC in self.RecoverMap:
        #     self.RecoverMap[package.TOPIC] += 1

        match package.DT:
            case DT.LOGIN:  # P001503
                if package.Code == 0:
                    logger.info("可註冊檔數：" + package.Qnum)
                    if self.conn.QuoteFuture:
                        logger.info("可註冊期貨報價")
                    if self.conn.QuoteStock:
                        logger.info("可註冊證券報價")
            case DT.NOTICE:  # 公告
                logger.info("公告:", package.ToLog())
            case DT.QUOTE_STOCK_T30 | DT.QUOTE_STOCK_MATCH1 | DT.QUOTE_STOCK_MATCH2 | DT.QUOTE_STOCK_MATCH3:  # PI31001
                row = package_decode(package=package)
            case DT.QUOTE_STOCK_DEPTH1 | DT.QUOTE_STOCK_DEPTH2:  # PI31002
                row = package_decode(package=package)
            case DT.QUOTE_LAST_PRICE_STOCK:  # PI30026
                row = package_decode(package=package)
            case DT.QUOTE_ODD_MATCH1 | DT.QUOTE_ODD_MATCH2:  # PI35001
                row = package_decode(package=package)
            case DT.QUOTE_ODD_DEPTH1 | DT.QUOTE_ODD_DEPTH2:  # PI31002
                row = package_decode(package=package)
            case DT.QUOTE_LAST_PRICE_ODD:  # PI30026
                row = package_decode(package=package)
            case DT.QUOTE_STOCK_INDEX1 | DT.QUOTE_STOCK_INDEX2:  # PI31011
                row = package_decode(package=package)
                row['IDX'] = [package.IDX[i].VALUE for i in range(package.COUNT)]
            case DT.QUOTE_STOCK_NEWINDEX1 | DT.QUOTE_STOCK_AVGINDEX:  # PI31021, PI31022
                row = package_decode(package=package)
            case DT.QUOTE_LAST_INDEX1 | DT.QUOTE_LAST_INDEX2:  # PI31026
                row = package_decode(package=package)
                row['IDX'] = [
                    {
                        package.IDX[i].RefIndex,
                        package.IDX[i].FirstIndex,
                        package.IDX[i].LastIndex,
                        package.IDX[i].DayHighIndex,
                        package.IDX[i].DayLowIndex
                    } for i in range(package.COUNT)]
            case _:
                logger.warning(f"{package.DT} not match any case.")
        logger.info(row)

    # 接收KGI QuoteCom API status event
    def onQuoteGetStatus(self, sender, status, msg):
        smsg = bytes(msg).decode('UTF-8', 'strict')
        logger.debug(f"{sender} {status} {msg}.")

        match status:
            case COM_STATUS.LOGIN_READY:
                logger.info(f"登入成功: {sender.Accounts}")
                self.is_login = True
            case COM_STATUS.ACCTCNT_NOMATCH:
                logger.info(f"部份帳號取得失敗: {smsg}")
            case COM_STATUS.LOGIN_FAIL:
                logger.info(f"登入失敗:[{smsg}]")
            case COM_STATUS.LOGIN_UNKNOW:
                logger.warning(f"登入狀態不明:[{smsg}]")
            case COM_STATUS.CONNECT_READY:  # 連線成功
                logger.info(f"QuoteCom: {smsg}, IP={self.conn.MyIP}")
            case COM_STATUS.CONNECT_FAIL:
                logger.error(f"連線失敗: {smsg} {sender.ServerHost}:{sender.ServerPort}")
            case COM_STATUS.DISCONNECTED:
                logger.info(f"斷線: {smsg}")
            case COM_STATUS.AS400_CONNECTED:
                logger.info(f"AS400 連線成功: {smsg}")
            case COM_STATUS.AS400_CONNECTFAIL:
                logger.info(f"AS400 連線失敗: {smsg}")
            case COM_STATUS.AS400_DISCONNECTED:
                logger.info(f"AS400 連線斷線: {smsg}")
            case COM_STATUS.SUBSCRIBE:
                logger.info(f"註冊:[{smsg}]")
            case COM_STATUS.UNSUBSCRIBE:
                logger.info(f"取消註冊:[{smsg}]")
            case COM_STATUS.ACK_REQUESTID:  # 下單或改單第一次回覆
                request_id = int.from_bytes(msg[0:8], byteorder='big')
                ack_status = msg[8]
                logger.info(f"序號回覆: {request_id} 狀態={'收單' if ack_status == 1 else '失敗'}.")
            case COM_STATUS.RECOVER_DATA:
                if (msg[0] == 0):
                    self.RecoverMap[smsg] = 0
                    logger.info(f"開始回補 Topic:[{smsg}]")
                elif (msg[0] == 1):
                    logger.info(f"結束回補 Topic:[{smsg} 筆數:{self.RecoverMap[smsg]}]")
            case _:
                logger.warning(f"STATUS:UNKNOWN={status}, msg=[{smsg}]")

    def onRecoverStatus(self, sender, topic, status, recover_count):
        logger.debug(f"{sender} {topic} {status} {recover_count}.")

        match status:
            case RECOVER_STATUS.RS_DONE:  # 回補資料結束
                logger.info(f"結束回補 Topic:[{topic} 筆數:{recover_count}]")
            case RECOVER_STATUS.RS_BEGIN:  # 開始回補資料
                logger.info(f"開始回補 Topic:[{topic}]")
            case RECOVER_STATUS.RS_NOAUTHRITY:
                logger.info(f"無回補權限 Topic:[{topic}]")

    def __exit__(self):
        # self.conn.Logout()
        logger.info('[Logout] Success.')
