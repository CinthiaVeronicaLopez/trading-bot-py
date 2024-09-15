# IMPORTS
import os
import time
import requests
import hmac
import json
import uuid
from hashlib import sha256

# CONSTANTS
from dotenv import load_dotenv

load_dotenv()

SYMBOL = "BTC-USDT"
API_URL = os.getenv("API_URL")  # "https://open-api.bingx.com"
API_URL_DEMO = os.getenv("API_URL_DEMO")  # "https://open-api-vst.bingx.com"
APIURL = API_URL_DEMO
APIKEY = os.getenv("API_KEY")
SECRETKEY = os.getenv("SECRET_KEY")
PATH = {
    # MARKET DATA
    "contracts": "/openApi/swap/v2/quote/contracts",
    "depth": "/openApi/swap/v2/quote/depth",
    "trades": "/openApi/swap/v2/quote/trades",
    "premiumIndex": "/openApi/swap/v2/quote/premiumIndex",
    "fundingRate": "/openApi/swap/v2/quote/fundingRate",
    "klines": "/openApi/swap/v3/quote/klines",
    "openInterest": "/openApi/swap/v2/quote/openInterest",
    "ticker": "/openApi/swap/v2/quote/ticker",
    "historicalTrades": "/openApi/swap/v1/market/historicalTrades",
    "bookTicker": "/openApi/swap/v2/quote/bookTicker",
    "markPriceKlines": "/openApi/swap/v1/market/markPriceKlines",
    "price": "/openApi/swap/v1/ticker/price",
    # ACCOUNT ENPOINTS
    "balance": "/openApi/swap/v3/user/balance",
    "positions": "/openApi/swap/v2/user/positions",
    "income": "/openApi/swap/v2/user/income",
    "export": "/openApi/swap/v2/user/income/export",
    "commissionRate": "/openApi/swap/v2/user/commissionRate",
    # TRADES ENDPOINTS
    "test": "/openApi/swap/v2/trade/order/test",
    "place": "/openApi/swap/v2/trade/order",
    "close": "/openApi/swap/v1/trade/closePosition",
    "close-all": "/openApi/swap/v2/trade/closeAllPositions",
    "cancel": "/openApi/swap/v2/trade/order",
    "current": "/openApi/swap/v2/trade/openOrders",
    "pending": "/openApi/swap/v2/trade/openOrder",
}


class TradesEndpoints:
    """Manage API REST Trades Endpoints"""

    def __init__(
        self, path="price", params_map={"symbol": SYMBOL}, method="GET", payload={}
    ):
        self.secret_key = SECRETKEY
        self.api_key = APIKEY
        self.api_url = APIURL
        self.method = method
        self.path = PATH[path] if path else ""
        self.params_map = params_map
        self.payload = payload

    def get_sign(self, params_str):
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            params_str.encode("utf-8"),
            digestmod=sha256,
        ).hexdigest()
        # print("sign=" + signature)
        return signature

    def parseParam(self):
        params_map = self.params_map
        sorted_keys = sorted(params_map)
        paramsStr = "&".join(["%s=%s" % (x, params_map[x]) for x in sorted_keys])
        if paramsStr != "":
            return paramsStr + "&timestamp=" + str(int(time.time() * 1000))
        else:
            return paramsStr + "timestamp=" + str(int(time.time() * 1000))

    def send_request(self):
        params_str = self.parseParam()
        url = "%s%s?%s&signature=%s" % (
            self.api_url,
            self.path,
            params_str,
            self.get_sign(params_str),
        )
        # print(url)
        headers = {
            "X-BX-APIKEY": self.api_key,
        }
        response = requests.request(
            self.method, url, headers=headers, data=self.payload
        )
        print(response.text)
        return response.json()

    # MARKET DATA
    def symbols(self):
        self.path = PATH["contracts"]
        self.method = "GET"
        self.params_map = {}
        return self.send_request()

    def order_book(self, limit=5, symbol=SYMBOL):
        self.path = PATH["depth"]
        self.method = "GET"
        self.params_map = {"symbol": symbol, "limit": str(limit)}
        return self.send_request()

    def recent_trades_list(self, limit=5, symbol=SYMBOL):
        self.path = PATH["trades"]
        self.method = "GET"
        self.params_map = {"symbol": symbol, "limit": str(limit)}
        return self.send_request()

    def mark_price_funding_rate(self, symbol=SYMBOL):
        self.path = PATH["premiumIndex"]
        self.method = "GET"
        self.params_map = {"symbol": symbol}
        return self.send_request()

    def get_funding_rate_history(self, limit=2, symbol=SYMBOL):
        self.path = PATH["fundingRate"]
        self.method = "GET"
        self.params_map = {"symbol": symbol, "limit": str(limit)}
        return self.send_request()

    def kline_candlestick_data(self, limit=1000, interval="1h", symbol=SYMBOL):
        self.path = PATH["klines"]
        self.method = "GET"
        self.params_map = {
            "symbol": symbol,
            "interval": interval,
            "limit": str(limit),
            # "startTime": "1702717199998"
        }
        return self.send_request()

    def open_interest_statistics(self, symbol=SYMBOL):
        self.path = PATH["openInterest"]
        self.method = "GET"
        self.params_map = {"symbol": symbol}
        return self.send_request()

    def ticker_price_change_statistics(self, symbol=SYMBOL):
        self.path = PATH["ticker"]
        self.method = "GET"
        self.params_map = {"symbol": symbol}
        return self.send_request()

    def query_historical_transaction_orders(self, limit=1000, symbol=SYMBOL):
        self.path = PATH["historicalTrades"]
        self.method = "GET"
        self.params_map = {
            # "fromId": "412551",
            "limit": str(limit),
            "symbol": symbol,
            # "timestamp": "1702731995838",
            # "recvWindow": "60000"
        }
        return self.send_request()

    def symbol_order_book_ticker(self, symbol=SYMBOL):
        self.path = PATH["bookTicker"]
        self.method = "GET"
        self.params_map = {"symbol": symbol}
        return self.send_request()

    def mark_price_kline_candlestick_data(
        self, limit=1000, interval="1h", symbol=SYMBOL
    ):
        self.path = PATH["markPriceKlines"]
        self.method = "GET"
        self.params_map = {
            "symbol": symbol,
            "interval": interval,
            "limit": str(limit),
            # "startTime": "1702717199998"
        }
        return self.send_request()

    def symbol_price_ticker(self, symbol=SYMBOL):
        self.path = PATH["price"]
        self.method = "GET"
        self.params_map = {"symbol": symbol}
        return self.send_request()

    # ACCOUNT ENPOINTS
    def query_account_data(self):
        self.path = PATH["balance"]
        self.method = "GET"
        self.params_map = {}
        return self.send_request()

    def query_position_data(self, symbol=SYMBOL):
        self.path = PATH["positions"]
        self.method = "GET"
        self.params_map = {"symbol": symbol}
        return self.send_request()

    def get_account_profit_loss_fund_flow(self, limit=1000):
        self.path = PATH["income"]
        self.method = "GET"
        self.params_map = {
            # "startTime": "1702713615001",
            # "endTime": "1702731787011",
            "limit": str(limit),
            # "timestamp": "1702731787011"
        }
        return self.send_request()

    def export_fund_flow(self, limit=200, symbol=SYMBOL):
        self.path = PATH["export"]
        self.method = "GET"
        self.params_map = {
            # "endTime": "",
            "limit": str(limit),
            # "recvWindow": "10000",
            # "startTime": "",
            "symbol": symbol,
            # "timestamp": "1702449874964"
        }
        return self.send_request()

    def query_trading_commission_rate(self):
        self.path = PATH["commissionRate"]
        self.method = "GET"
        self.params_map = {
            # "timestamp": "1702732072912",
            # "recvWindow": "5000"
        }
        return self.send_request()

    # TRADES ENDPOINTS
    def serialize_to_json(
        self, start_price, stop_price, type="TAKE_PROFIT_MARKET", working_type="MARK_PRICE"
    ):
        data = {
            "type": type,
            "stopPrice": stop_price,
            "price": price,
            "workingType": working_type,
        }
        print("data", data)
        return json.dumps(data)

    def place(
        self,
        side,
        quantity,
        price=False,
        take_profit=False,
        type="MARKET",
        positionSide="LONG",
        symbol=SYMBOL,
        path="place",
    ):
        self.path = PATH[path]
        self.method = "POST"
        self.params_map = {
            "symbol": symbol,
            "side": side,
            "positionSide": positionSide,
            "type": type,
            "quantity": str(quantity),
            "clientOrderID": str(uuid.uuid4()),
        }
        if not bool(take_profit) and bool(price):
            self.params_map["price"] = str(price)
        if take_profit:
            self.params_map["takeProfit"] = take_profit
        return self.send_request()

    def test_order(
        self,
        side="BUY",
        quantity=5,
        price=False,
        take_profit=False,
        type="MARKET",
        positionSide="LONG",
        symbol=SYMBOL,
    ):
        response = self.symbol_price_ticker()
        data = response["data"]
        start_price = float(data["price"]) #* 1.001
        stop_price = float(start_price) * 1.01
        take_profit = self.serialize_to_json(start_price, stop_price)
        return self.place(
            side,
            quantity,
            price,
            take_profit,
            type,
            positionSide,
            symbol,
            "test"
        )

    def pending(self, order_id, symbol=SYMBOL):
        self.path = PATH["pending"]
        self.method = "GET"
        self.params_map = {"orderId": order_id, "symbol": symbol}
        return self.send_request()

    def current(self, symbol=SYMBOL):
        self.path = PATH["current"]
        self.method = "GET"
        self.params_map = {"symbol": symbol}
        return self.send_request()

    def close_all(self, symbol=SYMBOL):
        self.path = PATH["close-all"]
        self.method = "POST"
        self.params_map = {
            "symbol": symbol,
        }
        return self.send_request()

    def close(self, position_id):
        self.path = PATH["close"]
        self.method = "POST"
        self.params_map = {"positionId": position_id}
        return self.send_request()

    def cancel_order(self, order_id, symbol=SYMBOL):
        # TODO: this doesn't work
        self.path = PATH["cancel"]
        self.method = "DELETE"
        self.params_map = {"orderId": order_id, "symbol": symbol}
        return self.send_request()

    def long(self, price, quantity, type="LIMIT", symbol=SYMBOL):
        return self.place("BUY", quantity, price, False, type, "LONG", symbol)