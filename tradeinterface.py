from src.binance_futures import BinanceFutures
from tradecalc import *
from model import *

BINANCE_ACCOUNT = 'binanceaccount2'

def get_pair_info():
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair='', demo=False)
    raw_pair_info = exchange.get_futures_exchange_info()['symbols']
    pair_info = dict()
    for pair in raw_pair_info:
        if pair['symbol'][-len('USDT'):] == 'USDT':
            pair_info[pair['symbol']] = {
                'min_lot_size' : pair['filters'][1]['minQty'],
                'min_price_step' : pair['filters'][0]['tickSize'],
            }
    return pair_info

def market_long_entry(pair, position_size):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    exchange.entry("Long", True, position_size)

def market_short_entry(pair, position_size):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    exchange.entry("Short", False, position_size)

def limit_long_entry(pair, position_size, entry_price):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    exchange.entry("Long", True, position_size, limit=entry_price)

def limit_short_entry(pair, position_size, entry_price):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    exchange.entry("Short", False, position_size, limit=entry_price)

def stop_limit_long_entry(pair, position_size, entry_price):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    dummy_price = round_param(float(entry_price)*(1.00+0.005), get_min_price_step(pair))
    dummy_price = float(dummy_price)
    exchange.entry("Long", True, position_size, limit=dummy_price, stop=entry_price)

def stop_limit_short_entry(pair, position_size, entry_price):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    dummy_price = round_param(float(entry_price)*(1.00-0.005), get_min_price_step(pair))
    dummy_price = float(dummy_price)
    exchange.entry("Short", False, position_size, limit=dummy_price, stop=entry_price)

def get_all_orders(pair):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    return exchange.get_all_open_orders()

def get_open_position(pair):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    return exchange.get_position()

def close_open_position(pair):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    exchange.close_all()

def cancel_all_order(pair):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    exchange.cancel_all()

def get_exit_price(pair):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    print('TODO: print_exit_price(pair)')

def set_sl_risk_percentage(pair, risk_percentage):
    print('TODO: set_sl_risk_percentage(pair, risk_percentage)')

def set_sl(pair, price):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    print('TODO: set_sl(pair, price)')

def set_tp_reward_percentage(pair, rewardpercentage):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    print('TODO: set_tp_reward_percentage(pair, rewardpercentage)')

def set_tp(pair, price):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    print('TODO: set_tp(pair, price)')



if __name__=='__main__':
    position_size = 100.0
    pair='XLMUSDT'
    entry_price = 0.3292
    # exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    # stop_limit_long_entry(pair, position_size, entry_price)
    # x = print_open_orders(pair)
    # x = print_open_position(pair)
    # print(x)
    # exchange.entry("Long", True, position_size, limit=0.33, stop=0.4)
    # exchange.entry("Short", False, position_size)
    # exchange.entry("Long", True, position_size, limit=0.30, stop=0.40)
    # exchange.entry("Long", True, position_size, stop=0.33718)
