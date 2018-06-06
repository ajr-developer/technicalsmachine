# strategies.py
# Contains logic for all trading strategies 

import time
import pandas as pd
from datetime import datetime

from binance.client import Client
import technical_indicators as indicators

def get_candles(binance_client, symbol, interval):
    """ Pulls in candle information from Binance

    :param symbol: Trading pair symbol (ex. IOTABTC)
    :type symbol: str.
    :param interval: Candle intervals 
    :type interval: str. (use Client.KLINE_INTERVAL_*)

    :returns: Candle information retrieved from Binance 
    :type returns: DataFrame
    
    """
    candles = binance_client.get_klines(symbol=symbol, interval=interval, limit=50)
    candles_df = pd.DataFrame(data=candles, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', \
        'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', \
        'Can be ignored'])
    
    return candles_df

def get_price(self, symbol):
    """ Gets current price for given symbol

    :param symbol: Trading pair symbol (ex. IOTABTC)
    :type symbol: str.
    
    """
    price = self.client.get_symbol_ticker(symbol=symbol)
    return float(price["price"])

