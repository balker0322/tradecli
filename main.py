import click
from model import *
from tradeinterface import *
from tradecalc import *


def update_user_params(**kwargs):
    if kwargs['pr']:
        set_pair(kwargs['pr'])
    if kwargs['rp']:
        set_risk_as_percent(kwargs['rp'])
    if kwargs['sl']:
        set_sl(kwargs['sl'])
    if kwargs['e']:
        set_target_entry(kwargs['e'])
    if (kwargs['rp']):
        set_risk_as_percent(kwargs['rp'])
    if not (kwargs['rv'] == 1.0):
        pass

    # min_lot_size = get_min_lot_size(pair)
    # max_position_size = calc_position_size(
    #     entry_price=get_target_entry(pair),
    #     stop_loss_price=get_target_stop_loss(pair),
    #     min_lot_size=min_lot_size,
    #     risk=get_risk()
    # )



@click.group()
def main():
    pass

# experiment
@main.command()
@click.option('-q', multiple=True)
def exp(q):
    print(q)


# Set Capital
@main.command()
@click.argument('capital', nargs=-1)
def c(capital):
    '''
    Set Capital Price in USDT. Risk percentage is be based on this price.
    '''
    total = 0.0
    for cap in capital:
        total += float(cap)
    set_capital(total)

# set pair
@main.command()
@click.argument('pr')
def pr(pr):
    '''
    Set Pair
    '''
    set_pair(pr.upper())

# Set Risk Percentage
@main.command()
@click.argument('risk_percentage')
def rp(risk_percentage):
    '''
    Set risk in terms of percent of capital
    '''
    set_risk_as_percent(risk_percentage)

# Set Target Entry
@main.command()
@click.argument('pair')
@click.argument('target_entry')
def e(pair, target_entry):
    '''
    Set Target Entry
    '''
    set_target_entry(pair, round_param(target_entry,get_min_price_step(pair)))

# Set Target Stop Loss
@main.command()
@click.argument('pair')
@click.argument('target_stop_loss')
def sl(pair, target_stop_loss):
    '''
    Set Target Stop Loss
    '''
    set_target_stop_loss(pair, round_param(target_stop_loss,get_min_price_step(pair)))

# Calculate Max Position
@main.command()
@click.argument('pair')
@click.option('-p',default=1.0)
def ps(pair, p):
    '''
    Set Position Size
    '''
    min_lot_size = get_min_lot_size(pair)
    max_position_size = calc_position_size(
        entry_price=get_target_entry(pair),
        stop_loss_price=get_target_stop_loss(pair),
        min_lot_size=min_lot_size,
        risk=get_risk()
    )
    print('{} max_position_size is {}'.format(pair, max_position_size))
    set_position_size(pair, round_param(max_position_size*p,min_lot_size))

# open position
@main.command()
@click.argument('et')
@click.argument('s')
@click.option('-pr',default='')
@click.option('-e',default=0.0)
@click.option('-sl',default=0.0)
@click.option('-rp',default=0.0)
@click.option('-rv',default=1.0)
@click.option('-tp', multiple=True)
@click.option('-tprr', multiple=True)
def open(et, s, **kwargs):
    entry_type = et.lower()
    side = s.lower()

    update_user_params(**kwargs)

    if entry_type == 'm' and side == 'long':
        mlong()
    elif entry_type == 'l' and side == 'long':
        llong()
    elif entry_type == 'sl' and side == 'long':
        sllong()
    elif entry_type == 'm' and side == 'short':
        mshort()
    elif entry_type == 'l' and side == 'short':
        lshort()
    elif entry_type == 'sl' and side == 'short':
        slshort()
    else:
        error_print('Invalid arguments')
        return

# Market Long Entry
def mlong():
    '''
    Market Long Entry
    '''
    pair = get_pair()
    position_size = get_position_size(pair)
    market_long_entry(pair, position_size)

# Market Short Entry
def mshort():
    '''
    Market Short Entry
    '''
    pair = get_pair()
    position_size = get_position_size(pair)
    position_size = get_position_size(pair)
    market_short_entry(pair, position_size)

# Limit Long Entry
def llong():
    '''
    Limit Long Entry
    '''
    position_size = get_position_size(pair)
    entry_price = get_target_entry(pair)
    limit_long_entry(pair, position_size, entry_price)

# Limit Short Entry
def lshort():
    '''
    Limit Short Entry
    '''
    pair = get_pair()
    position_size = get_position_size(pair)
    entry_price = get_target_entry(pair)
    limit_short_entry(pair, position_size, entry_price)

# Stop Limit Long Entry
def sllong():
    '''
    Stop Limit Long Entry
    '''
    pair = get_pair()
    position_size = get_position_size(pair)
    entry_price = get_target_entry(pair)
    stop_limit_long_entry(pair, position_size, entry_price)

# Stop Limit Short Entry
def slshort():
    '''
    Stop Limit Short Entry
    '''
    pair = get_pair()
    position_size = get_position_size(pair)
    entry_price = get_target_entry(pair)
    stop_limit_short_entry(pair, position_size, entry_price)


# Set take profit
@main.command()
@click.argument('pair')
@click.argument('tp1', default=0.0)
@click.argument('tp2', default=0.0)
@click.argument('tp3', default=0.0)
@click.argument('tp4', default=0.0)
@click.argument('tp5', default=0.0)
def tp(pair, **kwargs):
    '''
    Set take profit
    '''
    min_price_step = get_min_price_step(pair)
    take_profit_list = []
    for tp in kwargs:
        if float(tp) == 0.0:
            continue
        take_profit_list.append(round_param(tp, min_price_step))
    set_take_profit(pair, take_profit_list)


# Set take profit as rr ratio
@main.command()
@click.argument('pair')
@click.argument('rr1', default=0.0)
@click.argument('rr2', default=0.0)
@click.argument('rr3', default=0.0)
@click.argument('rr4', default=0.0)
@click.argument('rr5', default=0.0)
def tprr(pair, **kwargs):
    '''
    Set take profit as rr ratio
    '''
    min_price_step = get_min_price_step(pair)
    entry_price = get_target_entry(pair)
    stop_loss_price = get_target_stop_loss(pair)
    take_profit_list = []
    for rr in kwargs:
        if float(kwargs[rr]) == 0.0:
            continue
        take_profit_list.append(calc_exit_price(entry_price, stop_loss_price, min_price_step, kwargs[rr]))
    set_take_profit(pair, take_profit_list)

# Close Open Position
@main.command()
@click.argument('pair')
def cp(pair):
    '''
    Close Open Position
    '''
    close_open_position(pair)

# Cancel Open Orders
@main.command()
@click.argument('pair')
def co(pair):
    '''
    Cancel Open Orders
    '''
    cancel_all_order(pair)

# Submit SL and TP
@main.command()
@click.argument('pair')
def sltp(pair):
    '''
    Submit SL and TP
    '''
    position = float(get_open_position(pair)['positionAmt'])
    if position == 0.0:
        print('No open position for {} pair'.format(pair))
        return
    
    min_lot_size = get_min_lot_size(pair)
    tp_list = get_take_profit(pair)
    sl_price = get_target_stop_loss(pair)
    tp_count = len(tp_list)
    tp_targets = []
    total_pos_size_set = 0.0

    for i, tp in enumerate(tp_list):
        tp_pos_size = round_param(abs(position)/float(tp_count),min_lot_size)
        if i == tp_count - 1.0:
            tp_pos_size = abs(position) - total_pos_size_set
        tp_targets.append({
            'price':tp,
            'position_size':tp_pos_size,
        })
        total_pos_size_set += float(tp_pos_size)
    
    set_sl(pair,sl_price)
    set_mul_tp(pair,tp_targets)


# Calculate exit prices
@main.command()
@click.argument('pair')
def calcrr(pair):
    '''
    Calculate exit prices
    '''
    target_entry = get_target_entry(pair)
    target_exit = get_target_stop_loss(pair)
    min_price_step = get_min_price_step(pair)
    rr_ratio = ['-1','0','1','2','3','4']
    side = 'LONG' if target_exit < target_entry else 'SHORT'
    print('========================================')
    print(pair)
    print('{} ENTRY: {} USDT'.format(pair,side,target_entry))
    for rr in rr_ratio:
        price = calc_exit_price(entry_price=target_entry, stop_loss_price=target_exit, min_price_step=min_price_step, rr_ratio=rr)
        s = 'RR_RATIO: {:.1f}'.format(float(rr)) if float(rr) > 0.0 else ('STOP LOSS' if float(rr) < 0.0 else 'BREAKEVEN')
        print('{}\t{}'.format(
            s,
            price
        ))
    print('========================================')


# Show current status
@main.command()
@click.argument('pair')
def stat(pair):
    '''
    Show current status
    '''
    print(pair)
    print('Market Price: {} USDT'.format(get_market_price(pair)))

    position = get_open_position(pair)
    if float(position['positionAmt']) == 0.0:
        print('Position: None')
        return
    
    entryPrice = position['entryPrice']
    positionAmt = position['positionAmt']
    print('Position:')
    print('entry:\t{} USDT'.format(entryPrice))
    print('qty:\t{} {}'.format(positionAmt, pair[-4:]))

    sl_list = get_sl_order(pair)
    tp_list = get_tp_order(pair)

    capital = get_capital(pair)

    if sl_list:
        print('SL:')
        print('{}\t{}\t{}'.fomat('price','qty','pnl'))
        for sl in sl_list:
            price = sl['stopPrice']
            qty = sl['origQty']
            pnl = calc_percent_pnl(entryPrice, positionAmt, price, capital)
            pnl = '{0}{1:.2f}%'.format('+' if pnl > 0.0 else ' ' if pnl == 0.0 else '',pnl*100.0)
            print('{} USDT\t{} {}\t{}'.format(price,qty,pair[-4:],pnl))
    else:
        print('SL: No set Stop Loss')

    if tp_list:
        print('TP:')
        print('{}\t{}\t{}'.fomat('price','qty','pnl'))
        for sl in sl_list:
            price = sl['price']
            qty = sl['origQty']
            pnl = calc_percent_pnl(entryPrice, positionAmt, price, capital)
            pnl = '{0}{1:.2f}%'.format('+' if pnl > 0.0 else ' ' if pnl == 0.0 else '',pnl*100.0)
            print('{} USDT\t{} {}\t{}'.format(price,qty,pair[-4:],pnl))
    else:
        print('TP: No set Take Profit')


if __name__ == '__main__':
    main()