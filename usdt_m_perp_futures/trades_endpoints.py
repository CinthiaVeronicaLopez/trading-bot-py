# IMPORTS
import os
import requests
import hmac
import json
import uuid
from hashlib import sha256
import ntplib
import numpy as np
import time
import seaborn as sns # Libreria graficas

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
    "batchOrders": "/openApi/swap/v2/trade/batchOrders",
    "cancel": "/openApi/swap/v2/trade/order",
    "cancelMultipleOrders": "/openApi/swap/v2/trade/batchOrders",
    "cancelAllOpenOrders": "/openApi/swap/v2/trade/allOpenOrders",
    "close-all": "/openApi/swap/v2/trade/closeAllPositions",
    "current": "/openApi/swap/v2/trade/openOrders",
    "pending": "/openApi/swap/v2/trade/openOrder",
    "order": "/openApi/swap/v2/trade/order",
    "marginType": "/openApi/swap/v2/trade/marginType",
    "changeMarginType": "/openApi/swap/v2/trade/marginType",
    "leverage": "/openApi/swap/v2/trade/leverage",
    "setLeverage": "/openApi/swap/v2/trade/leverage",
    "forceOrders": "/openApi/swap/v2/trade/forceOrders",
    "allOrders": "/openApi/swap/v2/trade/allOrders",
    "positionMargin": "/openApi/swap/v2/trade/positionMargin",
    "allFillOrders": "/openApi/swap/v2/trade/allFillOrders",
    "setDual": "/openApi/swap/v1/positionSide/dual",
    "dual": "/openApi/swap/v1/positionSide/dual",
    "cancelReplace": "/openApi/swap/v1/trade/cancelReplace",
    "batchCancelReplace": "/openApi/swap/v1/trade/batchCancelReplace",
    "cancelAllAfter": "/openApi/swap/v2/trade/cancelAllAfter",
    "closePosition": "/openApi/swap/v1/trade/closePosition",
    "fullOrder": "/openApi/swap/v1/trade/fullOrder",
    "maintMarginRatio": "/openApi/swap/v1/maintMarginRatio",
    "fillHistory": "/openApi/swap/v1/trade/fillHistory",
    "positionHistory": "/openApi/swap/v1/trade/positionHistory",
}


def get_ntp_time():
    ntp = 0
    while not ntp > 0:
        try:
            ntp_client = ntplib.NTPClient()
            response = ntp_client.request("pool.ntp.org")  # Utiliza el servidor NTP
            # El timestamp es en segundos, lo multiplicamos por 1000 para obtenerlo en milisegundos
            ntp = int(response.tx_time * 1000)
        except Exception as e:
            print(f"Error al obtener el timestamp de NTP: {e}")
            # Si hay un error, usamos el tiempo local como fallback            
            ntp = 0
            print("Esperando conexión...")
            time.sleep(10)        
            continue  
    return ntp


def getTimestamp(minutes=0):
    minutes = minutes * 60
    current = time.time()
    return int(current + minutes)

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
            return paramsStr + "&timestamp=" + str(get_ntp_time())#int(time.time() * 1000))
        else:
            return paramsStr + "timestamp=" + str(get_ntp_time())#int(time.time() * 1000))

    def send_request(self):
        headers = {
            "X-BX-APIKEY": self.api_key,
        }
        data = [{}]
        code = 1
        # while code != 0:
        try:
            params_str = self.parseParam()
            url = "%s%s?%s&signature=%s" % (
                self.api_url,
                self.path,
                params_str,
                self.get_sign(params_str),
            )
            response = requests.request(
                self.method, url, headers=headers, data=self.payload
            )
            response_json = response.json()
                # Verificar si la respuesta contiene el campo 'code'
            if "code" in response_json:
                code = response_json["code"]
            else:
                raise ValueError(f"Campo 'code' no encontrado en la respuesta: {response.text}")

            # Verificar si la respuesta contiene el campo 'data'
            if "data" in response_json:
                data = response_json["data"]
            else:
                raise ValueError(f"Campo 'data' no encontrado en la respuesta: {response.text}")

            if code != 0:
                raise ValueError(f"Error en la respuesta de la API: {response.text}")

        except ValueError as e:
            data = False
            print("Error de conexión o en la respuesta de la API:")
            print(self.path)
            print(e)
            time.sleep(10)
            # continue
        except Exception as e:
            data = False
            print("Otro tipo de error:")
            print(e)
            time.sleep(10)
            # continue
        return data

    # TIPO DE PENDIENTE
    def get_trend(self, slope, diff):
        trend = "LATERAL"
        if slope > 1 * diff:
            trend = "LONG"
        elif slope < -1 * diff:
            trend = "SHORT"
        return trend

    # CALCULA MA
    def _ma_(
        self,
        limits=[200, 5, 10, 20],
        interval="1m",
        type="close",
        slope_max=7,
        symbol=SYMBOL,
    ):

        def calc_trend(klines, limit=48, type="close"):
            # Obtener los últimos valores
            last_klines = klines[-1*limit:]
            # Extraer los precios de cierre (close) y los timestamps
            close_prices = np.array([float(item['close']) for item in last_klines])
            timestamps = np.array([item['time'] for item in last_klines])
            # Convertir los timestamps a segundos desde el primer valor
            time_seconds = (timestamps - timestamps.min()) / 1000  # Convertir milisegundos a segundos
            # Cálculo manual de la pendiente
            # Aplicamos la fórmula de la regresión lineal: y = mx + b
            A = np.vstack([time_seconds, np.ones(len(time_seconds))]).T
            slope, intercept = np.linalg.lstsq(A, close_prices, rcond=None)[0]            
            return slope

        def calc_ma(klines, limit, type="close"):
            sum = 0
            for i in range(limit - 1, -1, -1):
                sum = sum + float(klines[i][type])
            return float(sum / limit)

        limit_max = limits[0]
        ma = {}

        klines = self.kline_candlestick_data(limit_max, interval, symbol)        
        if klines:
            if len(klines) == limit_max:
                for i in range(len(limits)):
                    ma["ma" + str(i)] = calc_ma(klines, limits[i], type)
                ma["slope"] = calc_trend(klines, slope_max, type)  # limit_max)

        return ma

    # MARKET DATA
    def symbols(self, symbol=SYMBOL):
        self.path = PATH["contracts"]
        self.method = "GET"
        self.params_map = {"symbol": symbol}
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
        self.params_map = {
            "recvWindow": "0",
            "symbol": symbol,
            # "timestamp": str(get_ntp_time()),
        }
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
        self,
        start_price,
        stop_price,
        type="TAKE_PROFIT_MARKET",
        working_type="MARK_PRICE",
    ):
        data = {
            "type": type,
            "stopPrice": stop_price,
            "price": start_price,
            "workingType": working_type,
        }
        print("data", data)
        return json.dumps(data)

    def gen_params_map(
        self,
        side,
        quantity,
        price=False,
        take_profit=False,
        type="MARKET",
        positionSide="LONG",
        symbol=SYMBOL,
        cancelReplaceMode=False,
        cancelClientOrderId=False,
        cancelOrderId=False,
        cancelRestrictions=False,
    ):
        params_map = {
            "symbol": symbol,
            "side": side,
            "positionSide": positionSide,
            "type": type,
            "quantity": quantity,
            "clientOrderID": str(uuid.uuid4()),
            "timestamp": str(get_ntp_time()),
        }
        if not bool(take_profit) and bool(price):
            params_map["price"] = str(price)
        if take_profit:
            params_map["takeProfit"] = take_profit
        if cancelReplaceMode:
            params_map["cancelReplaceMode"] = cancelReplaceMode
        if cancelClientOrderId:
            params_map["cancelClientOrderId"] = cancelClientOrderId
        if cancelOrderId:
            params_map["cancelOrderId"] = cancelOrderId
        if cancelRestrictions:
            params_map["cancelRestrictions"] = cancelRestrictions
        self.params_map = params_map
        return params_map

    def place_order(
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
        self.params_map = self.gen_params_map(
            side, quantity, price, take_profit, type, positionSide, symbol
        )
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
        if not price:
            print("test price")
            symbol_price = self.symbol_price_ticker()
            start_price = float(symbol_price["price"])  # * 1.001
            stop_price = float(start_price) * 1.01
            take_profit = self.serialize_to_json(start_price, stop_price)
        return self.place_order(
            side, quantity, price, take_profit, type, positionSide, symbol, "test"
        )

    def place_multiple_orders(
        self,
        batchOrders=[],
        path="batchOrders",
    ):
        self.path = PATH[path]
        self.method = "POST"
        if len(batchOrders) > 0:
            self.params_map = {"batchOrders": json.dumps(batchOrders)}
            return self.send_request()

    def close_all_positions(self, symbol=SYMBOL):
        self.path = PATH["close-all"]
        self.method = "POST"
        self.params_map = {
            "symbol": symbol,
        }
        return self.send_request()

    def cancel_order(self, order_id, symbol=SYMBOL):
        # TODO: this doesn't work, see https://bingx-api.github.io/docs/#/en-us/swapV2/trade-api.html#Cancel%20Order
        self.path = PATH["cancel"]
        self.method = "DELETE"
        self.params_map = {"orderId": order_id, "symbol": symbol}
        return self.send_request()

    def cancel_multiple_orders(self, clientOrderIdList, symbol=SYMBOL):
        # TODO: this doesn't work, see https://bingx-api.github.io/docs/#/en-us/swapV2/trade-api.html#Cancel%20multiple%20orders
        self.path = PATH["cancelMultipleOrders"]
        self.method = "DELETE"
        print("clientOrderIdList", clientOrderIdList)
        self.params_map = {"clientOrderIDList": clientOrderIdList, "symbol": symbol}
        return self.send_request()

    def cancel_all_open_orders(self, symbol=SYMBOL):
        # TODO: this doesn't work, see https://bingx-api.github.io/docs/#/en-us/swapV2/trade-api.html#Cancel%20All%20Open%20Orders
        self.path = PATH["cancelAllOpenOrders"]
        self.method = "DELETE"
        self.params_map = {"symbol": symbol}
        return self.send_request()

    def current_all_open_orders(self, symbol=SYMBOL):
        # TODO: this doesn't work, see https://bingx-api.github.io/docs/#/en-us/swapV2/trade-api.html#Current%20All%20Open%20Orders
        self.path = PATH["current"]
        self.method = "GET"
        self.params_map = {"symbol": symbol}
        return self.send_request()

    def query_pending_order_status(self, order_id, symbol=SYMBOL):
        self.path = PATH["pending"]
        self.method = "GET"
        self.params_map = {"orderId": order_id, "symbol": symbol}
        return self.send_request()

    def query_order_details(self, order_id, symbol=SYMBOL):
        self.path = PATH["order"]
        self.method = "GET"
        self.params_map = {"orderId": order_id, "symbol": symbol}
        return self.send_request()

    def query_margin_type(self, symbol=SYMBOL):
        self.path = PATH["marginType"]
        self.method = "GET"
        self.params_map = {"symbol": symbol}
        return self.send_request()

    def change_margin_type(self, margin_type="CROSSED", symbol=SYMBOL):
        self.path = PATH["changeMarginType"]
        self.method = "POST"
        self.params_map = {"marginType": margin_type, "symbol": symbol}
        return self.send_request()

    def query_leverage(self, symbol=SYMBOL):
        self.path = PATH["leverage"]
        self.method = "GET"
        self.params_map = {"symbol": symbol}
        return self.send_request()

    def set_leverage(self, leverage="5", side="SHORT", symbol=SYMBOL):
        self.path = PATH["setLeverage"]
        self.method = "POST"
        self.params_map = {"leverage": leverage, "side": side, "symbol": symbol}
        return self.send_request()

    def users_force_orders(self, symbol=SYMBOL):
        self.path = PATH["forceOrders"]
        self.method = "GET"
        self.params_map = {"symbol": symbol}
        return self.send_request()

    def query_order_history(
        self,
        endTime=getTimestamp(24 * 60),
        limit="500",
        startTime=getTimestamp(),
        symbol=SYMBOL,
    ):
        self.path = PATH["allOrders"]
        self.method = "GET"
        self.params_map = {
            "endTime": endTime,
            "limit": limit,
            "startTime": startTime,
            "symbol": symbol,
        }
        return self.send_request()

    def modify_isolated_position_margin(
        self, amount=3, type=1, positionSide="LONG", symbol=SYMBOL
    ):
        self.path = PATH["positionMargin"]
        self.method = "POST"
        self.params_map = {
            "symbol": symbol,
            "type": str(type),
            "amount": str(amount),
            "positionSide": positionSide,
        }
        return self.send_request()

    def query_historical_transaction_orders(
        self,
        endTs=getTimestamp(24 * 60),
        startTs=getTimestamp(),
        tradingUnit="COIN",
        symbol=SYMBOL,
    ):
        self.path = PATH["allFillOrders"]
        self.method = "GET"
        self.params_map = {
            "endTs": endTs,
            "startTs": startTs,
            "symbol": symbol,
            "tradingUnit": tradingUnit,
        }
        return self.send_request()

    def set_position_mode(self, dualSidePosition=True):
        self.path = PATH["setDual"]
        self.method = "POST"
        self.params_map = {"dualSidePosition": str(dualSidePosition).lower()}
        return self.send_request()

    def query_position_mode(self):
        self.path = PATH["dual"]
        self.method = "GET"
        self.params_map = {}
        return self.send_request()

    def cancel_existing_order_send_new_order(self, batchOrders=[]):
        self.path = PATH["cancelReplace"]
        self.method = "POST"
        if len(batchOrders) > 0:
            self.params_map = {"batchOrders": json.dumps(batchOrders)}
            return self.send_request()

    def cancel_orders_place_orders_in_batches(self, batchOrders=[]):
        return self.place_multiple_orders(batchOrders, "batchCancelReplace")

    def cancel_all_after(self, type="ACTIVATE", timeOut=10):
        self.path = PATH["cancelAllAfter"]
        self.method = "POST"
        self.params_map = {"type": type, "timeOut": timeOut}
        return self.send_request()

    def close_position_by_position_id(self, position_id):
        self.path = PATH["closePosition"]
        self.method = "POST"
        self.params_map = {"positionId": position_id}
        return self.send_request()

    def all_orders(
        self,
        endTime=getTimestamp(24 * 60),
        limit="500",
        startTime=getTimestamp(),
        symbol=SYMBOL,
    ):
        self.path = PATH["fullOrder"]
        self.method = "GET"
        self.params_map = {
            "endTime": endTime,
            "limit": limit,
            "startTime": startTime,
            "symbol": symbol,
        }
        return self.send_request()

    def position_maintenance_margin_ratio(self, symbol=SYMBOL):
        self.path = PATH["maintMarginRatio"]
        self.method = "GET"
        self.params_map = {"symbol": symbol}
        return self.send_request()

    def query_historical_transaction_details(
        self,
        endTs=getTimestamp(24 * 60),
        startTs=getTimestamp(),
        lastFillId=130753,
        pageSize=50,
        symbol=SYMBOL,
    ):
        self.path = PATH["fillHistory"]
        self.method = "GET"
        self.params_map = {
            "endTs": endTs,
            "startTs": startTs,
            "symbol": symbol,
            "lastFillId": lastFillId,
            "pageSize": pageSize,
        }
        return self.send_request()

    def query_position_history(
        self,
        pageId=0,
        startTime=getTimestamp(),
        pageSize=20,
        symbol=SYMBOL,
    ):
        self.path = PATH["positionHistory"]
        self.method = "GET"
        self.params_map = {
            "symbol": symbol,
            "pageId": pageId,
            "pageSize": pageSize,
            "startTime": startTime,
        }
        return self.send_request()

    def long(self, price, quantity, type="LIMIT", symbol=SYMBOL):
        return self.place_order("BUY", quantity, price, False, type, "LONG", symbol)
