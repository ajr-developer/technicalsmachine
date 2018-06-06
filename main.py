import strategies
from binance.client import Client

client = Client("", "")
candles = strategies.get_candles(client, "IOTABTC", Client.KLINE_INTERVAL_15MINUTE)
print(candles)
