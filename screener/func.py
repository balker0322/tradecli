from binance.client import Client
# import ta
import pandas as pd
# from src import conf
from src.config import config

api_key = config['binance_keys']['binanceaccount1']['API_KEY']
api_secret = config['binance_keys']['binanceaccount1']['SECRET_KEY']
client = Client(api_key, api_secret)
unit = dict()
unit['m'] = 'min'
unit['h'] = 'hour'
unit['d'] = 'day'
unit['w'] = 'week'
unit['M'] = 'month'

def historical_klines(pair, interval, num_period):
    interval_num = int(interval[:-1])
    interval_unit = interval[-1]
    history = "{} {} ago UTC".format(interval_num*num_period, unit[interval_unit])

    return client.get_historical_klines(pair, interval, history)

def get_all_pairs():
    '''
    Get all USDT pairs
    '''
    exchange_info = client.get_exchange_info()
    return [symbol_info['symbol'] for symbol_info in exchange_info['symbols'] if symbol_info['symbol'][-4:]=='USDT']


if __name__ == '__main__':
    print('hello')