import click
from model import *
from tradeinterface import *
from tradecalc import *


@click.group()
def main():
    pass

# Set Capital
@main.command()
@click.argument('c1')
@click.argument('c2', default=0.0)
@click.argument('c3', default=0.0)
def setcapital(c1, c2, c3):
    '''
    Set Capital Price in USDT. Risk percentage is be based on this price.
    '''
    capital = float(c1) + float(c2) + float(c3)
    set_capital(capital)

# Set Risk
@main.command()
@click.argument('risk')
def setrisk(risk):
    '''
    Set risk in terms of amount in USDT
    '''
    set_risk(risk)

# Set Risk Percentage
@main.command()
@click.argument('risk_percentage')
def setriskpercentage(risk_percentage):
    '''
    Set risk in terms of percent of capital
    '''
    set_risk_as_percent(risk_percentage)

# Set Target Entry
@main.command()
@click.argument('pair')
@click.argument('target_entry')
def settargetentry(pair, target_entry):
    '''
    Set Target Entry
    '''
    set_target_entry(pair, target_entry)

# Set Target Exit
@main.command()
@click.argument('pair')
@click.argument('target_exit')
def settargetexit(pair, target_exit):
    '''
    Set Target Exit
    '''
    set_target_exit(pair, target_exit)


# Set take profit
@main.command()
@click.argument('pair')
@click.argument('tp1', default=0.0)
@click.argument('tp2', default=0.0)
@click.argument('tp3', default=0.0)
@click.argument('tp4', default=0.0)
@click.argument('tp5', default=0.0)
def settp(pair, **kwargs):
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
    


# Append take profit
@main.command()
@click.argument('pair')
@click.argument('tp')
def appendtp(pair, tp):
    '''
    Append take profit
    '''
    min_price_step = get_min_price_step(pair)
    append_take_profit(pair, round_param(tp, min_price_step))


# Calculate Max Position
@main.command()
@click.argument('pair')
def calcmaxpos(pair):
    '''
    Calculate Maximum position size based on risk amount, target entry and target exit
    '''
    max_position_size = calc_position_size(
        entry_price=get_target_entry(pair),
        stop_loss_price=get_target_exit(pair),
        min_lot_size=get_min_lot_size(pair),
        risk=get_risk()
    )
    print('{} max_position_size is {}'.format(pair, max_position_size))
    # set_max_position_size(pair, max_position_size)

# Set Position
@main.command()
@click.argument('pair')
@click.argument('position_size')
def setpositionsize(pair, position_size):
    '''
    Set Position
    '''
    set_position_size(pair, position_size)

# Initialize Default Pair Info
@main.command()
def pairinfoinit():
    '''
    Initialize assigned variables
    '''
    pair_info = get_pair_info()
    init_pair_info(pair_info)

# Market Long Entry
@main.command()
@click.argument('pair')
def marketlongentry(pair):
    '''
    Market Long Entry
    '''
    position_size = get_position_size(pair)
    market_long_entry(pair, position_size)

# Market Short Entry
@main.command()
@click.argument('pair')
def marketshortentry(pair):
    '''
    Market Short Entry
    '''
    position_size = get_position_size(pair)
    market_short_entry(pair, position_size)

# Limit Long Entry
@main.command()
@click.argument('pair')
def limitlongentry(pair):
    '''
    Limit Long Entry
    '''
    position_size = get_position_size(pair)
    entry_price = get_target_entry(pair)
    limit_long_entry(pair, position_size, entry_price)

# Limit Short Entry
@main.command()
@click.argument('pair')
def limitshortentry(pair):
    '''
    Limit Short Entry
    '''
    position_size = get_position_size(pair)
    entry_price = get_target_entry(pair)
    limit_short_entry(pair, position_size, entry_price)

# Stop Limit Long Entry
@main.command()
@click.argument('pair')
def stoplimitlongentry(pair):
    '''
    Stop Limit Long Entry
    '''
    position_size = get_position_size(pair)
    entry_price = get_target_entry(pair)
    stop_limit_long_entry(pair, position_size, entry_price)

# Stop Limit Short Entry
@main.command()
@click.argument('pair')
def stoplimitshortentry(pair):
    '''
    Stop Limit Short Entry
    '''
    position_size = get_position_size(pair)
    entry_price = get_target_entry(pair)
    stop_limit_short_entry(pair, position_size, entry_price)

# Print Open Orders
@main.command()
@click.argument('pair')
def printopenorders(pair):
    '''
    Print Open Orders
    '''
    get_all_orders(pair)

# Print Open Position
@main.command()
@click.argument('pair')
def printopenposition(pair):
    '''
    Print Open Position
    '''
    get_open_position(pair)

# Close Open Position
@main.command()
@click.argument('pair')
def closeopenposition(pair):
    '''
    Close Open Position
    '''
    close_open_position(pair)

# Cancel Open Orders
@main.command()
@click.argument('pair')
def cancelopenorder(pair):
    '''
    Cancel Open Orders
    '''
    cancel_all_order(pair)

# Print Recommended exit prices
@main.command()
@click.argument('pair')
def printexitprice(pair):
    '''
    Print Recommended exit prices
    '''
    get_exit_price(pair)

# Set SL as percentage loss
@main.command()
@click.argument('pair')
@click.argument('risk_percentage')
def setslriskpercentage(pair, risk_percentage):
    '''
    Set SL as percentage loss
    '''
    set_sl_risk_percentage(pair, risk_percentage)

# Set SL as price
@main.command()
@click.argument('pair')
@click.argument('price')
def setsl(pair, price):
    '''
    Set SL price
    '''
    set_sl(pair, price)

# Set TP as percentage reward
@main.command()
@click.argument('pair')
@click.argument('rewardpercentage')
def settprewardpercentage(pair, rewardpercentage):
    '''
    Set TP as percentage reward
    '''
    set_tp_reward_percentage(pair, rewardpercentage)

# Set TP as price
@main.command()
@click.argument('pair')
@click.argument('price')
def settp(pair, price):
    '''
    Set TP price
    '''
    set_tp(pair, price)

# Print PNL based on target entry and exit price
@main.command()
@click.argument('pair')
def printtargetpnl(pair):
    '''
    TODO: Print PNL based on target entry and exit price
    '''
    pass


# Show info
@main.command()
@click.argument('pair')
def showaccountinfo():
    '''
    Show Account Info
    '''
    capital = float(get_capital())
    risk = float(get_risk())
    percent_risk = (risk/capital)*100.0
    print('Capital:\t{:.2f}\tUSDT'.format(capital))
    print('Risk:   \t{:.2f}\tUSDT ({:.2f}%)'.format(risk, percent_risk))


# Calculate exit prices
@main.command()
@click.argument('pair')
def calcexitprice(pair):
    '''
    Calculate exit prices
    '''
    target_entry = get_target_entry(pair)
    target_exit = get_target_exit(pair)
    min_price_step = get_min_price_step(pair)
    rr_ratio = ['-1','0','1','2','3','4']
    for rr in rr_ratio:
        price = calc_exit_price(entry_price=target_entry, stop_loss_price=target_exit, min_price_step=min_price_step, rr_ratio=rr)
        s = 'RR_RATIO: {:.1f}'.format(float(rr)) if float(rr) > 0.0 else ('STOPLOSS' if float(rr) < 0.0 else 'BREAKEVEN')
        print('{}\t{}'.format(
            s,
            price
        ))


if __name__ == '__main__':
    main()