from models.settings import Settings
import helpers.util as util
from models.signal import Signal
import helpers.tools as tools
import statsmodels.api as sm
import talib
import coins
import numpy as np
import helpers.util as util
import shared_vars as sv

def get_signal(i_1, data_1, settings: Settings):
    if sv.ham_60c_triger > 0:
        sv.ham_60c_triger-=1
    op5, hi5, lo5, cl5 = None, None, None, None
    op2, hi2, lo2, cl2 = None, None, None, None
    sv.signal.signal = 3
    
    lenth = 210

    closes_1 = data_1[i_1-lenth:i_1, 4]
    highs_1 = data_1[i_1-lenth:i_1, 2]
    lows_1 = data_1[i_1-lenth:i_1, 3]
    opens_1 = data_1[i_1-lenth:i_1, 1]
    

    signal_1 = 3
    
    rsi_1 = talib.RSI(closes_1, 22)#22
    if signal_1 == 3:
        if rsi_1[-1]<19:#18
            if closes_1[-1] > opens_1[-1]:
                if tools.check_high_candel(highs_1[-1], lows_1[-1], 0.02, settings.coin):
                    low_tail, high_tail, body = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
                    if high_tail < body*1:
                        low_tail, high_tail, body = tools.get_tail_body(opens_1[-2], highs_1[-2], lows_1[-2], closes_1[-2])
                        if high_tail < body*1:
                            sv.signal.type_os_signal = 'ham_usdc'
                            sv.settings.init_stop_loss = 0.01#serv.set_stls(0.020, abs(vol_can))#0.004
                            sv.settings.target_len = 5#5
                            sv.settings.amount = 20#20
                            signal_1 = 1

    if rsi_1[-1]<40 and signal_1 == 3:
        if closes_1[-1] > opens_1[-1]:
            if tools.all_True_any_False(closes_1, opens_1, 5, 'all', True, 3):
                low_tail, high_tail, body = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
                if high_tail < body*1:#5 3
                    if cl5 is None:
                        op5, hi5, lo5, cl5 = tools.convert_timeframe(opens_1, highs_1, lows_1, closes_1, 5, 0)
                    rsi = talib.RSI(cl5, 20)#20
                    if rsi[-1]<18:
                        low_tail, high_tail, body = tools.get_tail_body(op5[-1], hi5[-1], lo5[-1], cl5[-1])
                        if low_tail < body*0.4:
                            if tools.check_high_candel(hi5[-1], lo5[-1], 0.028, settings.coin): #28#
                                signal_1 = 1
                                sv.settings.init_stop_loss = 0.01 #0.004
                                sv.settings.target_len = 7#7
                                sv.settings.amount = 20#20
                                sv.signal.type_os_signal = 'ham_usdc'

    
    if signal_1 == 3:
        if closes_1[-1] > opens_1[-1]:
            low_tail_1, high_tail_1, body_1 = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
            if  high_tail_1 < body_1*1:
                if op2 is None:
                    op2, hi2, lo2, cl2 = tools.convert_timeframe(opens_1, highs_1, lows_1, closes_1, 2, 30)
                rsi = talib.RSI(cl2, 22)#22
                if rsi[-1]<20:#18
                    if tools.check_high_candel(hi2[-1], lo2[-1], 0.022, settings.coin):
                        low_tail, high_tail, body = tools.get_tail_body(op2[-1], hi2[-1], lo2[-1], cl2[-1])
                        if low_tail < body*1:
                            sv.signal.type_os_signal = 'ham_usdc'
                            sv.settings.init_stop_loss = 0.006
                            sv.settings.target_len = 5#5
                            sv.settings.amount = 20#20
                            signal_1 = 1
    
    # if signal_1 == 3:
    #     if closes_1[-1]>opens_1[-1]:
    #         rsi_1 = talib.RSI(closes_1, 14)
    #         koff = 0.0032
    #         if rsi_1[-1]<35:
    #             vol_can_1 = util.calculate_percent_difference(closes_1[-2], opens_1[-1])
    #             vol_can_2 = util.calculate_percent_difference(closes_1[-3], opens_1[-2])
    #             if ((vol_can_1 < -koff or vol_can_1 > koff) or (vol_can_2 < -koff or vol_can_2 > koff)):
    #                 sv.signal.type_os_signal = 'ham_usdc_1'
    #                 sv.settings.init_stop_loss = 0.006
    #                 sv.settings.target_len = 20#5
    #                 sv.settings.amount = 20
    #                 signal_1 = 1
    
    if signal_1 == 3:
        rsi_1 = talib.RSI(closes_1, 14)
        op15, hi15, lo15, cl15 = tools.convert_timeframe(opens_1, highs_1, lows_1, closes_1, 15, 2)
        if (rsi_1[-1]<16 and tools.check_high_candel(hi15[-1], lo15[-1], 0.032, sv.settings.coin)):
            if tools.rsi_repeater(rsi_1[-60:], 5, 0, 46)>5 and closes_1[-1]<opens_1[-1]:
                sv.signal.type_os_signal = 'ham_60c'
                sv.settings.init_stop_loss = 0.006
                sv.settings.target_len = 20#5
                sv.settings.amount = 20
                signal_1 = 1

    if signal_1 in sv.settings.s:
        sv.signal.signal = signal_1
        sv.signal.data = 1
        pos = {'open_time': data_1[i_1][0]}
        if 'ham_60c' == sv.signal.type_os_signal:
            pos_list = util.filter_dicts(sv.etalon_positions, pos, 5, 0)
            low_tail, high_tail, body = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
            if closes_1[-1]> opens_1[-1]:
                sv.settings.amount = 40
            elif len(pos_list)>0:
                sv.settings.amount = 30
            elif low_tail>body*1.5 or high_tail>body:
                sv.signal.type_os_signal = 'stub'
                sv.settings.target_len = 3
            elif low_tail<body*0.1 and closes_1[-1]<opens_1[-1]:
                sv.settings.amount = 5
            else:
                sv.settings.amount = 10

        if 'ham_60c' in sv.signal.type_os_signal:
            pos_list = util.filter_dicts(sv.etalon_positions, pos, 15, 0)
            types_7 = [val['type_of_signal'] for val in pos_list]
            if 'ham_1a' in types_7 or 'ham_2a' in types_7 or 'ham_5b' in types_7:
                sv.signal.type_os_signal = 'stub'
                sv.settings.target_len = 3

        sv.signal.volume = abs(util.calculate_percent_difference(highs_1[-3], lows_1[-1]))
        
        sv.signal.index = i_1
        return

    sv.signal.signal = 3
    return

def check_rsi(rsi, opens_1, closes_1):
    if rsi<6 and rsi > 0:
        if tools.all_True_any_False(closes_1, opens_1, 5, 'all', True, 3):
            return True
    
    return False