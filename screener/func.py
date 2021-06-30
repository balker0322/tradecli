from binance.client import Client
import ta
import pandas as pd
from src.config import config
from tqdm import tqdm

api_key = config['binance_keys']['binanceaccount1']['API_KEY']
api_secret = config['binance_keys']['binanceaccount1']['SECRET_KEY']
client = Client(api_key, api_secret)
unit = dict()
unit['m'] = 'min'
unit['h'] = 'hour'
unit['d'] = 'day'
unit['w'] = 'week'
unit['M'] = 'month'
PAIRS = ['BTCUSDT',
 'ETHUSDT',
 'BCHUSDT',
 'XRPUSDT',
 'EOSUSDT',
 'LTCUSDT',
 'TRXUSDT',
 'ETCUSDT',
 'LINKUSDT',
 'XLMUSDT',
 'ADAUSDT',
 'XMRUSDT',
 'DASHUSDT',
 'ZECUSDT',
 'XTZUSDT',
 'BNBUSDT',
 'ATOMUSDT',
 'ONTUSDT',
 'IOTAUSDT',
 'BATUSDT',
 'VETUSDT',
 'NEOUSDT',
 'QTUMUSDT',
 'IOSTUSDT',
 'THETAUSDT',
 'ALGOUSDT',
 'ZILUSDT',
 'KNCUSDT',
 'ZRXUSDT',
 'COMPUSDT',
 'OMGUSDT',
 'DOGEUSDT',
 'SXPUSDT',
 'KAVAUSDT',
 'BANDUSDT',
 'RLCUSDT',
 'WAVESUSDT',
 'MKRUSDT',
 'SNXUSDT',
 'DOTUSDT',
 'DEFIUSDT',
 'YFIUSDT',
 'BALUSDT',
 'CRVUSDT',
 'TRBUSDT',
 'YFIIUSDT',
 'RUNEUSDT',
 'SUSHIUSDT',
 'SRMUSDT',
 'BZRXUSDT',
 'EGLDUSDT',
 'SOLUSDT',
 'ICXUSDT',
 'STORJUSDT',
 'BLZUSDT',
 'UNIUSDT',
 'AVAXUSDT',
 'FTMUSDT',
 'HNTUSDT',
 'ENJUSDT',
 'FLMUSDT',
 'TOMOUSDT',
 'RENUSDT',
 'KSMUSDT',
 'NEARUSDT',
 'AAVEUSDT',
 'FILUSDT',
 'RSRUSDT',
 'LRCUSDT',
 'MATICUSDT',
 'OCEANUSDT',
 'CVCUSDT',
 'BELUSDT',
 'CTKUSDT',
 'AXSUSDT',
 'ALPHAUSDT',
 'ZENUSDT',
 'SKLUSDT',
 'GRTUSDT',
 '1INCHUSDT',
 'AKROUSDT',
 'CHZUSDT',
 'SANDUSDT',
 'ANKRUSDT',
 'LUNAUSDT',
 'BTSUSDT',
 'LITUSDT',
 'UNFIUSDT',
 'DODOUSDT',
 'REEFUSDT',
 'RVNUSDT',
 'SFPUSDT',
 'XEMUSDT',
 'COTIUSDT',
 'CHRUSDT',
 'MANAUSDT',
 'ALICEUSDT',
 'HBARUSDT',
 'ONEUSDT',
 'LINAUSDT',
 'STMXUSDT',
 'DENTUSDT',
 'CELRUSDT',
 'HOTUSDT',
 'MTLUSDT',
 'OGNUSDT',
 'BTTUSDT',
 'NKNUSDT',
 'SCUSDT',
 'DGBUSDT',
 '1000SHIBUSDT',
 'ICPUSDT',
 'BAKEUSDT',
 'GTCUSDT',
 'BTCDOMUSDT',
 'KEEPUSDT']
INDICATORS = [
    'rsi_1m',
    'rsi_5m',
    'rsi_15m',
    'rsi_30m',
    'rsi_1h',
    'rsi_1d',
]
NUMPERIOD = 14

def historical_klines(pair, interval, num_period):
    '''
    Response:
    [0] Open time
    [1] Open
    [2] High
    [3] Low
    [4] Close
    [5] Volume
    [6] Close time
    [7] Quote asset volume
    [8] Number of trades
    [9] Taker buy base asset volume
    [10] Taker buy quote asset volume
    [11] Can be ignored
    '''
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

def rsi(klines):
    closing_price = pd.DataFrame(klines)[4]
    closing_price = pd.to_numeric(closing_price)
    return ta.momentum.rsi(closing_price, window=len(closing_price)).iloc[-1]

def get_crypto_df(pairs=PAIRS, indicator=INDICATORS, num_period=NUMPERIOD):

    columns = ['pair']
    columns+=indicator
    df = pd.DataFrame(columns=columns)

    for pair in tqdm(pairs):

        try:
            row_info = dict()

            for column in columns:
                
                if column == 'pair':
                    row_info[column] = pair

                if column == 'rsi_1m':
                    row_info[column] = rsi(historical_klines(pair, '1m', num_period))

                if column == 'rsi_5m':
                    row_info[column] = rsi(historical_klines(pair, '5m', num_period))

                if column == 'rsi_10m':
                    row_info[column] = rsi(historical_klines(pair, '10m', num_period))

                if column == 'rsi_15m':
                    row_info[column] = rsi(historical_klines(pair, '15m', num_period))

                if column == 'rsi_30m':
                    row_info[column] = rsi(historical_klines(pair, '30m', num_period))

                if column == 'rsi_1h':
                    row_info[column] = rsi(historical_klines(pair, '1h', num_period))

                if column == 'rsi_1d':
                    row_info[column] = rsi(historical_klines(pair, '1d', num_period))
            
            df = df.append(row_info, ignore_index=True)
        except:
            continue
    
    return df
            

if __name__ == '__main__':
    print('hello')