import pickle as pk
from message import *
from tradecalc import *

MODEL_FILE_NAME = 'model.pk'

def dump_file(data):
    pk.dump(data,open(MODEL_FILE_NAME, 'wb'))

def load_file(file_name=MODEL_FILE_NAME):
    return pk.load(open(file_name, 'rb'))

def init_pair_info(pair_info):
    try:
        model_file = load_file()
        for pair in pair_info:
            model_file[pair]=pair_info[pair]
        dump_file(model_file)
    except:
        dump_file(pair_info)

def get_min_lot_size(pair):
    try:
        model_file = load_file()
        return model_file[pair]['min_lot_size']
    except Exception as e:
        error_print('error in get_min_lot_size')
        error_print(e)

def get_min_price_step(pair):
    try:
        model_file = load_file()
        return model_file[pair]['min_price_step']
    except Exception as e:
        error_print('error in get_min_price_step')
        error_print(e)

def set_capital(capital):
    try:
        cap = float(capital)
        model_file = load_file()
        model_file['capital'] = cap
        dump_file(model_file)
        info_print('capital is set to {}'.format(get_capital()))
    except:
        error_print('error')

def get_capital():
    try:
        model_file = load_file()
        return model_file['capital']
    except:
        error_print('error')

def set_risk_as_percent(percentage):
    risk = float(percentage) * float(get_capital())
    set_risk(risk)

def set_risk(risk):
    try:
        model_file = load_file()
        model_file['risk'] = -1.0*abs(float(risk))
        dump_file(model_file)
        info_print('risk is set to {}'.format(get_risk()))
    except:
        error_print('error')

def get_risk():
    try:
        model_file = load_file()
        return model_file['risk']
    except:
        error_print('error')

def set_position_size(pair, position_size):
    try:
        model_file = load_file()
        model_file[pair]['position_size'] = float(position_size)
        dump_file(model_file)
        info_print('{} pair position size is set to {} {}'.format(pair, get_position_size(pair), pair[:-len('USDT')]))
    except Exception as e:
        error_print('error in set_position_size')
        error_print(e)

def get_position_size(pair):
    try:
        model_file = load_file()
        return model_file[pair]['position_size']
    except Exception as e:
        error_print('error in get_position_size')
        error_print(e)

def set_max_position_size(pair, max_position_size):
    try:
        model_file = load_file()
        model_file[pair]['max_position_size'] = float(max_position_size)
        dump_file(model_file)
        info_print('{} pair max position size is set to {} {}'.format(pair, get_max_position_size(pair), pair[:-len('USDT')]))
    except Exception as e:
        error_print('error in set_max_position_size')
        error_print(e)

def get_max_position_size(pair):
    try:
        model_file = load_file()
        return model_file[pair]['max_position_size']
    except Exception as e:
        error_print('error in get_max_position_size')
        error_print(e)


def set_target_entry(pair, target_entry):
    try:
        model_file = load_file()
        model_file[pair]['target_entry'] = float(target_entry)
        dump_file(model_file)
        info_print('{} pair target entry is set to {} USDT'.format(pair, get_target_entry(pair)))
    except Exception as e:
        error_print('error in set_target_entry')
        error_print(e)

def get_target_entry(pair):
    try:
        model_file = load_file()
        return model_file[pair]['target_entry']
    except Exception as e:
        error_print('error in get_target_entry')
        error_print(e)

def set_target_exit(pair, target_exit):
    try:
        model_file = load_file()
        model_file[pair]['stop_loss'] = float(target_exit)
        dump_file(model_file)
        info_print('{} pair target exit is set to {} USDT'.format(pair, get_target_exit(pair)))
    except Exception as e:
        error_print('error in set_target_exit')
        error_print(e)

def get_target_exit(pair):
    try:
        model_file = load_file()
        return model_file[pair]['stop_loss']
    except Exception as e:
        error_print('error in get_target_exit')
        error_print(e)

def append_take_profit(pair, take_profit):
    try:
        model_file = load_file()
        model_file[pair]['take_profit'].append(float(take_profit))
        dump_file(model_file)
        info_print('{} pair take profit is set to {} USDT'.format(pair, get_take_profit(pair)))
    except Exception as e:
        error_print('error in set_take_profit')
        error_print(e)

def set_take_profit(pair, take_profit_list):
    try:
        model_file = load_file()
        model_file[pair]['take_profit'] = take_profit_list
        dump_file(model_file)
        info_print('{} pair take profit is set to {} USDT'.format(pair, get_take_profit(pair)))
    except Exception as e:
        error_print('error in set_take_profit')
        error_print(e)

def get_take_profit(pair):
    try:
        model_file = load_file()
        return model_file[pair]['take_profit']
    except Exception as e:
        error_print('error in get_take_profit')
        error_print(e)


