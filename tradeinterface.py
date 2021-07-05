from src.binance_futures import BinanceFutures
from src.binance_futures_websocket import BinanceFuturesWs
from tradecalc import *
from model import *
import time
import src.strategy as strategy

BINANCE_ACCOUNT = 'binanceaccount2'
BINANCE_ACCOUNT_VIEWING = 'binanceaccount1'

def get_pair_info():
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair='', demo=False)
    raw_pair_info = exchange.get_futures_exchange_info()['symbols']
    pair_info = dict()
    for pair in raw_pair_info:
        if pair['symbol'][-len('USDT'):] == 'USDT':
            pair_info[pair['symbol']] = {
                'min_lot_size' : pair['filters'][1]['minQty'],
                'min_price_step' : pair['filters'][0]['tickSize'],
                'take_profit':[]
            }
    return pair_info

def market_long_entry(pair, position_size):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    market_price = exchange.get_market_price()
    dummy_price = round_param(float(market_price)*(1.00+0.005), get_min_price_step(pair))
    dummy_price = float(dummy_price)
    exchange.entry("Long", True, position_size, limit=dummy_price)

def market_short_entry(pair, position_size):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    market_price = exchange.get_market_price()
    dummy_price = round_param(float(market_price)*(1.00-0.005), get_min_price_step(pair))
    dummy_price = float(dummy_price)
    exchange.entry("Short", False, position_size, limit=dummy_price)

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
    position = exchange.get_position()
    position_size = float(position['positionAmt'])
    print('position_size {}'.format(position_size))

    if position_size == 0.0:
        error_print('No open position for {} pair'.format(pair))
        return

    market_price = exchange.get_market_price()
    print('market_price {}'.format(market_price))

    if position_size > 0.0:
        dummy_price = round_param(float(market_price)*(1.00-0.005), get_min_price_step(pair))
        dummy_price = float(dummy_price)
        print('Long dummy_price {}'.format(dummy_price))
        exchange.entry("Short", False, abs(position_size), limit=dummy_price, reduce_only=True)

    if position_size < 0.0:
        dummy_price = round_param(float(market_price)*(1.00+0.005), get_min_price_step(pair))
        dummy_price = float(dummy_price)
        exchange.entry("Long", True, abs(position_size), limit=dummy_price, reduce_only=True)

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
    exchange.set_sl(price)

def set_mul_tp(pair, tp_targets):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    exchange.set_mul_tp(tp_targets)

def set_tp_reward_percentage(pair, rewardpercentage):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    print('TODO: set_tp_reward_percentage(pair, rewardpercentage)')

def set_tp(pair, price):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    print('TODO: set_tp(pair, price)')

def cancel_sl(pair):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    sl_orders = exchange.get_sl_order()
    if sl_orders:
        for sl_order in sl_orders:
            exchange.cancel(sl_order['clientOrderId'])

def cancel_tp(pair):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    tp_orders = exchange.get_tp_order()
    if tp_orders:
        for tp_order in tp_orders:
            exchange.cancel(tp_order['clientOrderId'])
        
def get_market_price(pair):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    return exchange.get_market_price()

def get_tp_order(pair):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    return exchange.get_tp_order()

def get_sl_order(pair):
    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    return exchange.get_sl_order()

def auto_sltp(pair, sl, tp_targets):

    exchange = BinanceFutures(account=BINANCE_ACCOUNT, pair=pair, demo=False)
    
    def set_sltp(*args, **kwargs):
        exchange.set_sl(sl)
        exchange.set_mul_tp(tp_targets)
    
    exchange.ws = BinanceFuturesWs(account=exchange.account, pair=exchange.pair, test=exchange.demo)
    exchange.ws.bind('position',set_sltp)

    while True:
        time.sleep(1)

def display_plot(**kwargs):
    
    cls = getattr(strategy, 'statdisp')
    bot = cls()
    bot.test_net  = False
    bot.back_test = False
    bot.stub_test = False
    bot.hyperopt  = False
    bot.account = BINANCE_ACCOUNT_VIEWING
    bot.exchange_arg = 'binance'
    bot.pair = kwargs['pair']
    bot.set_capital(kwargs['capital'])
    bot.set_min_price_step(kwargs['min_price_step'])
    bot.run()
    bot.animate_plot.set_label(bot.pair)
    bot.run_animate_plot()



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
