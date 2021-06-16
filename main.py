import click
from model import *
from tradeinterface import *
from tradecalc import *


@click.group()
def main():
    pass

# # for experiment
# @main.command()
# @click.option('-c1', default=0.0)
# @click.argument('c2')
# def sample(c1, c2):
#     '''
#     sample
#     '''
#     print('c1', c1)
#     print('c2', c2)

# Set Capital
@main.command()
@click.argument('c1')
@click.argument('c2', default=0.0)
@click.argument('c3', default=0.0)
def c(c1, c2, c3):
    '''
    Set Capital Price in USDT. Risk percentage is be based on this price.
    '''
    capital = float(c1) + float(c2) + float(c3)
    set_capital(capital)

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

# Market Long Entry
@main.command()
@click.argument('pair')
def mlong(pair):
    '''
    Market Long Entry
    '''
    position_size = get_position_size(pair)
    market_long_entry(pair, position_size)

# Market Short Entry
@main.command()
@click.argument('pair')
def mshort(pair):
    '''
    Market Short Entry
    '''
    position_size = get_position_size(pair)
    market_short_entry(pair, position_size)

# Limit Long Entry
@main.command()
@click.argument('pair')
def llong(pair):
    '''
    Limit Long Entry
    '''
    position_size = get_position_size(pair)
    entry_price = get_target_entry(pair)
    limit_long_entry(pair, position_size, entry_price)

# Limit Short Entry
@main.command()
@click.argument('pair')
def lshort(pair):
    '''
    Limit Short Entry
    '''
    position_size = get_position_size(pair)
    entry_price = get_target_entry(pair)
    limit_short_entry(pair, position_size, entry_price)

# Stop Limit Long Entry
@main.command()
@click.argument('pair')
def sllong(pair):
    '''
    Stop Limit Long Entry
    '''
    position_size = get_position_size(pair)
    entry_price = get_target_entry(pair)
    stop_limit_long_entry(pair, position_size, entry_price)

# Stop Limit Short Entry
@main.command()
@click.argument('pair')
def slshort(pair):
    '''
    Stop Limit Short Entry
    '''
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
    print('entry:\t{} USDT'.format(entry))
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


    

# # Set Risk
# @main.command()
# @click.argument('risk')
# def setrisk(risk):
#     '''
#     Set risk in terms of amount in USDT
#     '''
#     set_risk(risk)

# # Append take profit
# @main.command()
# @click.argument('pair')
# @click.argument('tp')
# def appendtp(pair, tp):
#     '''
#     Append take profit
#     '''
#     min_price_step = get_min_price_step(pair)
#     append_take_profit(pair, round_param(tp, min_price_step))


# # Calculate Max Position
# @main.command()
# @click.argument('pair')
# def calcmaxpos(pair):
#     '''
#     Calculate Maximum position size based on risk amount, target entry and target exit
#     '''
#     max_position_size = calc_position_size(
#         entry_price=get_target_entry(pair),
#         stop_loss_price=get_target_exit(pair),
#         min_lot_size=get_min_lot_size(pair),
#         risk=get_risk()
#     )
#     print('{} max_position_size is {}'.format(pair, max_position_size))
#     # set_max_position_size(pair, max_position_size)

# # Set Position
# @main.command()
# @click.argument('pair')
# @click.argument('position_size')
# def setpositionsize(pair, position_size):
#     '''
#     Set Position
#     '''
#     set_position_size(pair, position_size)

# # Initialize Default Pair Info
# @main.command()
# def pairinfoinit():
#     '''
#     Initialize assigned variables
#     '''
#     pair_info = get_pair_info()
#     init_pair_info(pair_info)

# # Print Open Orders
# @main.command()
# @click.argument('pair')
# def printopenorders(pair):
#     '''
#     Print Open Orders
#     '''
#     get_all_orders(pair)

# # Print Open Position
# @main.command()
# @click.argument('pair')
# def printopenposition(pair):
#     '''
#     Print Open Position
#     '''
#     get_open_position(pair)

# # Print Recommended exit prices
# @main.command()
# @click.argument('pair')
# def printexitprice(pair):
#     '''
#     Print Recommended exit prices
#     '''
#     get_exit_price(pair)

# # Set SL as percentage loss
# @main.command()
# @click.argument('pair')
# @click.argument('risk_percentage')
# def setslriskpercentage(pair, risk_percentage):
#     '''
#     Set SL as percentage loss
#     '''
#     set_sl_risk_percentage(pair, risk_percentage)

# # Set SL as price
# @main.command()
# @click.argument('pair')
# @click.argument('price')
# def setsl(pair, price):
#     '''
#     Set SL price
#     '''
#     set_sl(pair, price)

# # Set TP as percentage reward
# @main.command()
# @click.argument('pair')
# @click.argument('rewardpercentage')
# def settprewardpercentage(pair, rewardpercentage):
#     '''
#     Set TP as percentage reward
#     '''
#     set_tp_reward_percentage(pair, rewardpercentage)

# # Set TP as price
# @main.command()
# @click.argument('pair')
# @click.argument('price')
# def settp(pair, price):
#     '''
#     Set TP price
#     '''
#     set_tp(pair, price)

# # Print PNL based on target entry and exit price
# @main.command()
# @click.argument('pair')
# def printtargetpnl(pair):
#     '''
#     TODO: Print PNL based on target entry and exit price
#     '''
#     pass


# # Show info
# @main.command()
# @click.argument('pair')
# def showaccountinfo():
#     '''
#     Show Account Info
#     '''
#     capital = float(get_capital())
#     risk = float(get_risk())
#     percent_risk = (risk/capital)*100.0
#     print('Capital:\t{:.2f}\tUSDT'.format(capital))
#     print('Risk:   \t{:.2f}\tUSDT ({:.2f}%)'.format(risk, percent_risk))


if __name__ == '__main__':
    main()