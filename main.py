import json
from usdt_m_perp_futures.trades_endpoints import TradesEndpoints

orders = []

if __name__ == "__main__":
    t = TradesEndpoints()
    response = t.test_order()
    # batchOrders = []
    # batchOrders.append(t.gen_params_map("BUY", 0.01, False, False, "MARKET", "LONG", "BTC-USDT"))
    # batchOrders.append(t.gen_params_map("SELL", 0.01, False, False, "MARKET", "SHORT", "BTC-USDT"))
    # response = t.place_multiple_orders(json.dumps(batchOrders))
    
    # position = data[0]
    # position_id = position['positionId']
    # close(position_id)
    # print(response)
