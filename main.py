import requests
from collections import defaultdict

"""
{'duration': 90, 'is_buy_order': False, 'issued': '2025-02-27T02:42:57Z', 'location_id': 60010336, 'min_volume': 1, 'order_id': 6996368580, 'price': 2299000.0, 'range': 'region', 'system_id': 30005312, 'type_id': 46998, 'volume_remain': 1, 'volume_total': 1}
"""


max_buy= {}
min_sell = {}
volume_lookup = {}

for i in range(1, 101):
    res = requests.get(f"https://esi.evetech.net/dev/markets/10000002/orders/?datasource=tranquility&order_type=all&page={i}")
    for order in res.json():
        iid = order['type_id']
        if order['is_buy_order']:
            if iid in max_buy:
                max_buy[iid] = max(max_buy[iid], order['price'])
            else:
                max_buy[iid] = order['price']
        else:
            if iid in min_sell:
                min_sell[iid] = min(min_sell[iid], order['price'])
            else:
                min_sell[iid] = order['price']
        volume_lookup[iid] = order['volume_remain']

"""
Must be a seller
"""
rank = []

for item_id, sell_price in min_sell.items():
    spread = 0.0
    if item_id in max_buy:
        spread = max_buy - sell_price
        print(spread)
    else:
        continue
    if spread <= 0.0:
        continue
    rank.append([volume_lookup[item_id] * spread, item_id])

print(rank)

for item in sorted(rank, key=lambda x: -x[0]):
    print(f"{item[1]} with score {item[0]:.2f}")

