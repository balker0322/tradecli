import pickle as pk
from message import *

MODEL_FILE_NAME = 'model.pk'

def dump_file(data):
    pk.dump(data,open(MODEL_FILE_NAME, 'wb'))

def load_file(file_name=MODEL_FILE_NAME):
    return pk.load(open(file_name, 'rb'))

def init_pair_info(pair_info):
    dump_file(pair_info)

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
    print('risk percentage is entered')
    pass

def set_risk(risk):
    print('risk amount is entered')
    pass

def get_risk():
    print('TODO: get_risk')
    pass

def set_position_size(pair, position_size):
    print('TODO: set_position_size(pair, position_size)')
    pass

def get_position_size(pair):
    print('TODO: get_position_size(pair)')
    pass

def set_target_entry(pair, target_entry):
    print('TODO: set_target_entry(pair, target_entry)')
    pass

def get_target_entry(pair):
    print('TODO: get_target_entry(pair, target_entry)')
    pass

def set_target_exit(pair, target_exit):
    print('TODO: set_target_exit(pair, target_exit)')
    pass

def get_target_exit(pair):
    print('TODO: get_target_exit(pair, target_exit)')
    pass