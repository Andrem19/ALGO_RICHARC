import shared_vars as sv
from models.settings import Settings
import helpers.util as util
import coins


def profit_counter(taker_maker: bool, open_price: float, buy: bool, close_price: float) -> float:
    if taker_maker == True:
        comission = sv.settings.amount /100 * sv.settings.taker_fee
    else:
        comission = sv.settings.amount /100 * sv.settings.maker_fee

    if open_price != 0:
        coins = sv.settings.amount / open_price
        profit_or_loss = 0
        isProf = None

        sell_pr = coins * close_price
        pr =  sv.settings.amount - sell_pr
        profit_or_loss = abs(pr)
        if buy:
            if open_price < close_price:
                isProf = True
                profit_or_loss -= comission
            elif close_price <= open_price:
                isProf = False
                profit_or_loss += comission
        else:
            if open_price <= close_price:
                isProf = False
                profit_or_loss += comission
            elif close_price < open_price:
                isProf = True
                profit_or_loss -= comission
        
        if isProf and profit_or_loss>0:
            return abs(round(profit_or_loss, 4))
        elif not isProf or profit_or_loss<0:
            return -abs(round(profit_or_loss, 4))#-abs(round(serv.spread_imitation(profit_or_loss), 4))
    else: return 0

def process_profit(dt: dict, is_first_iter: bool):

    taker = False if 'ham_60c' in sv.signal.type_os_signal or sv.settings.coin in coins.usdc_set else True
    if dt['type_close'] == 'timefinish':
        taker = True
    buy = True if sv.signal.signal == 1 else False
    prof = profit_counter(taker, dt['price_open'], buy, dt['price_close'])

    saldo = 0
    if is_first_iter == True and len(dt['profit_list'])==0:
        saldo = prof
    elif is_first_iter == False and len(dt['profit_list'])==1:
        saldo = dt['profit_list'][-1]['saldo']+prof
    else:
        saldo = dt['profit_list'][-1]['saldo']+prof

    position = {
        'open_time': dt['open_time'],
        'close_time': float(dt['cand_close'][0]),
        'signal': sv.signal.signal,
        'profit': prof,
        'coin': sv.settings.coin,
        'saldo': saldo,
        'type_close': dt['type_close'],
        'data_s': sv.signal.data,
        'type_of_signal': sv.signal.type_os_signal,
        'volume': round(sv.signal.volume, 4),
    }
    if validate_position(position):
        dt['profit_list'].append(position)
    # else:
    #     print('Invalid position')
    # dt['profit_list'].append(position)
    
    return position

def validate_position(position):
    required_keys = ['open_time', 'close_time', 'signal', 'profit', 'coin', 'saldo', 'type_close', 'data_s', 'type_of_signal', 'volume']
    required_types = [float, float, int, float, str, float, str, int, str, float]

    for key, required_type in zip(required_keys, required_types):
        if key not in position:
            print(f'Key {key} is missing in position')
            return False
        if not isinstance(position[key], required_type):
            print(f'Invalid type for {key}. Expected {required_type}, got {type(position[key])}')
            return False

    return True