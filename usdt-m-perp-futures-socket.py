import os
import json
import websocket
import gzip
import io
import time
import requests
import hmac
from hashlib import sha256

# CONSTANTS
from dotenv import load_dotenv

load_dotenv()
URL = "wss://open-api-swap.bingx.com/swap-market"
CHANNEL = "https://open-api.bingx.com/openApi/user/auth/userDataStream"

APIURL = os.getenv("API_URL")
APIKEY = os.getenv("API_KEY")
SECRETKEY = os.getenv("SECRET_KEY")

# Get listenKey
headers = {
    "X-BX-APIKEY": APIKEY,
}
response = requests.request("POST", CHANNEL, headers=headers, data={})
print(response.text)
data = json.loads(response.text)
# Extract the "listenKey" value
listen_key = data["listenKey"]
print(listen_key)
URL = URL + "?listenKey=" + listen_key

#
class Test:

    def __init__(self, url, channel):
        self.url = url
        self.ws = None
        self.channel = channel

    def on_open(self, ws):
        print("WebSocket connected")
        subStr = json.dumps(self.channel)
        ws.send(subStr)
        print("Subscribed to :", subStr)

    def on_data(self, ws, string, type, continue_flag):
        compressed_data = gzip.GzipFile(fileobj=io.BytesIO(string), mode="rb")
        decompressed_data = compressed_data.read()
        utf8_data = decompressed_data.decode("utf-8")
        print(utf8_data)

    def on_message(self, ws, message):
        compressed_data = gzip.GzipFile(fileobj=io.BytesIO(message), mode="rb")
        decompressed_data = compressed_data.read()
        utf8_data = decompressed_data.decode("utf-8")
        print(utf8_data)  # this is the message you need
        if (
            utf8_data == "Ping"
        ):  # this is very important , if you receive 'Ping' you need to send 'Pong'
            ws.send("Pong")

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("The connection is closed!")

    def start(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            # on_data=self.on_data,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.ws.run_forever()


if __name__ == "__main__":
    # Subscribe Market Depth Data
    # test = Test(URL, CHANNEL)
    CHANNEL = {
        "id": "e745cd6d-d0f6-4a70-8d5a-043e4c741b40",
        "reqType": "sub",
        "dataType": "",
    }
    # Subscribe the Latest Trade Detail
    # CHANNEL["dataType"] = "BTC-USDT@trade"
    # Subscribe K-Line Data
    # CHANNEL["dataType"] = "BTC-USDT@kline_1m"})
    # Subscribe to 24-hour price changes
    # CHANNEL["dataType"] = "BTC-USDT@ticker"})
    # Subscribe to latest price changes
    # CHANNEL["dataType"] = "BTC-USDT@lastPrice"})
    # Subscribe to latest mark price changes
    # CHANNEL["dataType"] = "BTC-USDT@markPrice"
    # Subscribe to the Book Ticker Streams
    # CHANNEL["dataType"] = "BTC-USDT@bookTicker"


    test = Test(URL, CHANNEL)
    test.start()
