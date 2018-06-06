from data_processing import format_data_COINMARKETCAP, format_data_TABLE

def lambda_handler(event, context):
    list = format_data_COINMARKETCAP('https://api.coinmarketcap.com/v2/ticker/?sort=rank')
    formatted_list = format_data_TABLE(list)
    return formatted_list