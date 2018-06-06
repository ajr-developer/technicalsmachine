# modules
import time
import pandas as pd
from datetime import datetime

# files
from binance.client import Client
import technical_indicators as indicators
import data_processing as data_processing

class CryptoBot():

    def __init__(self, api_key, api_secret, ):
        """ Crypto_bot constructor

        :param api_key: Api Key used to initialize Binance Client
        :type api_key: str.
        :param api_secret: Api Secret used to initialize Binance Client
        :type api_secret: str.
        
        """
        ### ALLOWED STRATEGIES ###
        TRADING_STRATEGY_BB_RSI = 'bb_rsi_strategy'
        ### ALLOWED SYMBOLS ###
        SYMBOL_IOTABTC = "IOTABTC"

        self.candles_df = None
        self.strategy = None

        # initialize Binance client
        self.client = Client(api_key, api_secret)

    def start(self, strategy, symbol):
        """ Starts the bot — instance begins monitoring and trading

        :param strategy: Trading strategy to follow
        :type symbol: str. (use CryptoBot.TRADING_STRATEGY_BB_RSI)
        :param symbol: indicates which trading pair to monitor
        :type symbol: str. (use CryptoBot.SYMBOL_IOTABTC)
        """
        list = data_processing.format_data_COINMARKETCAP('https://api.coinmarketcap.com/v2/ticker/?sort=rank')
        formatted_list = data_processing.format_data_TABLE(list)

        for item in formatted_list:
            name = item[1] + "BTC"
            print(name)
            try:
                # pull in data from Binance
                self.update_candles(name, Client.KLINE_INTERVAL_15MINUTE)
                current_price = self.get_price(name)
                if self.strategy_result_BUY(current_price, symbol):
                    trade = Trade(name, current_price, strategy, 0.01)
                    print("BUY" + trade.__str__())
            except:
                print("naw dawg")
                


    def update_candles(self, symbol, interval):
        """ Pulls in candle information from Binance and update candle_df instance variable 

        :param symbol: Trading pair symbol (ex. IOTABTC)
        :type symbol: str.
        :param interval: Candle intervals 
        :type interval: str. (use Client.KLINE_INTERVAL_*)
        
        """
        # Pull in candle information
        candles = self.client.get_klines(symbol=symbol, interval=interval, limit=50)

        #create dataframe for candles
        candles_df = pd.DataFrame(data=candles, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', \
            'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', \
            'Can be ignored'])
       
        self.candles_df = candles_df

    def get_price(self, symbol):
        """ Gets current price for given symbol

        :param symbol: Trading pair symbol (ex. IOTABTC)
        :type symbol: str.
        
        """
        price = self.client.get_symbol_ticker(symbol=symbol)
        return float(price["price"])
       
    def strategy_result_BUY(self, price, symbol):
        """ Checks whether strategy indicates to buy at current price  
        :param price: Current price of a currency
        :type symbol: str.
        :param interval: Candle intervals 
        :type interval: str. (use Client.KLINE_INTERVAL_*)

        :returns: True if strategy indicates to buy at current price
        :type returns: boolean
        
        """
        candles_df = self.candles_df
        candles_df['Close'] = candles_df['Close'].astype('float64') 
        candles_df = indicators.bollinger_bands(candles_df, 20)
        current_candle = candles_df.index[-1]
        last_candle = candles_df.loc[current_candle]

        lowerBB = last_candle["lowerBB"]


        threshhold = price * 0.005

        # If price is within 0.5% of lower BB, signal to buy 
        if price <= lowerBB + threshhold:
            return True

        else:
            return False


    def strategy_result_SELL(self, price, symbol):
        """ Checks whether strategy indicates to sell at current price  
        :param price: Current price of a currency
        :type symbol: str.
        :param interval: Candle intervals 
        :type interval: str. (use Client.KLINE_INTERVAL_*)

        :returns: True if strategy indicates to buy at current price
        :type returns: boolean
        
        """
        candles_df = self.candles_df
        candles_df['Close'] = candles_df['Close'].astype('float64') 
        candles_df = indicators.bollinger_bands(candles_df, 20)
        current_candle = candles_df.index[-1]
        last_candle = candles_df.loc[current_candle]

        upperBB = last_candle["upperBB"]

        current_price = self.get_price(symbol)
        threshhold = current_price * 0.01

        # If price is within 0.5% of upper BB, signal to sell
        if current_price >= upperBB - threshhold:
            return True

        else:
            return False


class Trade():

    def __init__(self, symbol, price, strategy, stop_loss):
        """ Trade object constructor

        :param api_key: Api Key used to initialize Binance Client
        :type api_key: str.
        :param api_secret: Api Secret used to initialize Binance Client
        :type api_secret: str.
        
        """

        self.symbol = symbol
        self.price = price
        self.time = datetime.now().time()
        self.strategy = strategy
        self.stop_loss = price - (price * stop_loss)
        self.state_ACTIVE = True  # Activate trade

    def __str__(self):
        return self.symbol 


