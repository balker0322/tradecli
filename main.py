import click
from model import *
from tradeinterface import *
from tradecalc import *


def update_user_params(**kwargs):
    if kwargs['pr']:
        set_pair(kwargs['pr'])

    pair = get_pair()    

    if kwargs['rp']:
        set_risk_as_percent(kwargs['rp'])
    if kwargs['sl']:
        set_target_stop_loss(pair, kwargs['sl'])
    if kwargs['e']:
        set_target_entry(pair, kwargs['e'])
    if kwargs['sl'] or  kwargs['e'] or  kwargs['rp']:
        min_lot_size = get_min_lot_size(pair)
        max_position_size = calc_position_size(
            entry_price=get_target_entry(pair),
            stop_loss_price=get_target_stop_loss(pair),
            min_lot_size=min_lot_size,
            risk=get_risk()
        )
        set_max_position_size(pair, max_position_size)
        set_position_size(pair, max_position_size)
    if kwargs['rv']:
        set_position_size(
            pair,
            round_param(
                get_max_position_size(pair)* kwargs['rv'],
                get_min_lot_size(pair)
            )
        )

@click.group()
@click.option('-pr',default='')
@click.option('-e',default=0.0)
@click.option('-sl',default=0.0)
@click.option('-rp',default=0.0)
@click.option('-rv',default=0.0)
def main(**kwargs):
    update_user_params(**kwargs)

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

# Market Long Entry
@main.command()
def mlong():
    '''
    Market Long Entry
    '''
    pair = get_pair()
    position_size = get_position_size(pair)
    market_long_entry(pair, position_size)

# Market Short Entry
@main.command()
def mshort():
    '''
    Market Short Entry
    '''
    pair = get_pair()
    position_size = get_position_size(pair)
    position_size = get_position_size(pair)
    market_short_entry(pair, position_size)

# Limit Long Entry
@main.command()
def llong():
    '''
    Limit Long Entry
    '''
    position_size = get_position_size(pair)
    entry_price = get_target_entry(pair)
    limit_long_entry(pair, position_size, entry_price)

# Limit Short Entry
@main.command()
def lshort():
    '''
    Limit Short Entry
    '''
    pair = get_pair()
    position_size = get_position_size(pair)
    entry_price = get_target_entry(pair)
    limit_short_entry(pair, position_size, entry_price)

# Stop Limit Long Entry
@main.command()
def sllong():
    '''
    Stop Limit Long Entry
    '''
    pair = get_pair()
    position_size = get_position_size(pair)
    entry_price = get_target_entry(pair)
    stop_limit_long_entry(pair, position_size, entry_price)

# Stop Limit Short Entry
@main.command()
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
@click.argument('tp_list', nargs=-1)
def tp(tp_list):
    '''
    Set take profit
    '''
    pair = get_pair()
    min_price_step = get_min_price_step(pair)
    take_profit_list = []
    for tp in tp_list:
        if float(tp) == 0.0:
            continue
        take_profit_list.append(round_param(tp, min_price_step))
    set_take_profit(pair, take_profit_list)


# Set take profit as rr ratio
@main.command()
@click.argument('rr_list', nargs=-1)
def tprr(rr_list):
    '''
    Set take profit as rr ratio
    '''
    pair = get_pair()
    min_price_step = get_min_price_step(pair)
    entry_price = get_target_entry(pair)
    stop_loss_price = get_target_stop_loss(pair)
    take_profit_list = []
    for rr in rr_list:
        if float(rr) == 0.0:
            continue
        take_profit_list.append(calc_exit_price(entry_price, stop_loss_price, min_price_step, rr))
    set_take_profit(pair, take_profit_list)

# Close Open Position
@main.command()
def cp():
    '''
    Close Open Position
    '''
    pair = get_pair()
    close_open_position(pair)

# Cancel Open Orders
@main.command()
def co():
    '''
    Cancel Open Orders
    '''
    pair = get_pair()
    cancel_all_order(pair)

# Submit SL and TP
@main.command()
def sltp():
    '''
    Submit SL and TP
    '''
    pair = get_pair()
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
def calcrr():
    '''
    Calculate exit prices
    '''
    pair = get_pair()
    target_entry = get_target_entry(pair)
    target_exit = get_target_stop_loss(pair)
    min_price_step = get_min_price_step(pair)
    rr_ratio = ['-1','0','1','2','3','4']
    side = 'LONG' if target_exit < target_entry else 'SHORT'
    print('========================================')
    print(pair)
    print('{} ENTRY: {} USDT'.format(side,target_entry))
    for rr in rr_ratio:
        price = calc_exit_price(entry_price=target_entry, stop_loss_price=target_exit, min_price_step=min_price_step, rr_ratio=rr)
        s = 'RR_RATIO: {:.1f}'.format(float(rr)) if float(rr) > 0.0 else ('STOP LOSS' if float(rr) < 0.0 else 'BREAKEVEN')
        print('{}\t{} USDT'.format(
            s,
            price
        ))
    print('========================================')


# Show current status
@main.command()
def stat():
    '''
    Show current status
    '''
    pair = get_pair()
    print('========================================')
    print('Capital: {} USDT'.format(get_capital()))
    print('Risk: {0:.2f}%'.format(get_risk_as_percent()*100.0))
    print()
    print('Pair: {}'.format(pair))
    print('Target Entry:        {} USDT'.format(get_target_entry(pair)))
    print('Target Stop Loss:    {} USDT'.format(get_target_stop_loss(pair)))
    print('Entry Position Size: {} {}'.format(get_position_size(pair),pair[:-4]))
    print('Max Position Size:   {} {}'.format(get_max_position_size(pair),pair[:-4]))
    print()
    print('Market Price: {} USDT'.format(get_market_price(pair)))

    position = get_open_position(pair)
    if float(position['positionAmt']) == 0.0:
        print('Position: None')
        print('========================================')
        return
    
    entryPrice = position['entryPrice']
    positionAmt = position['positionAmt']
    print()
    print('Position:')
    print('entry:\t{} USDT'.format(entryPrice))
    print('qty:\t{} {}'.format(positionAmt, pair[-4:]))

    sl_list = get_sl_order(pair)
    tp_list = get_tp_order(pair)

    capital = get_capital()

    if sl_list:
        print()
        print('SL:')
        print('{}\t\t{}\t\t{}'.format('price','qty','pnl'))
        for sl in sl_list:
            price = sl['stopPrice']
            qty = sl['origQty']
            pnl = calc_percent_pnl(entryPrice, positionAmt, price, capital)
            pnl = '{0}{1:.2f} %'.format('+' if pnl > 0.0 else ' ' if pnl == 0.0 else '',pnl*100.0)
            print('{} USDT\t{} {}\t\t{}'.format(price,qty,pair[:-4],pnl))
    else:
        print('SL: No set Stop Loss')

    if tp_list:
        print()
        print('TP:')
        print('{}\t\t{}\t\t{}'.format('price','qty','pnl'))
        for tp in tp_list:
            price = tp['price']
            qty = tp['origQty']
            pnl = calc_percent_pnl(entryPrice, tp['origQty'], price, capital)
            pnl = '{0}{1:.2f} %'.format('+' if pnl > 0.0 else ' ' if pnl == 0.0 else '',pnl*100.0)
            print('{} USDT\t{} {}\t\t{}'.format(price,qty,pair[:-4],pnl))
    else:
        print('TP: No set Take Profit')

    print('========================================')


if __name__ == '__main__':
    main()