from src.binance_futures import BinanceFutures


def get_pair_info():
    exchange = BinanceFutures(account='binanceaccount1', pair='BTCUSDT', demo=False)
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
    print('TODO: market_long_entry')

def market_short_entry(pair, position_size):
    print('TODO: market_short_entry')

def limit_long_entry(pair, position_size, entry_price):
    print('TODO: limit_long_entry')

def limit_short_entry(pair, position_size, entry_price):
    print('TODO: limit_short_entry')

def stop_limit_long_entry(pair, position_size, entry_price):
    print('TODO: stop_limit_long_entry')

def stop_limit_short_entry(pair, position_size, entry_price):
    print('TODO: stop_limit_short_entry')

def print_open_orders(pair):
    print('TODO: print_open_orders(pair)')

def print_open_position(pair):
    print('TODO: print_open_position(pair)')

def close_open_position(pair):
    print('TODO: close_open_position(pair)')

def cancel_open_order(pair):
    print('TODO: cancel_open_order(pair)')

def print_exit_price(pair):
    print('TODO: print_exit_price(pair)')

def set_sl_risk_percentage(pair, risk_percentage):
    print('TODO: set_sl_risk_percentage(pair, risk_percentage)')

def set_sl(pair, price):
    print('TODO: set_sl(pair, price)')

def set_tp_reward_percentage(pair, rewardpercentage):
    print('TODO: set_tp_reward_percentage(pair, rewardpercentage)')

def set_tp(pair, price):
    print('TODO: set_tp(pair, price)')
