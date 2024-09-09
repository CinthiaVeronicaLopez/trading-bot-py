# BingX API Docs
# USDT-M Perp FuturesCoin-M Perp 
# Trades Endpoints
1. Test Order
2. Place order
3. Place order in demo trading
4. Place multiple orders
5. Close All Positions
6. Cancel Order
7. Cancel multiple orders
8. Cancel All Open Orders
9. Current All Open Orders
10. Query pending order status
11. Query Order details
12. Query Margin Type
13. Change Margin Type
14. Query Leverage
15. Set Leverage
16. User's Force Orders
17. Query Order history
18. Modify Isolated Position Margin
19. Query historical transaction orders
20. Set Position Mode
21. Query position mode
22. Cancel an Existing Order and Send a New Orde
23. Cancel orders in batches and place orders in batches
24. Cancel All After
25. Close position by position ID
26. All Orders
27. Position and Maintenance Margin Ratio
28. Query historical transaction details
29. Query Position History

### Test Order
__HTTP Request https://open-api.bingx.com__

> The participation and return are consistent with the ordering interface, but the actual order will not be placed, only the test results will be returned.The result is a fake order, and your funds will not be deducted. It will not appear on the real transaction panel and is only used to help you practice using the order interface

> Depending on the order type, certain parameters are mandatory:

* LIMIT: Mandatory Parameters: quantity, price
* MARKET: Mandatory Parameters: quantity
* TRAILING_STOP_MARKET (Tracking Stop Loss Order) or TRAILING_TP_SL (Trailing TakeProfit/StopLoss Order): The price field or priceRate field needs to be filled in
* TRIGGER_LIMIT, STOP, TAKE_PROFIT: Mandatory Parameters: quantity、stopPrice、price
* STOP_MARKET, TAKE_PROFIT_MARKET, TRIGGER_MARKET: Mandatory Parameters: quantity、stopPrice

> The triggering of the conditional order must:

#### STOP/STOP_MARKET stop loss order:
* The accumulative quantity of the pending stop loss orders cannot be greater than the quantity of open positions
* Buy: the mark price is higher than or equal to the trigger price stopPrice
* Sell: the mark price is lower than or equal to the trigger price stopPrice

#### TAKE_PROFIT/TAKE_PROFIT_MARKET take profit order:
* The accumulative quantity of the pending take profit order cannot be greater than the position quantity
* Buy: the mark price is lower than or equal to the trigger price stopPrice
* Sell: the mark price is higher than or equal to the trigger price stopPrice

> The minimum order quantity can be obtained from the interface /openApi/swap/v2/quote/contracts: tradeMinQuantity, tradeMinUSDT

#### Trading Rules:
* Trading Rules: https://bingx.com/en/tradeInfo/perpetual/trading-rules/BTC-USDT/
* About price accuracy and quantity accuracy reference interface: https://open-api.bingx.com/openApi/swap/v2/quote/contracts
* If the accuracy exceeds the range of the current period, the current API order will still be successful, but it will be truncated. For example, the price requirement is: 0.0001, if the order is 0.123456, it will be successfully submitted with 0.1234.

1. Create API KEY
2. Configure API KEY permissions  
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

##### request parameters

POST /openApi/swap/v2/trade/order/test
##### rate limitation by UID: 5/s & rate limitation by IP in group Number: 
__API KEY permission:__ Perpetual Futures Trading
Content-Type: request body(application/json) query string
  
Request
```json
{
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
  "type": "string", // LIMIT: Limit Order / MARKET: Market Order / STOP_MARKET: Stop Market Order / TAKE_PROFIT_MARKET: Take Profit Market Order / STOP: Stop Limit Order / TAKE_PROFIT: Take Profit Limit Order / TRIGGER_LIMIT: Stop Limit Order with Trigger / TRIGGER_MARKET: Stop Market Order with Trigger / TRAILING_STOP_MARKET: Trailing Stop Market Order / TRAILING_TP_SL: Trailing TakeProfit or StopLoss
  "side": "string", // buying and selling direction SELL, BUY
  "positionSide": "string", // Position direction, required for single position as BOTH, for both long and short positions only LONG or SHORT can be chosen, defaults to LONG if empty
  "reduceOnly": "string", // true, false; Default value is false for single position mode; This parameter is not accepted for both long and short positions mode
  "price": "float64", // Price, represents the trailing stop distance in TRAILING_STOP_MARKET and TRAILING_TP_SL
  "quantity": "float64", // Original quantity, only support units by COIN ,Ordering with quantity U is not currently supported.
  "stopPrice": "float64", // Trigger price, only required for STOP_MARKET, TAKE_PROFIT_MARKET, STOP, TAKE_PROFIT, TRIGGER_LIMIT, TRIGGER_MARKET
  "priceRate": "float64", // For type: TRAILING_STOP_MARKET or TRAILING_TP_SL; Maximum: 1
  "timestamp": "int64", // request timestamp, unit: millisecond
  "stopLoss": "string", // Support setting stop loss while placing an order. Only supports type: STOP_MARKET/STOP
  "takeProfit": "string", // Support setting take profit while placing an order. Only supports type: TAKE_PROFIT_MARKET/TAKE_PROFIT
  "clientOrderId": "string", // Customized order ID for users, with a limit of characters from 1 to 40. Different orders cannot use the same clientOrderId
  "recvWindow": "int64", // Request valid time window value, Unit: milliseconds
  "timeInForce": "string", // Time in Force, currently supports PostOnly, GTC, IOC, and FOK
  "closePosition": "string", // true, false; all position squaring after triggering, only support STOP_MARKET and TAKE_PROFIT_MARKET; not used with quantity; comes with only position squaring effect, not used with reduceOnly
  "activationPrice": "float64", // Used with TRAILING_STOP_MARKET or TRAILING_TP_SL orders, default as the latest price(supporting different workingType)
  "stopGuaranteed": "string" // true: Enables the guaranteed stop-loss and take-profit feature; false: Disables the feature. The guaranteed stop-loss feature is not enabled by default. Supported order types include: STOP_MARKET: Market stop-loss order / TAKE_PROFIT_MARKET: Market take-profit order / STOP: Limit stop-loss order / TAKE_PROFIT: Limit take-profit order / TRIGGER_LIMIT: Stop-limit order with trigger / TRIGGER_MARKET: Market order with trigger for stop-loss.
}
{
  "symbol": "BTC-USDT",
  "side": "BUY",
  "positionSide": "LONG",
  "type": "MARKET",
  "quantity": 5,
  "takeProfit": "{\"type\": \"TAKE_PROFIT_MARKET\", \"stopPrice\": 31968.0,\"price\": 31968.0,\"workingType\":\"MARK_PRICE\"}"
}
```
stopLoss/takeProfit
``` json
{
  "type": "string", // Only supports type: STOP_MARKET/STOP, TAKE_PROFIT_MARKET/TAKE_PROFIT
  "stopPrice": "float64", // Trigger price, only for STOP_MARKET, TAKE_PROFIT_MARKET, STOP, TAKE_PROFIT
  "price": "float64", // Order price
  "workingType": "string", // Trigger price type for stopPrice: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default is MARK_PRICE. When the type is STOP or STOP_MARKET, and stopGuaranteed is true, the workingType must only be CONTRACT_PRICE.
  "stopGuaranteed": "string" // true: Enables the guaranteed stop-loss and take-profit feature; false: Disables the feature. The guaranteed stop-loss feature is not enabled by default. Supported order types include: STOP_MARKET: Market stop-loss order / TAKE_PROFIT_MARKET: Market take-profit order / STOP: Limit stop-loss order / TAKE_PROFIT: Limit take-profit order / TRIGGER_LIMIT: Stop-limit order with trigger / TRIGGER_MARKET: Market order with trigger for stop-loss.
}
```
Response
``` json
{
  "symbol": "string", // trading pair, for example: BTC-USDT
  "side": "string", // buying and selling direction
  "type": "string", // LIMIT: Limit Order / MARKET: Market Order / STOP_MARKET: Stop Market Order / TAKE_PROFIT_MARKET: Take Profit Market Order / STOP: Stop Limit Order / TAKE_PROFIT: Take Profit Limit Order / TRIGGER_LIMIT: Stop Limit Order with Trigger / TRIGGER_MARKET: Stop Market Order with Trigger / TRAILING_STOP_MARKET: Trailing Stop Market Order / TRAILING_TP_SL: Trailing TakeProfit or StopLoss
  "positionSide": "string", // Position direction, required for single position as BOTH, for both long and short positions only LONG or SHORT can be chosen, defaults to LONG if empty
  "reduceOnly": "string", // true, false; Default value is false for single position mode; This parameter is not accepted for both long and short positions mode
  "orderId": "int64", // Order ID
  "clientOrderId": "string", // Customized order ID for users
  "stopGuaranteed": "string" // true: Enables the guaranteed stop-loss and take-profit feature; false: Disables the feature. The guaranteed stop-loss feature is not enabled by default. Supported order types include: STOP_MARKET: Market stop-loss order / TAKE_PROFIT_MARKET: Market take-profit order / STOP: Limit stop-loss order / TAKE_PROFIT: Limit take-profit order / TRIGGER_LIMIT: Stop-limit order with trigger / TRIGGER_MARKET: Market order with trigger for stop-loss.
}
{
  "code": 0,
  "msg": "",
  "data": {
    "order": {
      "symbol": "BTC-USDT",
      "orderId": 1735950529123455000,
      "side": "BUY",
      "positionSide": "LONG",
      "type": "MARKET",
      "clientOrderId": "",
      "workingType": "MARK_PRICE"
    }
  }
}
```

### Sample code
```python
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/order/test'
    method = "POST"
    paramsMap = {
    "symbol": "BTC-USDT",
    "side": "BUY",
    "positionSide": "LONG",
    "type": "MARKET",
    "quantity": 5,
    "takeProfit": "{\"type\": \"TAKE_PROFIT_MARKET\", \"stopPrice\": 31968.0,\"price\": 31968.0,\"workingType\":\"MARK_PRICE\"}"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())
```


### Place order
The current account places an order on the specified symbol contract. (Supports limit order, market order, market order for plan entrustment, limit order for plan entrustment, position stop profit and stop loss order, and liquidation for positions)
#### HTTP Request https://open-api.bingx.com

> Depending on the order type, certain parameters are mandatory:

* LIMIT: Mandatory Parameters: quantity, price
* MARKET: Mandatory Parameters: quantity
* TRAILING_STOP_MARKET (Tracking Stop Loss Order) or TRAILING_TP_SL (Trailing TakeProfit/StopLoss Order): The price field or priceRate field needs to be filled in
* TRIGGER_LIMIT, STOP, TAKE_PROFIT: Mandatory Parameters: quantity、stopPrice、price
* STOP_MARKET, TAKE_PROFIT_MARKET, TRIGGER_MARKET: Mandatory Parameters: quantity、stopPrice

### 1. Open/Close: How to use the same endpoint to open (Long/Short) and close (Long/Short) positions? Please refer to the following request payload combination:

open/buy LONG: side=BUY & positionSide=LONG
close/sell LONG: side=SELL & positionSide=LONG
open/sell SHORT: side=SELL & positionSide=SHORT
close/buy SHORT: side=BUY & positionSide=SHORT
```json
{"symbol": "ETH-USDT","side": "BUY","positionSide": "LONG", "type": "MARKET", "quantity": 5}
```

### 2. Set take profit and stop loss: This endpoint can also be used to set take profit and stop loss, but the position needs to be opened first;
```json
{"symbol": "ETH-USDT","side": "BUY","positionSide": "LONG", "type": "TAKE_PROFIT_MARKET", "quantity": 3, "stopPrice": 31968.0}
```

### 3. set stopLoss and takeProfit when open position:using takeProfit and stopLoss fields
```json
{"symbol": "BTC-USDT","side": "BUY","positionSide": "LONG","type": "MARKET","quantity": 5,"takeProfit": "{\"type\": \"TAKE_PROFIT_MARKET\", \"stopPrice\": 31968.0,\"price\": 31968.0,\"workingType\":\"MARK_PRICE\"}"}
```

> The triggering of the conditional order must:

### STOP/STOP_MARKET stop loss order:
* The accumulative quantity of the pending stop loss orders cannot be greater than the quantity of open positions
* Buy: the mark price is higher than or equal to the trigger price stopPrice
* Sell: the mark price is lower than or equal to the trigger price stopPrice

### TAKE_PROFIT/TAKE_PROFIT_MARKET take profit order:
* The accumulative quantity of the pending take profit order cannot be greater than the position quantity
* Buy: the mark price is lower than or equal to the trigger price stopPrice
* Sell: the mark price is higher than or equal to the trigger price stopPrice

> The minimum order quantity can be obtained from the interface /openApi/swap/v2/quote/contracts: tradeMinQuantity, tradeMinUSDT

### Trading Rules:
* Trading Rules: https://bingx.com/en/tradeInfo/perpetual/trading-rules/BTC-USDT/
* About price accuracy and quantity accuracy reference interface: https://open-api.bingx.com/openApi/swap/v2/quote/contracts
* If the accuracy exceeds the range of the current period, the current API order will still be successful, but it will be truncated. For example, the price requirement is: 0.0001, if the order is 0.123456, it will be successfully submitted with 0.1234.

1. Create API KEY  
2. Configure API KEY permissions  
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
POST /openApi/swap/v2/trade/order

#### rate limitation by UID: 5/s & rate limitation by IP in group Number: 3
__API KEY permission:__ Perpetual Futures Trading
Content-Type: request body (application/json) query string

Request
```json
{
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
  "type": "string", // LIMIT: Limit Order / MARKET: Market Order / STOP_MARKET: Stop Market Order / TAKE_PROFIT_MARKET: Take Profit Market Order / STOP: Stop Limit Order / TAKE_PROFIT: Take Profit Limit Order / TRIGGER_LIMIT: Stop Limit Order with Trigger / TRIGGER_MARKET: Stop Market Order with Trigger / TRAILING_STOP_MARKET: Trailing Stop Market Order / TRAILING_TP_SL: Trailing TakeProfit or StopLoss
  "side": "string", // buying and selling direction SELL, BUY
  "positionSide": "string", // Position direction, required for single position as BOTH, for both long and short positions only LONG or SHORT can be chosen, defaults to LONG if empty
  "reduceOnly": "string", // true, false; Default value is false for single position mode; This parameter is not accepted for both long and short positions mode
  "price": "float64", // Price, represents the trailing stop distance in TRAILING_STOP_MARKET and TRAILING_TP_SL
  "quantity": "float64", // Original quantity, only support units by COIN ,Ordering with quantity U is not currently supported.
  "stopPrice": "float64", // Trigger price, only required for STOP_MARKET, TAKE_PROFIT_MARKET, STOP, TAKE_PROFIT, TRIGGER_LIMIT, TRIGGER_MARKET
  "priceRate": "float64", // For type: TRAILING_STOP_MARKET or TRAILING_TP_SL; Maximum: 1
  "timestamp": "int64", // request timestamp, unit: millisecond
  "stopLoss": "string", // Support setting stop loss while placing an order. Only supports type: STOP_MARKET/STOP
  "takeProfit": "string", // Support setting take profit while placing an order. Only supports type: TAKE_PROFIT_MARKET/TAKE_PROFIT
  "clientOrderId": "string", // Customized order ID for users, with a limit of characters from 1 to 40. Different orders cannot use the same clientOrderId
  "recvWindow": "int64", // Request valid time window value, Unit: milliseconds
  "timeInForce": "string", // Time in Force, currently supports PostOnly, GTC, IOC, and FOK
  "closePosition": "string", // true, false; all position squaring after triggering, only support STOP_MARKET and TAKE_PROFIT_MARKET; not used with quantity; comes with only position squaring effect, not used with reduceOnly
  "activationPrice": "float64", // Used with TRAILING_STOP_MARKET or TRAILING_TP_SL orders, default as the latest price(supporting different workingType)
  "stopGuaranteed": "string" // true: Enables the guaranteed stop-loss and take-profit feature; false: Disables the feature. The guaranteed stop-loss feature is not enabled by default. Supported order types include: STOP_MARKET: Market stop-loss order / TAKE_PROFIT_MARKET: Market take-profit order / STOP: Limit stop-loss order / TAKE_PROFIT: Limit take-profit order / TRIGGER_LIMIT: Stop-limit order with trigger / TRIGGER_MARKET: Market order with trigger for stop-loss.
}
{
  "symbol": "BTC-USDT",
  "side": "BUY",
  "positionSide": "LONG",
  "type": "MARKET",
  "quantity": 5,
  "takeProfit": "{\"type\": \"TAKE_PROFIT_MARKET\", \"stopPrice\": 31968.0,\"price\": 31968.0,\"workingType\":\"MARK_PRICE\"}"
}
```
stopLoss/takeProfit
``` json
{
  "type": "string", // Only supports type: STOP_MARKET/STOP, TAKE_PROFIT_MARKET/TAKE_PROFIT
  "stopPrice": "float64", // Trigger price, only for STOP_MARKET, TAKE_PROFIT_MARKET, STOP, TAKE_PROFIT
  "price": "float64", // Order price
  "workingType": "string", // Trigger price type for stopPrice: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default is MARK_PRICE. When the type is STOP or STOP_MARKET, and stopGuaranteed is true, the workingType must only be CONTRACT_PRICE.
  "stopGuaranteed": "string" // true: Enables the guaranteed stop-loss and take-profit feature; false: Disables the feature. The guaranteed stop-loss feature is not enabled by default. Supported order types include: STOP_MARKET: Market stop-loss order / TAKE_PROFIT_MARKET: Market take-profit order / STOP: Limit stop-loss order / TAKE_PROFIT: Limit take-profit order / TRIGGER_LIMIT: Stop-limit order with trigger / TRIGGER_MARKET: Market order with trigger for stop-loss.
}
```
Response
``` json
{
  "symbol": "string", // trading pair, for example: BTC-USDT
  "side": "string", // buying and selling direction
  "type": "string", // LIMIT: Limit Order / MARKET: Market Order / STOP_MARKET: Stop Market Order / TAKE_PROFIT_MARKET: Take Profit Market Order / STOP: Stop Limit Order / TAKE_PROFIT: Take Profit Limit Order / TRIGGER_LIMIT: Stop Limit Order with Trigger / TRIGGER_MARKET: Stop Market Order with Trigger / TRAILING_STOP_MARKET: Trailing Stop Market Order / TRAILING_TP_SL: Trailing TakeProfit or StopLoss
  "positionSide": "string", // Position direction, required for single position as BOTH, for both long and short positions only LONG or SHORT can be chosen, defaults to LONG if empty
  "reduceOnly": "string", // true, false; Default value is false for single position mode; This parameter is not accepted for both long and short positions mode
  "orderId": "int64", // Order ID
  "clientOrderId": "string", // Customized order ID for users
  "stopGuaranteed": "string" // true: Enables the guaranteed stop-loss and take-profit feature; false: Disables the feature. The guaranteed stop-loss feature is not enabled by default. Supported order types include: STOP_MARKET: Market stop-loss order / TAKE_PROFIT_MARKET: Market take-profit order / STOP: Limit stop-loss order / TAKE_PROFIT: Limit take-profit order / TRIGGER_LIMIT: Stop-limit order with trigger / TRIGGER_MARKET: Market order with trigger for stop-loss.
}
{
  "code": 0,
  "msg": "",
  "data": {
    "order": {
      "symbol": "BTC-USDT",
      "orderId": 1735950529123455000,
      "side": "BUY",
      "positionSide": "LONG",
      "type": "MARKET",
      "clientOrderId": "",
      "workingType": "MARK_PRICE"
    }
  }
}
```

### Sample code

```python
# import time
# import requests
# import hmac
# from hashlib import sha256

# APIURL = "https://open-api.bingx.com"
# APIKEY = ""
# SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/order'
    method = "POST"
    paramsMap = {
      "symbol": "BTC-USDT",
      "side": "BUY",
      "positionSide": "LONG",
      "type": "MARKET",
      "quantity": 5,
      "takeProfit": "{\"type\": \"TAKE_PROFIT_MARKET\", \"stopPrice\": 31968.0,\"price\": 31968.0,\"workingType\":\"MARK_PRICE\"}"
    }
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)


def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text


def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())
```

## Place order in demo trading
The current account places an order on the specified symbol contract. (Supports limit order, market order, market order for plan entrustment, limit order for plan entrustment, position stop profit and stop loss order, and liquidation for positions)
> demo trading domain: open-api-vst.bingx.com

## Place multiple orders
The current account performs batch order operations on the specified symbol contract.
#### HTTP Request https://open-api.bingx.com

* Specific order conditions and rules are consistent with ordinary orders

* BatchOrders is kind of difficult but do not worry, please refer to 4 steps below:
1. make your payload to string

    original parameters:

    batchOrders=[{"symbol":"ETH-USDT","type":"MARKET","side":"BUY","positionSide":"LONG","quantity":1},{"symbol":"BTC-USDT","type":"MARKET","side":"BUY","positionSide":"LONG","quantity":0.001}]&timestamp=1692956597902
2. sign original parameters

    signature: bab521321a62a1381a76b485b92dd0f4a8b16b4616cfa4c75ffba899f80dfc86
3. url encode each value,for example the value of batchOrders field,except timestamp field value (not url encode the key, not url encode entire original parametersg), make it like below:
    
    after url encoded: 
    
    batchOrders=%5B%7B%22symbol%22%3A%22ETH-USDT%22%2C%22type%22%3A%22MARKET%22%2C%22side%22%3A%22BUY%22%2C%22positionSide%22%3A%22LONG%22%2C%22quantity%22%3A1%7D%2C%7B%22symbol%22%3A%22BTC-USDT%22%2C%22type%22%3A%22MARKET%22%2C%22side%22%3A%22BUY%22%2C%22positionSide%22%3A%22LONG%22%2C%22quantity%22%3A0.001%7D%5D&timestamp=1692956597902

4. final request should be like

    > Batch orders are processed concurrently, and order matching order is not guaranteed

    > The minimum order quantity can be obtained from the interface /openApi/swap/v2/quote/contracts: tradeMinQuantity, tradeMinUSDT

### Trading Rules:
* Trading Rules: https://bingx.com/en/tradeInfo/perpetual/trading-rules/BTC-USDT/
* About price accuracy and quantity accuracy reference interface: https://open-api.bingx.com/openApi/swap/v2/quote/contracts
* If the accuracy exceeds the range of the current period, the current API order will still be successful, but it will be truncated. For example, the price requirement is: 0.0001, if the order is 0.123456, it will be successfully submitted with 0.1234.

1. Create API KEY  
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

### request parameters
POST /openApi/swap/v2/trade/batchOrders

### rate limitation by UID: 5/s & rate limitation by IP in group Number: 
__API KEY permission:__ Perpetual Futures Trading
Content-Type: request body (application/json) query string
  
Request
```json
{
  "batchOrders": "LIST<Order>", // Order list, supporting up to 5 orders, with Order objects referencing transactions to place orders
  "timestamp": "int64", // request timestamp, unit: millisecond
  "recvWindow": "int64" // Request valid time window value, Unit: milliseconds
}
{ // Demo
  "batchOrders": "[{\"symbol\": \"ETH-USDT\",\"type\": \"MARKET\",\"side\": \"BUY\",\"positionSide\": \"LONG\",\"quantity\": 1},{\"symbol\": \"BTC-USDT\",\"type\": \"MARKET\",\"side\": \"BUY\",\"positionSide\": \"LONG\",\"quantity\": 0.001}]"
}
```
Order
```json
{
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
  "type": "string", // LIMIT: Limit Order / MARKET: Market Order / STOP_MARKET: Stop Market Order / TAKE_PROFIT_MARKET: Take Profit Market Order / STOP: Stop Limit Order / TAKE_PROFIT: Take Profit Limit Order / TRIGGER_LIMIT: Stop Limit Order with Trigger / TRIGGER_MARKET: Stop Market Order with Trigger / TRAILING_STOP_MARKET: Trailing Stop Market Order / TRAILING_TP_SL: Trailing TakeProfit or StopLoss
  "side": "string", // buying and selling direction SELL, BUY
  "positionSide": "string", // Position direction, required for single position as BOTH, for both long and short positions only LONG or SHORT can be chosen, defaults to LONG if empty
  "reduceOnly": "string", // true, false; Default value is false for single position mode; This parameter is not accepted for both long and short positions mode
  "price": "float64", // Price, represents the trailing stop distance in TRAILING_STOP_MARKET and TRAILING_TP_SL
  "quantity": "float64", // Original quantity, only support units by COIN ,Ordering with quantity U is not currently supported.
  "stopPrice": "float64", // Trigger price, only required for STOP_MARKET, TAKE_PROFIT_MARKET, STOP, TAKE_PROFIT, TRIGGER_LIMIT, TRIGGER_MARKET
  "priceRate": "float64", // For type: TRAILING_STOP_MARKET or TRAILING_TP_SL; Maximum: 1
  "stopLoss": "string", // Support setting stop loss while placing an order. Only supports type: STOP_MARKET/STOP
  "takeProfit": "string", // Support setting take profit while placing an order. Only supports type: TAKE_PROFIT_MARKET/TAKE_PROFIT
  "timestamp": "int64", // request timestamp, unit: millisecond
  "clientOrderId": "string", // Customized order ID for users, with a limit of characters from 1 to 40. Different orders cannot use the same clientOrderId
  "recvWindow": "int64", // Request valid time window value, Unit: milliseconds
  "workingType": "string", // StopPrice trigger price types: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default MARK_PRICE. When the type is STOP or STOP_MARKET, and stopGuaranteed is true, the workingType must only be CONTRACT_PRICE.
  "timeInForce": "string", // Time in Force, currently supports PostOnly, GTC, IOC, and FOK
  "closePosition": "string", // true, false; all position squaring after triggering, only support STOP_MARKET and TAKE_PROFIT_MARKET; not used with quantity; comes with only position squaring effect, not used with reduceOnly
  "activationPrice": "float64", // Used with TRAILING_STOP_MARKET or TRAILING_TP_SL orders, default as the latest price(supporting different workingType)
  "stopGuaranteed": "string" // true: Enables the guaranteed stop-loss and take-profit feature; false: Disables the feature. The guaranteed stop-loss feature is not enabled by default. Supported order types include: STOP_MARKET: Market stop-loss order / TAKE_PROFIT_MARKET: Market take-profit order / STOP: Limit stop-loss order / TAKE_PROFIT: Limit take-profit order / TRIGGER_LIMIT: Stop-limit order with trigger / TRIGGER_MARKET: Market order with trigger for stop-loss.
}
```
stopLoss/takeProfit
```json
{
  "type": "string", // Only supports type: STOP_MARKET/STOP, TAKE_PROFIT_MARKET/TAKE_PROFIT
  "stopPrice": "float64", // Trigger price, only for STOP_MARKET, TAKE_PROFIT_MARKET, STOP, TAKE_PROFIT
  "price": "float64", // Order price
  "workingType": "string", // Trigger price type for stopPrice: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default is MARK_PRICE. When the type is STOP or STOP_MARKET, and stopGuaranteed is true, the workingType must only be CONTRACT_PRICE.
  "stopGuaranteed": "string" // true: Enables the guaranteed stop-loss and take-profit feature; false: Disables the feature. The guaranteed stop-loss feature is not enabled by default. Supported order types include: STOP_MARKET: Market stop-loss order / TAKE_PROFIT_MARKET: Market take-profit order / STOP: Limit stop-loss order / TAKE_PROFIT: Limit take-profit order / TRIGGER_LIMIT: Stop-limit order with trigger / TRIGGER_MARKET: Market order with trigger for stop-loss.
}
```
Response
```json
{
  "symbol": "string", // trading pair, for example: BTC-USDT
  "side": "string", // buying and selling direction
  "type": "string", // LIMIT: Limit Order / MARKET: Market Order / STOP_MARKET: Stop Market Order / TAKE_PROFIT_MARKET: Take Profit Market Order / STOP: Stop Limit Order / TAKE_PROFIT: Take Profit Limit Order / TRIGGER_LIMIT: Stop Limit Order with Trigger / TRIGGER_MARKET: Stop Market Order with Trigger / TRAILING_STOP_MARKET: Trailing Stop Market Order / TRAILING_TP_SL: Trailing TakeProfit or StopLoss
  "positionSide": "string", // Position direction, required for single position as BOTH, for both long and short positions only LONG or SHORT can be chosen, defaults to LONG if empty
  "reduceOnly": "string", // true, false; Default value is false for single position mode; This parameter is not accepted for both long and short positions mode
  "orderId": "int64", // Order ID
  "clientOrderId": "string", // Customized order ID for users
  "stopGuaranteed": "string" // true: Enables the guaranteed stop-loss and take-profit feature; false: Disables the feature. The guaranteed stop-loss feature is not enabled by default. Supported order types include: STOP_MARKET: Market stop-loss order / TAKE_PROFIT_MARKET: Market take-profit order / STOP: Limit stop-loss order / TAKE_PROFIT: Limit take-profit order / TRIGGER_LIMIT: Stop-limit order with trigger / TRIGGER_MARKET: Market order with trigger for stop-loss.
}
{
  "code": 0,
  "msg": "",
  "data": {
    "orders": [
      {
        "symbol": "ID-USDT",
        "orderId": 1736010300483712300,
        "side": "SELL",
        "positionSide": "LONG",
        "type": "MARKET",
        "clientOrderId": "",
        "workingType": ""
      }
    ]
  }
}
```
### Sample code
```python

import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/batchOrders'
    method = "POST"
    paramsMap = {
      "batchOrders": "[{\"symbol\": \"ETH-USDT\",\"type\": \"MARKET\",\"side\": \"BUY\",\"positionSide\": \"LONG\",\"quantity\": 1},{\"symbol\": \"BTC-USDT\",\"type\": \"MARKET\",\"side\": \"BUY\",\"positionSide\": \"LONG\",\"quantity\": 0.001}]"
    }
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())
```

## Close All Positions
One-click liquidation of all positions under the current account. Note that one-click liquidation is triggered by a market order.

#### HTTP Request https://open-api.bingx.com
1. Create API KEY
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
    POST /openApi/swap/v2/trade/closeAllPositions

#### rate limitation by UID: 5/s & rate limitation by IP in group Number: 2
__API KEY permission:__ Perpetual Futures Trading
Content-Type: request body (application/json)
  
Request
```json
{
  "symbol": "string", // Trading pair, for example: BTC-USDT, please use capital letters.
  "timestamp": "int64", // request timestamp in milliseconds
  "recvWindow": "int64" // Request valid time window value, Unit: milliseconds
}
{ // Demo
  "timestamp": "1702731721672",
  "symbol": "BTC-USDT"
}
```
Response
```json
{
  "success": "LIST<int64>", // Multiple order numbers generated by all one-click liquidation
  "failed": "array" // the order number of the failed position closing
}
{ // Demo
  "code": 0,
  "msg": "",
  "data": {
    "success": [
      1736008778921491200
    ],
    "failed": null
  }
}
```

### Sample code
```python

import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/closeAllPositions'
    method = "POST"
    paramsMap = {
    "timestamp": "1702731721672",
    "symbol": "BTC-USDT"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())
```


## Cancel Order
Cancel an order that the current account is in the current entrusted state.

#### HTTP Request https://open-api.bingx.com

>The cancellation interface is limited to one second and can only cancel the same orderId or clientOrderId. Please do not resubmit

1. Create API KEY
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
    DELETE /openApi/swap/v2/trade/order

#### rate limitation by UID: 5/s & rate limitation by IP in group Number: 3

__API KEY permission:__ Perpetual Futures Trading

Content-Type: request body (application/json) query string

Request
```json
{
  "orderId": "int64", // Order ID
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
  "clientOrderId": "string", // Customized order ID for users, with a limit of characters from 1 to 40. The system will convert this field to lowercase. Different orders cannot use the same clientOrderId
  "timestamp": "int64", // request timestamp, unit: millisecond
  "recvWindow": "int64" // Request valid time window value, Unit: milliseconds
}
{ // Demo
  "orderId": "1736011869418901234",
  "symbol": "RNDR-USDT",
  "timestamp": "1702732515704"
}
```
Response
```json
{
  "time": "int64", // order time, unit: millisecond
  "symbol": "string", // trading pair, for example: BTC-USDT
  "side": "string", // buying and selling direction
  "type": "string", // LIMIT: Limit Order / MARKET: Market Order / STOP_MARKET: Stop Market Order / TAKE_PROFIT_MARKET: Take Profit Market Order / STOP: Stop Limit Order / TAKE_PROFIT: Take Profit Limit Order / TRIGGER_LIMIT: Stop Limit Order with Trigger / TRIGGER_MARKET: Stop Market Order with Trigger / TRAILING_STOP_MARKET: Trailing Stop Market Order
  "positionSide": "string", // position side
  "cumQuote": "string", // transaction amount
  "status": "string", // order status
  "stopPrice": "string", // Trigger price
  "price": "string", // Price
  "origQty": "string", // original order quantity
  "avgPrice": "string", // average transaction price
  "executedQty": "string", // volume
  "orderId": "int64", // Order ID
  "profit": "string", // profit and loss
  "commission": "string", // Fee
  "updateTime": "int64", // update time, unit: millisecond
  "clientOrderId": "string" // Customized order ID for users. The system will convert this field to lowercase.
}
{ // Demo
  "code": 0,
  "msg": "",
  "data": {
    "order": {
      "symbol": "RNDR-USDT",
      "orderId": 1736011869418901200,
      "side": "BUY",
      "positionSide": "LONG",
      "type": "LIMIT",
      "origQty": "3",
      "price": "4.5081",
      "executedQty": "0",
      "avgPrice": "0.0000",
      "cumQuote": "0",
      "stopPrice": "",
      "profit": "0.0000",
      "commission": "0.000000",
      "status": "CANCELLED",
      "time": 1702732457867,
      "updateTime": 1702732457888,
      "clientOrderId": "lo******7",
      "leverage": "",
      "takeProfit": {
        "type": "",
        "quantity": 0,
        "stopPrice": 0,
        "price": 0,
        "workingType": ""
      },
      "stopLoss": {
        "type": "",
        "quantity": 0,
        "stopPrice": 0,
        "price": 0,
        "workingType": ""
      },
      "advanceAttr": 0,
      "positionID": 0,
      "takeProfitEntrustPrice": 0,
      "stopLossEntrustPrice": 0,
      "orderType": "",
      "workingType": ""
    }
  }
}
```


## Cancel multiple orders
Batch cancellation of some of the orders whose current account is in the current entrusted state.

#### HTTP Request https://open-api.bingx.com
1. Create API KEY 
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
    DELETE /openApi/swap/v2/trade/batchOrders

#### rate limitation by UID: 5/s & rate limitation by IP in group Number: 3
__API KEY permission:__ Perpetual Futures Trading

Content-Type: request body (application/json) query string
  
Request
```json
{
  "orderIdList": "LIST<int64>", // system order number, up to 10 orders [1234567,2345678]
  "clientOrderIdList": "LIST<string>", // Customized order ID for users, up to 10 orders ["abc1234567","abc2345678"]. The system will convert this field to lowercase.
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
  "timestamp": "int64", // request timestamp, unit: millisecond
  "recvWindow": "int64" // Request valid time window value, Unit: milliseconds
}
{ // Demo
  "orderIdList": "[1735924831603391122, 1735924833239172233]",
  "symbol": "BTC-USDT",
  "timestamp": "1702711750843"
}
```
Response
```json
{
  "code": "int64", // error code, 0 means successfully response, others means response failure
  "msg": "string", // Error Details Description
  "success": "LIST<Order>", // list of successfully canceled orders
  "failed": "array", // list of failed orders
  "orderId": "int64", // Order ID
  "errorCode": "int64", // error code, 0 means successfully response, others means response failure
  "errorMessage": "string" // Error Details Description
}
{
  "code": 0,
  "msg": "",
  "data": {
    "success": [
      {
        "symbol": "BTC-USDT",
        "orderId": 1735924831603391200,
        "side": "BUY",
        "positionSide": "LONG",
        "type": "LIMIT",
        "origQty": "0.0032",
        "price": "41682.9",
        "executedQty": "0.0000",
        "avgPrice": "0.0",
        "cumQuote": "0",
        "stopPrice": "",
        "profit": "0.0000",
        "commission": "0.000000",
        "status": "CANCELLED",
        "time": 1702711706435,
        "updateTime": 1702711706453,
        "clientOrderId": "",
        "leverage": "",
        "takeProfit": {
          "type": "",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": ""
        },
        "stopLoss": {
          "type": "",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": ""
        },
        "advanceAttr": 0,
        "positionID": 0,
        "takeProfitEntrustPrice": 0,
        "stopLossEntrustPrice": 0,
        "orderType": "",
        "workingType": ""
      },
      {
        "symbol": "BTC-USDT",
        "orderId": 1735924833239172400,
        "side": "BUY",
        "positionSide": "LONG",
        "type": "LIMIT",
        "origQty": "0.0033",
        "price": "41182.9",
        "executedQty": "0.0000",
        "avgPrice": "0.0",
        "cumQuote": "0",
        "stopPrice": "",
        "profit": "0.0000",
        "commission": "0.000000",
        "status": "CANCELLED",
        "time": 1702711706825,
        "updateTime": 1702711706838,
        "clientOrderId": "",
        "leverage": "",
        "takeProfit": {
          "type": "",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": ""
        },
        "stopLoss": {
          "type": "",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": ""
        },
        "advanceAttr": 0,
        "positionID": 0,
        "takeProfitEntrustPrice": 0,
        "stopLossEntrustPrice": 0,
        "orderType": "",
        "workingType": ""
      }
    ],
    "failed": null
  }
}
```
Order
```json
{
  "time": "int64", // order time, unit: millisecond
  "symbol": "string", // trading pair, for example: BTC-USDT
  "side": "string", // buying and selling direction
  "type": "string", // LIMIT: Limit Order / MARKET: Market Order / STOP_MARKET: Stop Market Order / TAKE_PROFIT_MARKET: Take Profit Market Order / STOP: Stop Limit Order / TAKE_PROFIT: Take Profit Limit Order / TRIGGER_LIMIT: Stop Limit Order with Trigger / TRIGGER_MARKET: Stop Market Order with Trigger / TRAILING_STOP_MARKET: Trailing Stop Market Order
  "positionSide": "string", // position side
  "cumQuote": "string", // transaction amount
  "status": "string", // order status
  "stopPrice": "string", // Trigger price
  "price": "string", // Price
  "origQty": "string", // original order quantity
  "avgPrice": "string", // average transaction price
  "executedQty": "string", // volume
  "orderId": "int64", // Order ID
  "profit": "string", // profit and loss
  "commission": "string", // Fee
  "updateTime": "int64", // update time, unit: millisecond
  "clientOrderId": "string" // Customized order ID for users. The system will convert this field to lowercase.
}
```
### Sample code
```python

import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/batchOrders'
    method = "DELETE"
    paramsMap = {
    "orderIdList": "[1735924831603391122, 1735924833239172233]",
    "symbol": "BTC-USDT",
    "timestamp": "1702711750843"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())
```


## Cancel All Open Orders
Cancel all orders in the current entrusted state of the current account.

#### HTTP Request https://open-api.bingx.com
1. Create API KEY
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
    DELETE /openApi/swap/v2/trade/allOpenOrders

#### rate limitation by UID: 5/s & rate limitation by IP in group Number: 2
__API KEY permission:__ Perpetual Futures Trading
Content-Type: request body (application/json) query string
  
Request
```json
{
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT,if you do not fill this field,will delete all type of orders
  "timestamp": "int64", // request timestamp in milliseconds
  "recvWindow": "int64" // Request valid time window value, Unit: milliseconds
}
{
  "recvWindow": "0",
  "symbol": "ATOM-USDT",
  "timestamp": "1702732849363"
}
```
Response
```json
{
  "success": "LIST<Order>", // list of successfully canceled orders
  "failed": "LIST<FailedOrder>" // list of failed orders
}
{
  "code": 0,
  "msg": "",
  "data": {
    "success": [
      {
        "symbol": "ATOM-USDT",
        "orderId": 1736013373487123500,
        "side": "SELL",
        "positionSide": "SHORT",
        "type": "LIMIT",
        "origQty": "3.00",
        "price": "13.044",
        "executedQty": "0.00",
        "avgPrice": "0.000",
        "cumQuote": "0",
        "stopPrice": "",
        "profit": "0",
        "commission": "0",
        "status": "CANCELLED",
        "time": 1702732816465,
        "updateTime": 1702732816488,
        "clientOrderId": "",
        "leverage": "",
        "takeProfit": {
          "type": "",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": ""
        },
        "stopLoss": {
          "type": "",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": ""
        },
        "advanceAttr": 0,
        "positionID": 0,
        "takeProfitEntrustPrice": 0,
        "stopLossEntrustPrice": 0,
        "orderType": "",
        "workingType": ""
      },
      {
        "symbol": "ATOM-USDT",
        "orderId": 1736013373487123500,
        "side": "BUY",
        "positionSide": "SHORT",
        "type": "LIMIT",
        "origQty": "3.00",
        "price": "11.292",
        "executedQty": "0.00",
        "avgPrice": "0.000",
        "cumQuote": "0",
        "stopPrice": "",
        "profit": "0",
        "commission": "0",
        "status": "CANCELLED",
        "time": 1702732816820,
        "updateTime": 1702732816839,
        "clientOrderId": "",
        "leverage": "",
        "takeProfit": {
          "type": "",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": ""
        },
        "stopLoss": {
          "type": "",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": ""
        },
        "advanceAttr": 0,
        "positionID": 0,
        "takeProfitEntrustPrice": 0,
        "stopLossEntrustPrice": 0,
        "orderType": "",
        "workingType": ""
      }
    ],
    "failed": [
      {
        "orderId": 111111,
        "clientOrderId": "111111",
        "errorCode": 80012,
        "errorMessage": "cancel order failed"
      },
      {
        "orderId": 222222,
        "clientOrderId": "222222",
        "errorCode": 80012,
        "errorMessage": "cancel order failed"
      }
    ]
  }
}
```
Order
```json
{
  "time": "int64", // order time, unit: millisecond
  "symbol": "string", // trading pair, for example: BTC-USDT
  "side": "string", // buying and selling direction
  "type": "string", // LIMIT: Limit Order / MARKET: Market Order / STOP_MARKET: Stop Market Order / TAKE_PROFIT_MARKET: Take Profit Market Order / STOP: Stop Limit Order / TAKE_PROFIT: Take Profit Limit Order / TRIGGER_LIMIT: Stop Limit Order with Trigger / TRIGGER_MARKET: Stop Market Order with Trigger / TRAILING_STOP_MARKET: Trailing Stop Market Order
  "positionSide": "string", // position side
  "cumQuote": "string", // transaction amount
  "status": "string", // order status
  "stopPrice": "string", // Trigger price
  "price": "string", // Price
  "origQty": "string", // original order quantity
  "avgPrice": "string", // average transaction price
  "executedQty": "string", // volume
  "orderId": "int64", // Order ID
  "profit": "string", // profit and loss
  "commission": "string", // Fee
  "updateTime": "int64" // update time, unit: millisecond
}
```
FailOrder
```json
{
  "orderId": "int64", // Order ID
  "clientOrderId": "string", // Customized order ID for users
  "errorCode": "int64", // error code, 0 means successfully response, others means response failure
  "errorMessage": "string" // Error Details Description
}
```

### Sample code
```python
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/allOpenOrders'
    method = "DELETE"
    paramsMap = {
    "recvWindow": "0",
    "symbol": "ATOM-USDT",
    "timestamp": "1702732849363"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())
```


## Current All Open Orders
Query all orders that the user is currently entrusted with.

#### HTTP Request https://open-api.bingx.com
1. Create API KEY
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
    GET /openApi/swap/v2/trade/openOrders

#### rate limitation by UID: 5/s & rate limitation by IP in group Number: 
__API KEY permission:__ Perpetual Futures Trading
Content-Type: request body (application/json) query string

Request
```json
{
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT,When not filled, query all pending orders. When filled, query the pending orders for the corresponding currency pair
  "timestamp": "int64", // request timestamp in milliseconds
  "recvWindow": "int64" // Request valid time window value, Unit: milliseconds
}
{
  "symbol": "BTC-USDT",
  "timestamp": "1702733126509"
}
```
Response
```json
{
  "time": "int64", // order time, unit: millisecond
  "symbol": "string", // trading pair, for example: BTC-USDT
  "side": "string", // buying and selling direction
  "type": "string", // LIMIT: Limit Order / MARKET: Market Order / STOP_MARKET: Stop Market Order / TAKE_PROFIT_MARKET: Take Profit Market Order / STOP: Stop Limit Order / TAKE_PROFIT: Take Profit Limit Order / TRIGGER_LIMIT: Stop Limit Order with Trigger / TRIGGER_MARKET: Stop Market Order with Trigger / TRAILING_STOP_MARKET: Trailing Stop Market Order/ TRIGGER_REVERSE_MARKET:trigger reverse Market order
  "positionSide": "string", // Position direction, required for single position as BOTH, for both long and short positions only LONG or SHORT can be chosen, defaults to LONG if empty
  "reduceOnly": "string", // true, false; Default value is false for single position mode; This parameter is not accepted for both long and short positions mode
  "cumQuote": "string", // transaction amount
  "status": "string", // order status
  "stopPrice": "string", // Trigger price
  "price": "string", // Price
  "origQty": "string", // original order quantity
  "avgPrice": "string", // average transaction price
  "executedQty": "string", // volume
  "orderId": "int64", // Order ID
  "profit": "string", // profit and loss
  "commission": "string", // Fee
  "workingType": "string", // StopPrice trigger price types: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default MARK_PRICE
  "updateTime": "int64", // update time, unit: millisecond
  "postOnly": "bool", // Maker only
  "trailingStopRate": "float64", // Retracement rate
  "stopGuaranteed": "string" // true: Enables the guaranteed stop-loss and take-profit feature; false: Disables the feature. The guaranteed stop-loss feature is not enabled by default. Supported order types include: STOP_MARKET: Market stop-loss order / TAKE_PROFIT_MARKET: Market take-profit order / STOP: Limit stop-loss order / TAKE_PROFIT: Limit take-profit order / TRIGGER_LIMIT: Stop-limit order with trigger / TRIGGER_MARKET: Market order with trigger for stop-loss.
}
{
  "code": 0,
  "msg": "",
  "data": {
    "orders": [
      {
        "symbol": "BTC-USDT",
        "orderId": 1733405587011123500,
        "side": "SELL",
        "positionSide": "LONG",
        "type": "LIMIT",
        "origQty": "0.0030",
        "price": "44459.6",
        "executedQty": "0.0000",
        "avgPrice": "0.0",
        "cumQuote": "0",
        "stopPrice": "",
        "profit": "0.0",
        "commission": "0.0",
        "status": "PENDING",
        "time": 1702256915574,
        "updateTime": 1702256915610,
        "clientOrderId": "",
        "leverage": "",
        "takeProfit": {
          "type": "",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": "",
          "StopGuaranteed": ""
        },
        "stopLoss": {
          "type": "",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": "",
          "StopGuaranteed": ""
        },
        "advanceAttr": 0,
        "positionID": 0,
        "takeProfitEntrustPrice": 0,
        "stopLossEntrustPrice": 0,
        "orderType": "",
        "trailingStopRate": 0,
        "trailingStopDistance": 0,
        "postOnly": false,
        "workingType": "MARK_PRICE"
      },
      {
        "symbol": "BTC-USDT",
        "orderId": 1733405587011123500,
        "side": "SELL",
        "positionSide": "LONG",
        "type": "LIMIT",
        "origQty": "0.0030",
        "price": "44454.6",
        "executedQty": "0.0000",
        "avgPrice": "0.0",
        "cumQuote": "0",
        "stopPrice": "",
        "profit": "0.0",
        "commission": "0.0",
        "status": "PENDING",
        "time": 1702111071719,
        "updateTime": 1702111071735,
        "clientOrderId": "",
        "leverage": "",
        "takeProfit": {
          "type": "",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": "",
          "StopGuaranteed": ""
        },
        "stopLoss": {
          "type": "",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": "",
          "StopGuaranteed": ""
        },
        "advanceAttr": 0,
        "positionID": 0,
        "takeProfitEntrustPrice": 0,
        "stopLossEntrustPrice": 0,
        "orderType": "",
        "trailingStopRate": 0,
        "trailingStopDistance": 0,
        "postOnly": false,
        "workingType": "MARK_PRICE"
      }
    ]
  }
}
```
status
```json
{
  "NEW": "", // New Order
  "PARTIALLY_FILLED": "", // Partial filled
  "FILLED": "", // all filled
  "CANCELED": "" // canceled
}
```

### Sample code
```python
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/openOrders'
    method = "GET"
    paramsMap = {
    "symbol": "BTC-USDT",
    "timestamp": "1702733126509"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())
```


## Query pending order status
Query order details

#### HTTP Request https://open-api.bingx.com
1. Create API KEY
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
    GET /openApi/swap/v2/trade/openOrder

#### rate limitation by UID: 5/s & rate limitation by IP in group Number: 2
__API KEY permission:__ Read
Content-Type: request body (application/json) query string

Request
```json
{
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
  "orderId": "int64", // Order ID
  "clientOrderId": "string", // Customized order ID for users, with a limit of characters from 1 to 40. Different orders cannot use the same clientOrderId
  "timestamp": "int64", // request timestamp in milliseconds
  "recvWindow": "int64" // Request valid time window value, Unit: milliseconds
}
{
  "orderId": "1736012449498123456",
  "symbol": "OP-USDT",
  "timestamp": "1702733255486"
}
```
Response
```json
{
  "time": "int64", // order time, unit: millisecond
  "symbol": "string", // trading pair, for example: BTC-USDT
  "side": "string", // buying and selling direction
  "type": "string", // LIMIT: Limit Order / MARKET: Market Order / STOP_MARKET: Stop Market Order / TAKE_PROFIT_MARKET: Take Profit Market Order / STOP: Stop Limit Order / TAKE_PROFIT: Take Profit Limit Order / TRIGGER_LIMIT: Stop Limit Order with Trigger / TRIGGER_MARKET: Stop Market Order with Trigger / TRAILING_STOP_MARKET: Trailing Stop Market Order
  "positionSide": "string", // Position direction, required for single position as BOTH, for both long and short positions only LONG or SHORT can be chosen, defaults to LONG if empty
  "reduceOnly": "string", // true, false; Default value is false for single position mode; This parameter is not accepted for both long and short positions mode
  "cumQuote": "string", // transaction amount
  "status": "string", // order status
  "stopPrice": "string", // Trigger price
  "price": "string", // Price
  "origQty": "string", // original order quantity
  "avgPrice": "string", // average transaction price
  "executedQty": "string", // volume
  "orderId": "int64", // Order ID
  "profit": "string", // profit and loss
  "commission": "string", // Fee
  "updateTime": "int64", // update time, unit: millisecond
  "workingType": "string", // StopPrice trigger price types: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default MARK_PRICE
  "clientOrderId": "string" // Customized order ID for users
}
{
  "code": 0,
  "msg": "",
  "data": {
    "order": {
      "symbol": "OP-USDT",
      "orderId": 1736012449498123500,
      "side": "SELL",
      "positionSide": "LONG",
      "type": "LIMIT",
      "origQty": "1.0",
      "price": "2.1710",
      "executedQty": "0.0",
      "avgPrice": "0.0000",
      "cumQuote": "0",
      "stopPrice": "",
      "profit": "0.0000",
      "commission": "0.000000",
      "status": "PENDING",
      "time": 1702732596168,
      "updateTime": 1702732596188,
      "clientOrderId": "l*****e",
      "leverage": "",
      "takeProfit": {
        "type": "",
        "quantity": 0,
        "stopPrice": 0,
        "price": 0,
        "workingType": ""
      },
      "stopLoss": {
        "type": "",
        "quantity": 0,
        "stopPrice": 0,
        "price": 0,
        "workingType": ""
      },
      "advanceAttr": 0,
      "positionID": 0,
      "takeProfitEntrustPrice": 0,
      "stopLossEntrustPrice": 0,
      "orderType": "",
      "workingType": "MARK_PRICE"
    }
  }
}
```
status
```json
{
  "NEW": "" // New Order
}
```

### Sample code
```python
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/openOrder'
    method = "GET"
    paramsMap = {
    "orderId": "1736012449498123456",
    "symbol": "OP-USDT",
    "timestamp": "1702733255486"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())
```


## Query Order details
Query order details

#### HTTP Request https://open-api.bingx.com
1. Create API KEY
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
    GET /openApi/swap/v2/trade/order

#### rate limitation by UID: 5/s & rate limitation by IP in group Number: 2
__API KEY permission:__ Read
Content-Type: request body (application/json) query string
  
Request
```json
{
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
  "orderId": "int64", // Order ID
  "clientOrderId": "string", // Customized order ID for users, with a limit of characters from 1 to 40. The system will convert this field to lowercase. Different orders cannot use the same clientOrderId
  "timestamp": "int64", // request timestamp in milliseconds
  "recvWindow": "int64" // Request valid time window value, Unit: milliseconds
}
{
  "orderId": "1736012449498123456",
  "symbol": "OP-USDT",
  "timestamp": "1702733255486"
}
```
Response
```json
{
  "time": "int64", // order time, unit: millisecond
  "symbol": "string", // trading pair, for example: BTC-USDT
  "side": "string", // buying and selling direction
  "type": "string", // LIMIT: Limit Order / MARKET: Market Order / STOP_MARKET: Stop Market Order / TAKE_PROFIT_MARKET: Take Profit Market Order / STOP: Stop Limit Order / TAKE_PROFIT: Take Profit Limit Order / TRIGGER_LIMIT: Stop Limit Order with Trigger / TRIGGER_MARKET: Stop Market Order with Trigger / TRAILING_STOP_MARKET: Trailing Stop Market Order
  "positionSide": "string", // Position direction, required for single position as BOTH, for both long and short positions only LONG or SHORT can be chosen, defaults to LONG if empty
  "reduceOnly": "string", // true, false; Default value is false for single position mode; This parameter is not accepted for both long and short positions mode
  "cumQuote": "string", // transaction amount
  "status": "string", // order status
  "stopPrice": "string", // Trigger price
  "price": "string", // Price
  "origQty": "string", // original order quantity
  "avgPrice": "string", // average transaction price
  "executedQty": "string", // volume
  "orderId": "int64", // Order ID
  "profit": "string", // profit and loss
  "commission": "string", // Fee
  "updateTime": "int64", // update time, unit: millisecond
  "workingType": "string", // StopPrice trigger price types: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default MARK_PRICE
  "clientOrderId": "string", // Customized order ID for users. The system will convert this field to lowercase.
  "stopGuaranteed": "string", // true: Enables the guaranteed stop-loss and take-profit feature; false: Disables the feature. The guaranteed stop-loss feature is not enabled by default. Supported order types include: STOP_MARKET: Market stop-loss order / TAKE_PROFIT_MARKET: Market take-profit order / STOP: Limit stop-loss order / TAKE_PROFIT: Limit take-profit order / TRIGGER_LIMIT: Stop-limit order with trigger / TRIGGER_MARKET: Market order with trigger for stop-loss.
  "triggerOrderId": "int64" // trigger order ID associated with this order
}
{
  "code": 0,
  "msg": "",
  "data": {
    "order": {
      "symbol": "OP-USDT",
      "orderId": 1736012449498123500,
      "side": "SELL",
      "positionSide": "LONG",
      "type": "LIMIT",
      "origQty": "1.0",
      "price": "2.1710",
      "executedQty": "0.0",
      "avgPrice": "0.0000",
      "cumQuote": "0",
      "stopPrice": "",
      "profit": "0.0000",
      "commission": "0.000000",
      "status": "PENDING",
      "time": 1702732596168,
      "updateTime": 1702732596188,
      "clientOrderId": "l*****e",
      "leverage": "",
      "takeProfit": {
        "type": "",
        "quantity": 0,
        "stopPrice": 0,
        "price": 0,
        "workingType": ""
      },
      "stopLoss": {
        "type": "",
        "quantity": 0,
        "stopPrice": 0,
        "price": 0,
        "workingType": ""
      },
      "advanceAttr": 0,
      "positionID": 0,
      "takeProfitEntrustPrice": 0,
      "stopLossEntrustPrice": 0,
      "orderType": "",
      "workingType": "MARK_PRICE",
      "stopGuaranteed": false,
      "triggerOrderId": 1736012449498123500
    }
  }
}
```
status
```json
{
  "NEW": "", // New Order
  "PARTIALLY_FILLED": "", // Partial filled
  "FILLED": "", // all filled
  "CANCELED": "" // canceled
}
```

Sample code
```python
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/order'
    method = "GET"
    paramsMap = {
    "orderId": "1736012449498123456",
    "symbol": "OP-USDT",
    "timestamp": "1702733255486"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())
```


## Query Margin Type
Query the user's margin mode on the specified symbol contract: isolated or cross.

#### HTTP Request https://open-api.bingx.com
1. Create API KEY
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
    GET /openApi/swap/v2/trade/marginType

#### rate limitation by UID: 2/s & rate limitation by IP in group Number: 2
__API KEY permission:__ Read
Content-Type: request body (application/json) query string
  
Request
```json
{
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
  "timestamp": "int64", // request timestamp in milliseconds
  "recvWindow": "int64" // Request valid time window value, Unit: milliseconds
}
{
  "symbol": "WOO-USDT",
  "timestamp": "1702733469134"
}
```
Response
```json
{
  "marginType": "string" // margin mode
}
{
  "code": 0,
  "msg": "",
  "data": {
    "marginType": "CROSSED"
  }
}
```
Status
```json
{
  "ISOLATED": "", // Isolated Margin
  "CROSSED": "" // Full position
}
```

### Sample code
```python
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/marginType'
    method = "GET"
    paramsMap = {
    "symbol": "WOO-USDT",
    "timestamp": "1702733469134"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())
```


## Change Margin Type
Change the user's margin mode on the specified symbol contract: isolated margin or cross margin.

#### HTTP Request https://open-api.bingx.com
1. Create API KEY
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
    POST /openApi/swap/v2/trade/marginType

#### rate limitation by UID: 2/s & rate limitation by IP in group Number: 2
API KEY permission: Perpetual Futures Trading
Content-Type: request body (application/json) query string

Request
```json
{
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
  "timestamp": "int64", // request timestamp in milliseconds
  "marginType": "string", // Margin mode ISOLATED (isolated margin), CROSSED (cross margin)
  "recvWindow": "int64" // Request valid time window value, Unit: milliseconds
}
{
  "symbol": "MINA-USDT",
  "marginType": "CROSSED",
  "recvWindow": "60000",
  "timestamp": "1702733445917"
}
```
Response
```json
{
  "code": "int64", // error code, 0 means successfully response, others means response failure
  "msg": "string" // Error Details Description
}
{
  "code": 0,
  "msg": ""
}
```
marginType
```json
{
  "ISOLATED": "", // Isolated Margin
  "CROSSED": "" // Full position
}
```

### Sample code
```python
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/marginType'
    method = "POST"
    paramsMap = {
    "symbol": "MINA-USDT",
    "marginType": "CROSSED",
    "recvWindow": "60000",
    "timestamp": "1702733445917"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())
```


## Query Leverage
Query the opening leverage of the user in the specified symbol contract.

#### HTTP Request https://open-api.bingx.com
1. Create API KEY
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
    GET /openApi/swap/v2/trade/leverage

#### rate limitation by UID: 5/s & rate limitation by IP in group Number: 2
__API KEY permission:__ Read
Content-Type: request body (application/json) query string

Request
```json
{
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
  "timestamp": "int64", // request timestamp in milliseconds
  "recvWindow": "int64" // Request valid time window value, Unit: milliseconds
}
{
  "symbol": "BCH-USDT",
  "timestamp": "1702733572940"
}
```
Response
```json
{
  "longLeverage": "int64", // Long position leverage
  "shortLeverage": "int64", // Short position Leverage
  "maxLongLeverage": "int64", // Max Long position leverage
  "maxShortLeverage": "int64", // Max Short position Leverage
  "availableLongVol": "string", // Available Long Volume
  "availableShortVol": "string", // Available Short Volume
  "availableLongVal": "string", // Available Long Value
  "availableShortVal": "string", // Available Short Value
  "maxPositionLongVal": "string", // Maximum Position Long Value
  "maxPositionShortVal": "string" // Maximum Position Short Value
}
{
  "code": 0,
  "msg": "",
  "data": {
    "longLeverage": 50,
    "shortLeverage": 50,
    "maxLongLeverage": 75,
    "maxShortLeverage": 75
  }
}
```

### Sample code
```python
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/leverage'
    method = "GET"
    paramsMap = {
    "symbol": "BCH-USDT",
    "timestamp": "1702733572940"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())
```


## Set Leverage
Adjust the user's opening leverage in the specified symbol contract.

#### HTTP Request https://open-api.bingx.com
1. Create API KEY
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
    POST /openApi/swap/v2/trade/leverage

#### rate limitation by UID: 2/s & rate limitation by IP in group Number: 2
__API KEY permission:__ Perpetual Futures Trading
Content-Type: request body (application/json) query string
  
Request
```json
{
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
  "side": "string", // Leverage for long or short positions. In the Hedge mode, LONG for long positions, SHORT for short positions. In the One-way mode, only supports BOTH.
  "timestamp": "int64", // request timestamp in milliseconds
  "leverage": "int64", // leverage
  "recvWindow": "int64" // Request valid time window value, Unit: milliseconds
}
{
  "leverage": "8",
  "side": "SHORT",
  "symbol": "ETH-USDT",
  "timestamp": "1702733704941"
}
```
Response
```json
{
  "leverage": "int64", // leverage
  "symbol": "string", // trading pair
  "availableLongVol": "string", // Available Long Volume
  "availableShortVol": "string", // Available Short Volume
  "availableLongVal": "string", // Available Long Value
  "availableShortVal": "string", // Available Short Value
  "maxPositionLongVal": "string", // Maximum Position Long Value
  "maxPositionShortVal": "string" // Maximum Position Short Value
}
{
  "code": 0,
  "msg": "",
  "data": {
    "leverage": 8,
    "symbol": "ETH-USDT"
  }
}
```

### Sample code
```python
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/leverage'
    method = "POST"
    paramsMap = {
    "leverage": "8",
    "side": "SHORT",
    "symbol": "ETH-USDT",
    "timestamp": "1702733704941"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())
```


## User's Force Orders
Query the user's forced liquidation order.

### HTTP Request https://open-api.bingx.com
* If "autoCloseType" is not passed, both forced liquidation orders and ADL liquidation orders will be returned
* If "startTime" is not passed, only the data within 7 days before "endTime" will be returned
1. Create API KEY
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
    GET /openApi/swap/v2/trade/forceOrders

#### rate limitation by UID: 10/s & rate limitation by IP in group Number: 
__API KEY permission:__ Perpetual Futures Trading
Content-Type: request body (application/json) query string

Request
```json
{
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
  "autoCloseType": "string", // "LIQUIDATION":liquidation order, "ADL":ADL liquidation order
  "startTime": "int64", // Start time, unit: millisecond
  "endTime": "int64", // End time, unit: millisecond
  "limit": "int", // The number of returned result sets The default value is 50, the maximum value is 100
  "timestamp": "int64", // request timestamp in milliseconds
  "recvWindow": "int64" // Request valid time window value, Unit: milliseconds
}
{
  "symbol": "ATOM-USDT",
  "startTime": "1696291200",
  "timestamp": "1699982303257"
}
```
Response
```json
{
  "time": "int64", // order time, unit: millisecond
  "symbol": "string", // trading pair, for example: BTC-USDT
  "side": "string", // buying and selling direction
  "type": "string", // LIMIT: Limit Order / MARKET: Market Order / STOP_MARKET: Stop Market Order / TAKE_PROFIT_MARKET: Take Profit Market Order / STOP: Stop Limit Order / TAKE_PROFIT: Take Profit Limit Order / TRIGGER_LIMIT: Stop Limit Order with Trigger / TRIGGER_MARKET: Stop Market Order with Trigger / TRAILING_STOP_MARKET: Trailing Stop Market Order
  "positionSide": "string", // Position direction, required for single position as BOTH, for both long and short positions only LONG or SHORT can be chosen, defaults to LONG if empty
  "reduceOnly": "string", // true, false; Default value is false for single position mode; This parameter is not accepted for both long and short positions mode
  "cumQuote": "string", // transaction amount
  "status": "string", // order status
  "stopPrice": "string", // Trigger price
  "price": "string", // Price
  "origQty": "string", // original order quantity
  "avgPrice": "string", // average transaction price
  "executedQty": "string", // volume
  "orderId": "int64", // Order ID
  "profit": "string", // profit and loss
  "commission": "string", // Fee
  "workingType": "string", // StopPrice trigger price types: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default MARK_PRICE
  "updateTime": "int64", // update time, unit: millisecond
  "stopGuaranteed": "string" // true: Enables the guaranteed stop-loss and take-profit feature; false: Disables the feature. The guaranteed stop-loss feature is not enabled by default. Supported order types include: STOP_MARKET: Market stop-loss order / TAKE_PROFIT_MARKET: Market take-profit order / STOP: Limit stop-loss order / TAKE_PROFIT: Limit take-profit order / TRIGGER_LIMIT: Stop-limit order with trigger / TRIGGER_MARKET: Market order with trigger for stop-loss.
}
{
  "code": 0,
  "msg": "",
  "data": {
    "orders": [
      {
        "symbol": "ATOM-USDT",
        "orderId": 172264854643022330000,
        "side": "SELL",
        "positionSide": "LONG",
        "type": "LIMIT",
        "origQty": "2.36",
        "price": "8.096",
        "executedQty": "2.36",
        "avgPrice": "8.095",
        "cumQuote": "19",
        "stopPrice": "",
        "profit": "-0.9346",
        "commission": "-0.009553",
        "status": "FILLED",
        "time": 1699546393000,
        "updateTime": 1699546393000,
        "clientOrderId": "",
        "leverage": "21X",
        "takeProfit": {
          "type": "",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": ""
        },
        "stopLoss": {
          "type": "",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": ""
        },
        "advanceAttr": 0,
        "positionID": 0,
        "takeProfitEntrustPrice": 0,
        "stopLossEntrustPrice": 0,
        "orderType": "",
        "workingType": "MARK_PRICE"
      }
    ]
  }
}
```

### Sample code
```python
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/forceOrders'
    method = "GET"
    paramsMap = {
    "symbol": "ATOM-USDT",
    "startTime": "1696291200",
    "timestamp": "1699982303257"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())
```


## Query Order history
Query the user's historical orders (order status is completed or canceled).

#### HTTP Request https://open-api.bingx.com
The maximum query time range shall not exceed 7 days
Query data within the last 7 days by default
1. Create API KEY
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
    GET /openApi/swap/v2/trade/allOrders

#### rate limitation by UID: 5/s & rate limitation by IP in group Number: 3
__API KEY permission:__ Perpetual Futures Trading
Content-Type: request body (application/json) query string
  
Request
```json
{
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT.If no symbol is specified, it will query the historical orders for all trading pairs.
  "orderId": "int64", // Only return subsequent orders, and return the latest order by default
  "startTime": "int64", // Start time, unit: millisecond
  "endTime": "int64", // End time, unit: millisecond
  "limit": "int", // number of result sets to return Default: 500 Maximum: 1000
  "timestamp": "int64", // request timestamp in milliseconds
  "recvWindow": "int64" // Request valid time window value, Unit: milliseconds
}
{
  "endTime": "1702731995000",
  "limit": "500",
  "startTime": "1702688795000",
  "symbol": "PYTH-USDT",
  "timestamp": "1702731995838"
}
```
Response
```json
{
  "time": "int64", // order time, unit: millisecond
  "symbol": "string", // trading pair, for example: BTC-USDT.If a specific pair is not provided, a history of transactions for all pairs will be returned
  "side": "string", // buying and selling direction
  "type": "string", // LIMIT: Limit Order / MARKET: Market Order / STOP_MARKET: Stop Market Order / TAKE_PROFIT_MARKET: Take Profit Market Order / STOP: Stop Limit Order / TAKE_PROFIT: Take Profit Limit Order / TRIGGER_LIMIT: Stop Limit Order with Trigger / TRIGGER_MARKET: Stop Market Order with Trigger / TRAILING_STOP_MARKET: Trailing Stop Market Order
  "positionSide": "string", // Position direction, required for single position as BOTH, for both long and short positions only LONG or SHORT can be chosen, defaults to LONG if empty
  "reduceOnly": "string", // true, false; Default value is false for single position mode; This parameter is not accepted for both long and short positions mode
  "cumQuote": "string", // transaction amount
  "status": "string", // order status
  "stopPrice": "string", // Trigger price
  "price": "string", // Price
  "origQty": "string", // original order quantity
  "avgPrice": "string", // average transaction price
  "executedQty": "string", // volume
  "orderId": "int64", // Order ID
  "profit": "string", // profit and loss
  "commission": "string", // Fee
  "workingType": "string", // StopPrice trigger price types: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default MARK_PRICE
  "updateTime": "int64", // update time, unit: millisecond
  "stopGuaranteed": "string", // true: Enables the guaranteed stop-loss and take-profit feature; false: Disables the feature. The guaranteed stop-loss feature is not enabled by default. Supported order types include: STOP_MARKET: Market stop-loss order / TAKE_PROFIT_MARKET: Market take-profit order / STOP: Limit stop-loss order / TAKE_PROFIT: Limit take-profit order / TRIGGER_LIMIT: Stop-limit order with trigger / TRIGGER_MARKET: Market order with trigger for stop-loss.
  "triggerOrderId": "int64" // trigger order ID associated with this order
}
{
  "code": 0,
  "msg": "",
  "data": {
    "orders": [
      {
        "symbol": "PYTH-USDT",
        "orderId": 1736007506620112100,
        "side": "SELL",
        "positionSide": "SHORT",
        "type": "LIMIT",
        "origQty": "33",
        "price": "0.3916",
        "executedQty": "33",
        "avgPrice": "0.3916",
        "cumQuote": "13",
        "stopPrice": "",
        "profit": "0.0000",
        "commission": "-0.002585",
        "status": "FILLED",
        "time": 1702731418000,
        "updateTime": 1702731470000,
        "clientOrderId": "",
        "leverage": "15X",
        "takeProfit": {
          "type": "TAKE_PROFIT",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": ""
        },
        "stopLoss": {
          "type": "STOP",
          "quantity": 0,
          "stopPrice": 0,
          "price": 0,
          "workingType": ""
        },
        "advanceAttr": 0,
        "positionID": 0,
        "takeProfitEntrustPrice": 0,
        "stopLossEntrustPrice": 0,
        "orderType": "",
        "workingType": "MARK_PRICE",
        "stopGuaranteed": false,
        "triggerOrderId": 1736012449498123500
      }
    ]
  }
}
```

### Sample code
```python

import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/allOrders'
    method = "GET"
    paramsMap = {
    "endTime": "1702731995000",
    "limit": "500",
    "startTime": "1702688795000",
    "symbol": "PYTH-USDT",
    "timestamp": "1702731995838"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())

```


## Modify Isolated Position Margin
Adjust the isolated margin funds for the positions in the isolated position mode.

#### HTTP Request https://open-api.bingx.com
1. Create API KEY
2. Configure API KEY permissions
3. Understanding signature authentication
4. Run the following example code  
5. Understand common error codes
6. Understand rate limitations
7. Understanding request timestamps
8. Understand fee schedule

#### request parameters
    POST /openApi/swap/v2/trade/positionMargin

#### rate limitation by UID: 2/s & rate limitation by IP in group Number: 2
__API KEY permission:__ Perpetual Futures Trading
Content-Type: request body (application/json) query string
  
Request
```json
{
  "symbol": "string", // There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
  "amount": "float64", // margin funds
  "type": "int", // adjustment direction 1: increase isolated margin, 2: decrease isolated margin
  "positionSide": "string", // Position direction, and only LONG or SHORT can be selected
  "timestamp": "int64", // request timestamp in milliseconds
  "recvWindow": "int64" // Request valid time window value, Unit: milliseconds
}
{
  "recvWindow": "10000",
  "symbol": "BTC-USDT",
  "type": "1",
  "amount": "3",
  "positionSide": "LONG",
  "timestamp": "1702718148654"
}
```
Response
```json
{
  "code": "int64", // error code, 0 means successfully response, others means response failure
  "msg": "string", // Error Details Description
  "amount": "float64", // margin funds
  "type": "int" // adjustment direction 1: increase isolated margin, 2: decrease isolated margin
}
{
  "code": 0,
  "msg": "",
  "amount": 3,
  "type": 1
}
```

### Sample code
```python
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = ""
SECRETKEY = ""

def demo():
    payload = {}
    path = '/openApi/swap/v2/trade/positionMargin'
    method = "POST"
    paramsMap = {
    "recvWindow": "10000",
    "symbol": "BTC-USDT",
    "type": "1",
    "amount": "3",
    "positionSide": "LONG",
    "timestamp": "1702718148654"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    print("demo:", demo())
```
