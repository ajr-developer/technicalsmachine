# data.py
# Contains logic to retrieve and format data for consumption by DataTables 

import RestfulClient
from binance.client import Client

COINMARKETCAP_API_URL = 'https://api.coinmarketcap.com/'
COINMARKETCAP_API_VERSION = 'v2'


def get_data_COINMARKETCAP(apiURL):
    """ Pulls in the top 100 cryptos from CoinMarketCap and formats for use in table

    :param apiURL: URL for CoinMarketCap's current API
    :type apiURL: str.

    :returns: Formatted list of top 100 cryptos on CoinMarketCap
    :type returns: list of JSON

    table_data = [
        {   
            'name': str,
            'symbol': str,
            'rank': str,
            'price': str,
            'market_cap': str
        },
        ...
    ]

    """
    # pull in and preliminarily data from API
    apiURL = apiURL
    exchangeData = RestfulClient.get(apiURL)['data']
    
    # store pertinent API data as array of JSON objects 
    formatted_exchange_data = []
    for key in exchangeData:
        name = exchangeData[key]['name']
        symbol = exchangeData[key]['symbol']
        rank = exchangeData[key]['rank']
        price = exchangeData[key]['quotes']['USD']['price']
        market_cap = exchangeData[key]['quotes']['USD']['market_cap']
        current_crypto = {
            'name': name,
            'symbol': symbol,
            'rank': rank,
            'price': price,
            'market_cap': market_cap
        }
        formatted_exchange_data.append(current_crypto)

    return formatted_exchange_data

def format_data_COINMARKETCAP(exchange_data, strategy):

    table_data = []
    for coin_entry in exchange_data:
        formatted_coin = []
        formatted_coin.append(str(coin_entry['rank']))
        formatted_coin.append(str(coin_entry['name']))
        formatted_coin.append(str(coin_entry['symbol']))
        formatted_coin.append(str(coin_entry['market_cap'])) 
        formatted_coin.append(str(coin_entry['price']))
        table_data.append(formatted_coin)
    
    return table_data

