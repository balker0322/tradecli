from decimal import Decimal as d

RISK = '0.05'
RR_RATIO = '2.0'
K_FACTOR = '1.0007'


def calc_position_size(entry_price, stop_loss_price, min_lot_size, risk=RISK, k_factor=K_FACTOR):
    if float(entry_price) > float(stop_loss_price):
        return long_pos_size(entry_price, stop_loss_price, min_lot_size, risk)
    return short_pos_size(entry_price, stop_loss_price, min_lot_size, risk)

def long_tp(entry_price, position_size, min_price_step, risk=RISK, rr_ratio=RR_RATIO, k_factor=K_FACTOR):
    adj_factor = d('1.0') / d(k_factor)
    tp = abs(d(risk)*d(rr_ratio)) / abs(d(position_size))
    tp = d(entry_price) + tp
    tp = tp / adj_factor
    return float(round_param(tp, min_price_step))

def long_sl(entry_price, position_size, min_price_step, risk=RISK, k_factor=K_FACTOR):
    adj_factor = d('1.0') / d(k_factor)
    sl = abs(d(risk)) / abs(d(position_size))
    sl = d(entry_price) - sl
    sl = sl / adj_factor
    return float(round_param(sl, min_price_step))

def long_pos_size(entry_price, stop_loss_price, min_lot_size, risk=RISK, k_factor=K_FACTOR):
    adj_factor = d('1.0') / d(k_factor)
    ps = d(stop_loss_price)*adj_factor - d(entry_price)
    ps = d(risk) / ps
    return float(round_param(ps, min_lot_size))

def short_tp(entry_price, position_size, min_price_step, risk=RISK, rr_ratio=RR_RATIO, k_factor=K_FACTOR):
    adj_factor = d('1.0') / d(k_factor)
    tp = abs(d(risk)*d(rr_ratio)) / abs(d(position_size))
    tp = d(entry_price)*adj_factor - tp
    return float(round_param(tp, min_price_step))

def short_sl(entry_price, position_size, min_price_step, risk=RISK, k_factor=K_FACTOR):
    adj_factor = d('1.0') / d(k_factor)
    sl = abs(d(risk)) / abs(d(position_size))
    sl = d(entry_price)*adj_factor + sl
    return float(round_param(sl, min_price_step))

def short_pos_size(entry_price, stop_loss_price, min_lot_size, risk=RISK, k_factor=K_FACTOR):
    adj_factor = d('1.0') / d(k_factor)
    ps = d(entry_price)*adj_factor - d(stop_loss_price)
    ps = d(risk) / ps
    return float(round_param(ps, min_lot_size))

def round_param(param_size, min_param_step):
    return param_size - (param_size%d(min_param_step))

if __name__ == "__main__":
    print(short_sl('36000.0', '0.0321', '0.1'))