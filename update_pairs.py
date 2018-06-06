# update_pairs.py
# Processes exchange data from Binance to provide a list of all their available trading pairs.
# Consumed by Select2 in order to allow users to search for their desired currency pair.
# Cryptocurrency dictionary allows users to search by individual symbols, or full name.
# Ex) ETHBTC, ETH, BTC, Ethereum, or Bitcoin would all bring up ETHBTC.

import json
from binance.client import Client

with open('cryptocurrencies.json') as f:
    cryptocurrency_symbol_dict = json.load(f)


def update_pairs_BINANCE():
    # get symbol data from client
    client = Client("", "")
    exchange_data = client.get_exchange_info()
    trading_pairs_data = exchange_data['symbols']

    # clean up symbol data to only include trading pair and asset symbols
    processed_trading_pairs = []
    for pair in trading_pairs_data:
        # get full names from imported crypto name dictionary
        base_asset_name = cryptocurrency_symbol_dict[pair['baseAsset']]
        quote_asset_name = cryptocurrency_symbol_dict[pair['quoteAsset']]
        trading_pair_name = base_asset_name + "/" + quote_asset_name

        trading_pair = {
            'trading_pair': {
                'symbol': pair['symbol'],
                'name': trading_pair_name
            },
            'base_asset': {
                'symbol': pair['baseAsset'],
                'name': base_asset_name
            },
            'quote_asset': {
                'symbol': pair['quoteAsset'],
                'name': quote_asset_name
            }
        }
        processed_trading_pairs.append(trading_pair)

    print(processed_trading_pairs)
