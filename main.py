import requests
from collections import defaultdict

res = requests.get(f"https://esi.evetech.net/dev/markets/10000002/orders/?datasource=tranquility&order_type=all&page=1")

order_ranks = defaultdict(list)
volume_lookup = {}

for order in res.json():
    if order is None:
        continue
    order_ranks[order['type_id']].append(order['price'])
    volume_lookup[order['type_id']] = order['volume_remain']

rank = []

for k, v in order_ranks.items():
    v = sorted(v)
    spread = v[-1] - v[0]
    if (spread == 0):
        continue
    print(f"ITEM ID: {k}, SPREAD: {spread:.2f} ISK, VOLUME: {volume_lookup[k]}")

    rank.append([spread * volume_lookup[k], k])

for item in sorted(rank, key=lambda x: -x[0]):
    print(f"{item[1]} with score {item[0]:.2f}")

