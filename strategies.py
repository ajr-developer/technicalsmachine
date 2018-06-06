# strategies.py
# Contains all logic required to apply technical trading strategies to trading pairs.

import time
import pandas as pd
from datetime import datetime

from binance.client import Client
import technical_indicators as indicators


# INTERACTION WITH BINANCE API 

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

def get_price(binance_client, symbol):
    """ Gets current price for given symbol

    :param symbol: Trading pair symbol (ex. IOTABTC)
    :type symbol: str.

    :returns: Current price for given symbol
    :type returns: String

    """
    price = binance_client.get_symbol_ticker(symbol=symbol)
    return float(price['price'])


# TRADING STRATEGY IMPLEMENTATIONS 

def bb_strategy(binance_client, symbol, interval):
    """ Applies basic Bollinger Bands strategy to provided symbol and interval

    :param symbol: Trading pair symbol (ex. IOTABTC)
    :type symbol: str.
    :param interval: Candle intervals 
    :type interval: str. (use Client.KLINE_INTERVAL_*)

    :returns: "BUY", "SELL", or "NEUTRAL" based on results of strategy
    :type returns: str.
    
    """
    # setup Bollinger Bands DataFrame
    candles_df = get_candles(binance_client, symbol, interval)
    candles_df['Close'] = candles_df['Close'].astype('float64') 
    candles_df = indicators.bollinger_bands(candles_df, 12)

    # setup data from most recent candle required for application of trading strategy
    current_price = get_price(binance_client, symbol)
    current_candle = candles_df.loc[candles_df.index[-1]]
    lower_bb = current_candle['lower_bb']
    upper_bb = current_candle['upper_bb']

    # apply trading strategy
    threshhold = current_price * 0.0025
    
    if current_price <= lower_bb + threshhold:
        return "BUY"
    elif current_price >= upper_bb - threshhold:
        return "SELL"
    else:
        return "NEUTRAL"






