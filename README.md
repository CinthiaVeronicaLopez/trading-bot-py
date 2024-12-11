# trading-bot-py - Python Trading Bot

## Socket API Reference

### Introduction

#### Access
the base URL of Websocket Market Data ：wss://open-api-swap.bingx.com/swap-market

#### Data Compression
All response data from Websocket server are compressed into GZIP format. Clients have to decompress them for further use.

#### Heartbeats
Once the Websocket Client and Websocket Server get connected, the server will send a heartbeat- Ping message every 5 seconds (the frequency might change).
When the Websocket Client receives this heartbeat message, it should return Pong message.

#### Subscriptions
After successfully establishing a connection with the Websocket server, the Websocket client sends the following request to subscribe to a specific topic:
```json
{ "id": "id1", "reqType": "sub", "dataType": "data to sub" }
```

After a successful subscription, the Websocket client will receive a confirmation message:
```json
{ "id": "id1", "code": 0, "msg": "" }
```

After that, once the subscribed data is updated, the Websocket client will receive the update message pushed by the server.

#### Unsubscribe
The format of unsubscription is as follows:
```json
{ "id": "id1", "reqType": "unsub", "dataType": "data to unsub"}
```

Confirmation of Unsubscription:
```json
{ "id": "id1", "code": 0, "msg": "" }
```


### Listen Key
websocket interface

> wss://open-api-swap.bingx.com/swap-market

account subscription data stream /swap-market?listenKey=

> wss://open-api-swap.bingx.com/swap-market?listenKey=a8ea75681542e66f1a50a1616dd06ed77dab61baa0c296bca03a9b13ee5f2dd7

#### generate Listen Key
listen key Valid for 1 hour
##### interface
CURL
> POST https://open-api.bingx.com/openApi/user/auth/userDataStream
Content-Type: request body (application/json)
response
> {"listenKey":"a8ea75681542e66f1a50a1616dd06ed77dab61baa0c296bca03a9b13ee5f2dd7"}

rate limitation by UID: 5/s & rate limitation by IP in group Number: 2
API KEY permission: 
No API KEY signature required
 
Header
```json
{
  "X-BX-APIKEY": "string" # API KEY
}
```
Response
```json
{
  "listenKey": "string" # listen Key
}
Code 
```python
CHANNEL = "https://open-api.bingx.com/openApi/user/auth/userDataStream"
headers = {
    "X-BX-APIKEY": APIKEY,
}
response = requests.request("POST", CHANNEL, headers=headers, data={})
print(response.text)
```

### Extend Listen Key Validity period
The validity period is extended to 60 minutes after this call, and it is recommended to send a ping every 30 minutes.
#### HTTP Request https://open-api.bingx.com

#### CURL
#### response
- http status 200 success
- http status 204 not content
- http status 404 not find key

1. Create API KEY  
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes  
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
> PUT https://open-api.bingx.com/openApi/user/auth/userDataStream

rate limitation by UID: 5/s & rate limitation by IP in group Number: 
API KEY permission: 
No API KEY signature required
Content-Type: request body (application/json)


### delete Listen Key
delete User data flow.
#### response
- http status 200 success
- http status 204 not content
- http status 404 not find key

#### request parameters
> DELETE https://open-api.bingx.com/openApi/user/auth/userDataStream

Request
```json
{
  "listenKey": "string" # listen Key
}
```
Code 
```python
listen_key = "your_listen_key"
CHANNEL = "https://open-api.bingx.com/openApi/user/auth/userDataStream"
headers = {
    "listenKey": listen_key,
}
response = requests.request("DELETE", CHANNEL, headers=headers, data={})
print(response.text)
```


## Websocket Market Data

### Subscribe Market Depth Data
Push limited order book depth information with a customizable push interval.

#### Subscription Type
The dataType is <symbol>@depth<level>@<interval>, for example, BTC-USDT@depth5@100ms, BTC-USDT@depth20@200ms, BTC-USDT@depth100@500ms.

If <interval> is not provided, the default is 500ms.

#### Subscription Parameters
Request
```json
{
  "symbol": "string", # There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
  "level": "string", # Depth level, such as 5，10，20，50，100
  "interval": "string" # Interval, e.g., 100ms, 200ms, 500ms, 1000ms
}
```
Response
```json
{
  "code": "", # With regards to error messages, 0 means normal, and 1 means error
  "dataType": "", # The type of subscribed data, such as BTC-USDT@depth5@500ms
  "data": "", # Push Data
  "asks": "", # Sell side depth
  "bids": "", # Buy side depth
  "p": "", # price
  "v": "" # volume
}
{"code":0,"dataType":"BTC-USDT@depth5@500ms","ts":1725236020190,"data":{"bids":[["57388.7","4.4249"],["57388.6","0.0323"],["57385.2","2.4081"],["57382.8","2.5252"],["57381.0","2.8511"]],"asks":[["57397.3","1.4781"],["57395.3","2.7615"],["57392.2","3.2240"],["57388.9","0.2759"],["57388.8","0.2177"]]}}
```
level
```json
{
  "level5": "",
  "level10": "",
  "level20": "",
  "level50": "",
  "level100": ""
}
```
interval
```json
{
  "100ms": "",
  "200ms": "",
  "500ms": "",
  "1000ms": ""
}
```
Code
```python
import json
import websocket
import gzip
import io
URL="wss://open-api-swap.bingx.com/swap-market" 
CHANNEL= {"id":"e745cd6d-d0f6-4a70-8d5a-043e4c741b40","reqType": "sub","dataType":"BTC-USDT@depth5@500ms"}
class Test(object):

    def __init__(self):
        self.url = URL 
        self.ws = None

    def on_open(self, ws):
        print('WebSocket connected')
        subStr = json.dumps(CHANNEL)
        ws.send(subStr)
        print("Subscribed to :",subStr)

    def on_data(self, ws, string, type, continue_flag):
        compressed_data = gzip.GzipFile(fileobj=io.BytesIO(string), mode='rb')
        decompressed_data = compressed_data.read()
        utf8_data = decompressed_data.decode('utf-8')
        print(utf8_data)

    def on_message(self, ws, message):
        compressed_data = gzip.GzipFile(fileobj=io.BytesIO(message), mode='rb')
        decompressed_data = compressed_data.read()
        utf8_data = decompressed_data.decode('utf-8')
        print(utf8_data)  #this is the message you need 
        if utf8_data == "Ping": # this is very important , if you receive 'Ping' you need to send 'Pong' 
           ws.send("Pong")

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print('The connection is closed!')

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
    test = Test()
    test.start()
```


### Subscribe the Latest Trade Detail
Subscribe to the trade detail data of a trading pair
#### Subscription Type
The dataType is <symbol>@trade E.g. BTC-USDT@trade ETH-USDT@trade

#### Subscription Parameters
Request
```json
{
  "symbol": "string" # There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
}
```
Response
```json
{
  "code": "", # With regards to error messages, 0 means normal, and 1 means error
  "dataType": "", # The type of subscribed data, such as market.depth.BTC-USDT.step0.level5
  "data": "" # Push Data
  "T": "", # transaction time
  "s": "", # trading pair
  "m": "", # Whether the buyer is a market maker. If true, this transaction is an active sell order, otherwise it is an active buy order.
  "p": "", # price
  "v": "" # volume
}
{"code":0,"dataType":"BTC-USDT@trade","data":[{"q":"0.1006","p":"58035.5","T":1725205512424,"m":false,"s":"BTC-USDT"},{"q":"0.0003","p":"58035.4","T":1725205512424,"m":true,"s":"BTC-USDT"}]}
```
Code
```python
CHANNEL= {"id":"e745cd6d-d0f6-4a70-8d5a-043e4c741b40","reqType": "sub","dataType":"BTC-USDT@trade"}
```


#### Subscribe K-Line Data
Subscribe to market k-line data of one trading pair

#### Subscription Type
The dataType is <symbol>@kline_<interval> E.g. BTC-USDT@kline_1m

#### Subscription example
```json
{
    "id":"e745cd6d-d0f6-4a70-8d5a-043e4c741b40",
    "reqType": "sub",
    "dataType":"BTC-USDT@kline_1m"
}
```
#### Subscription Parameters
 
Request
```json
{
  "symbol": "string", # There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
  "interval": "string" # The type of K-Line ( minutes, hours, weeks etc.)
}

```
Response
```json
{
  "code": "", # With regards to error messages, 0 means normal, and 1 means error
  "dataType": "", # The type of subscribed data, such as market.depth.BTC-USDT.step0.level5
  "data": "" # Push Data
  "c": "", # Closing Price
  "h": "", # High Price
  "l": "", # Low Price
  "o": "", # Opening Price
  "v": "", # volume
  "s": "" # trading pair
}
{"code":0,"dataType":"BTC-USDT@kline_1m","s":"BTC-USDT","data":[{"c":"58080.7","o":"58037.4","h":"58089.3","l":"58036.2","v":"47.8183","T":1725205560000}]}
```
interval
```json
{
  "1m": "", # 1 min Kline
  "3m": "", # 3 min Kline
  "5m": "", # 5 min Kline
  "15m": "", # 15 min Kline
  "30m": "", # 30 min Kline
  "1h": "", # 1-hour Kline
  "2h": "", # 2-hour Kline
  "4h": "", # 4-hour Kline
  "6h": "" # 6-hour Kline
}
```
Code
```python
CHANNEL= {"id":"e745cd6d-d0f6-4a70-8d5a-043e4c741b40","reqType": "sub","dataType":"BTC-USD@trade"}
```


#### Subscribe to 24-hour price changes
Push 24-hour price changes.

#### Subscription Type
dataType is <symbol>@ticker, such as BTC-USDT@ticker.

#### Subscription Parameters 
Request
```json
{
  "symbol": "string", # There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
}

```
Response
```json
{
  "code": "", # With regards to error messages, 0 means normal, and 1 means error
  "dataType": "", # The type of subscribed data, such as BTC-USDT@ticker
  "data": "" # Push Data
  "e": "", # Event type
  "E": "", # Event time
  "s": "", # trading pair, for example: BTC-USDT
  "p": "", # 24-hour price change
  "P": "", # Price change percentage
  "o": "", # First price in the last 24 hours
  "h": "", # Highest price in the last 24 hours
  "l": "", # Lowest price in the last 24 hours
  "L": "", # 24-hour turnover, the unit is USDT
  "c": "", # The time when the last transaction occurred within 24 hours
  "v": "", # 24-hour trading volume
  "q": "", # 24-hour trading amount, in USDT
  "O": "", # Time of the first transaction in the last 24 hours
  "C": "", # Time of the last transaction in the last 24 hours
  "B": "", # Bid price
  "b": "", # Bid quantity
  "A": "", # Ask price
  "a": "" # Ask quantity
}
{"code":0,"dataType":"BTC-USDT@ticker","data":{"e":"24hTicker","E":1725205664709,"s":"BTC-USDT","p":"-656.1","P":"-1.11","c":"58305.2","L":"0.0186","h":"59114.1","l":"57122.0","v":"40859.4190","q":"2390368926.39","o":"58961.3","O":1725205660601,"C":1725205664667,"A":"58304.4","a":"0.8298","B":"58304.3","b":"1.7605"}}
```
Code
```python
CHANNEL= {"id":"24dd0e35-56a4-4f7a-af8a-394c7060909c","reqType": "sub","dataType":"BTC-USDT@ticker"}
```


### Subscribe to latest price changes
Push latest price changes.

#### Subscription Type
dataType is <symbol>@lastPrice, such as BTC-USDT@lastPrice.

#### Subscription Parameters
Request
```json
{
  "symbol": "string", # There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
}
```
Response
```json
{
  "code": "", # With regards to error messages, 0 means normal, and 1 means error
  "dataType": "", # Subscribed data type, e.g., BTC-USDT@lastPrice
  "data": "", # Push content
  "e": "", # Event type
  "E": "", # Event time
  "s": "", # Trading pair, e.g., BTC-USDT
  "c": "" # Latest transaction price
}
{"code":0,"dataType":"BTC-USDT@lastPrice","data":{"e":"lastPriceUpdate","E":1725205707394,"s":"BTC-USDT","c":"58278.6"}}
```
Code
```python
CHANNEL= {"id":"24dd0e35-56a4-4f7a-af8a-394c7060909c","reqType": "sub","dataType":"BTC-USDT@lastPrice"}
```


### Subscribe to latest mark price changes
Push latest mark price changes.

#### Subscription Type
dataType is <symbol>@markPrice, such as BTC-USDT@markPrice.

#### Subscription Parameters
Request
```json
{
  "symbol": "string", # There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
}
```
Response
```json
{
  "code": "", # With regards to error messages, 0 means normal, and 1 means error
  "dataType": "", # Subscribed data type, e.g., BTC-USDT@markPrice
  "data": "", # Push content
  "e": "", # Event type
  "E": "", # Event time
  "s": "", # Trading pair, e.g., BTC-USDT
  "p": "" # Latest mark price
}
{"code":0,"dataType":"BTC-USDT@markPrice","data":{"e":"markPriceUpdate","E":1725205754727,"s":"BTC-USDT","p":"58221.6"}}
```
Code
```python
CHANNEL= {"id":"24dd0e35-56a4-4f7a-af8a-394c7060909c","reqType": "sub","dataType":"BTC-USDT@markPrice"}
```


### Subscribe to the Book Ticker Streams
Push the Book Ticker Streams.

#### Subscription Type
dataType is <symbol>@bookTicker, such as BTC-USDT@bookTicker.

#### Subscription Parameters
Request
```json
{
  "symbol": "string", # Trading pair, e.g., BTC-USDT, please use uppercase letters.
}
```
Response
```json
{
  "code": "", # With regards to error messages, 0 means normal, and 1 means error
  "dataType": "", # Subscribed data type, e.g., BTC-USDT@bookTicker.
  "data": "", # Push content
  "e": "", # Event type
  "u": "", # Update ID
  "E": "", # Event time
  "T": "", # Transaction time
  "s": "", # Trading pair, e.g., BTC-USDT
  "b": "", # Best bid price
  "B": "", # Best bid quantity
  "a": "", # Best ask price
  "A": "" # Best ask quantity
}
{"code":0,"dataType":"BTC-USDT@bookTicker","data":{"e":"bookTicker","u":285099199,"E":1725205790747,"T":1725205790748,"s":"BTC-USDT","b":"58279.4","B":"3.3588","a":"58280.0","A":"0.5331"}}
```
Code
```python
CHANNEL= {"id":"24dd0e35-56a4-4f7a-af8a-394c7060909c","reqType": "sub","dataType":"BTC-USDT@bookTicker"}
```


### Account balance and position update push
The event type of the account update event is fixed as ACCOUNT_UPDATE

When the account information changes, this event will be pushed：
- This event will only be pushed when there is a change in account information (including changes in funds, positions, etc.); This event will not be pushed if the change in the order status does not cause changes in the account and positions;
- position information: push only when there is a change in the symbol position.

Fund balance changes caused by "FUNDING FEE", only push brief events:
- When "FUNDING FEE" occurs in a user's cross position, the event ACCOUNT_UPDATE will only push the relevant user's asset balance information B (only push the asset balance information related to the occurrence of FUNDING FEE), and will not push any position information P.
- When "FUNDING FEE" occurs in a user's isolated position, the event ACCOUNT_UPDATE will only push the relevant user asset balance information B (only push the asset balance information used by "FUNDING FEE"), and related position information P( Only the position information where this "FUNDING FEE" occurred is pushed), and the rest of the position information will not be pushed.

The field "m" represents the reason for the launch of the event, including the following possible types: 
- DEPOSIT
- WITHDRAW
- ORDER
- FUNDING_FEE

> Account data no longer need to subscribe to channel type,after connect wss://open-api-cswap-ws.bingx.com/market?listenKey=a8ea75681542e66f1a50a1616dd06ed77dab61baa0c296bca03a9b13ee5f2dd7 ,All event types will be pushed

> The effective time of the listen key is 1 hour. In order to ensure that your subscription is not interrupted, please update the listen key regularly

#### Push data 
Response
```json
{
  "e": "", # event type:ACCOUNT_UPDATE
  "E": "", # event time：1676603102163
  "T": "", # push timestamp: 1676603102163
  "a": "obj" # account update event
}
```
a
```json
{
  "m": "", # event launch reason
  "B": "", # Array: balance information
  "P": "" # Array: trade info
}
```
B
```json
{
  "a": "", # asset name:USDT
  "wb": "", # wallet balance:5277.59264687
  "cw": "", # Wallet balance excluding isolated margin:5233.21709203
  "bc": "" # wallet balance change amount:0
}
```
P
```json
{
  "s": "", # trading pair:BTC-USDT
  "pa": "", # position:108.84300000
  "ep": "", # entry price:7.25620000
  "up": "", # unrealized profit and loss of positions:1.42220000
  "mt": "", # margin mode:isolated
  "iw": "", # If it is an isolated position, the position margin:23.19081642
  "ps": "" # position direction:SHORT
}
```

Code
```python
import json
import websocket
import gzip
import io
URL="wss://open-api-swap.bingx.com/swap-market?listenKey=a8ea75681542e66f1a50a1616dd06ed77dab61baa0c296bca03a9b13ee5f2dd7" 
CHANNEL= {"notice:":"no need to subscribe to  any specific channel,please check the hightlight msg in the api docs"}
class Test(object):

    def __init__(self):
        self.url = URL 
        self.ws = None

    def on_open(self, ws):
        print('WebSocket connected')
        subStr = json.dumps(CHANNEL)
        ws.send(subStr)
        print("Subscribed to :",subStr)

    def on_data(self, ws, string, type, continue_flag):
        compressed_data = gzip.GzipFile(fileobj=io.BytesIO(string), mode='rb')
        decompressed_data = compressed_data.read()
        utf8_data = decompressed_data.decode('utf-8')
        print(utf8_data)

    def on_message(self, ws, message):
        compressed_data = gzip.GzipFile(fileobj=io.BytesIO(message), mode='rb')
        decompressed_data = compressed_data.read()
        utf8_data = decompressed_data.decode('utf-8')
        print(utf8_data)  #this is the message you need 
        if utf8_data == "Ping": # this is very important , if you receive 'Ping' you need to send 'Pong' 
           ws.send("Pong")

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print('The connection is closed!')

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
    test = Test()
    test.start()
```
