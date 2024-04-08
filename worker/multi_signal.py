from models.settings import Settings
import helpers.util as util
from models.signal import Signal
import helpers.tools as tools
import statsmodels.api as sm
import talib
import numpy as np
import helpers.util as util
import shared_vars as sv

def get_signal(i_1, data_1, settings: Settings):

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
    if rsi_1[-1]<40 and signal_1 == 3:
        if closes_1[-1] > opens_1[-1]:
            op5, hi5, lo5, cl5 = tools.convert_timeframe(opens_1, highs_1, lows_1, closes_1, 5, 0)
            rsi = talib.RSI(cl5, 20)#20
            if rsi[-1]<18: #24
                low_tail, high_tail, body = tools.get_tail_body(op5[-1], hi5[-1], lo5[-1], cl5[-1])
                if low_tail < body*0.4:
                    if tools.check_high_candel(hi5[-1], lo5[-1], 0.028, settings.coin): #28#
                        low_tail, high_tail, body = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
                        if high_tail < body*1:
                            signal_1 = 1
                            sv.settings.init_stop_loss = 0.005 #0.004
                            sv.settings.target_len = 7#5
                            sv.settings.amount = 20#20
                            sv.signal.type_os_signal = 'ham_5a'
    
    

    if rsi_1[-1]<19:#18
        if tools.check_high_candel(highs_1[-1], lows_1[-1], 0.02, settings.coin) and closes_1[-1] > opens_1[-1]:
            low_tail, high_tail, body = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
            if high_tail < body*1:
                sv.signal.type_os_signal = 'ham_1a'
                sv.settings.init_stop_loss = 0.005#serv.set_stls(0.020, abs(vol_can))#0.004
                sv.settings.target_len = 5#5
                sv.settings.amount = 20#20
                signal_1 = 1

    if signal_1 == 3:
        if rsi_1[-1]<20:#20
            if closes_1[-1] > opens_1[-1]:
                if op5 is None:
                    op5, hi5, lo5, cl5 = tools.convert_timeframe(opens_1, highs_1, lows_1, closes_1, 5, 0)
                rsi = talib.RSI(cl5, 26)
                if rsi[-1]<18: #24
                    low_tail, high_tail, body = tools.get_tail_body(op5[-1], hi5[-1], lo5[-1], cl5[-1])
                    if low_tail > body*0.4 and low_tail < body*0.8:
                        if tools.check_high_candel(hi5[-1], lo5[-1], 0.028, settings.coin): #28
                            low_tail, high_tail, body = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
                            if high_tail < body*1:
                                signal_1 = 1
                                sv.settings.init_stop_loss = 0.004 #0.004
                                sv.settings.target_len = 7#5
                                sv.settings.amount = 20#20
                                sv.signal.type_os_signal = 'ham_5b'

    if signal_1 == 3:
        rsi_1 = talib.RSI(closes_1, 14)#14
        if rsi_1[-1]<14:#18
            if tools.check_high_candel(closes_1[-2], opens_1[-2], 0.015, settings.coin) and closes_1[-2] < opens_1[-2]:
                low_tail, high_tail, body = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
                if closes_1[-1] > lows_1[-2]:
                    if high_tail < body*2 and low_tail> body*1:
                        sv.signal.type_os_signal = 'ham_1bz'
                        sv.settings.init_stop_loss = 0.006#6
                        sv.settings.target_len = 4#4
                        sv.settings.amount = 20#20
                        signal_1 = 1

    if signal_1 == 3:
        if rsi_1[-1]<36:
            op2, hi2, lo2, cl2 = tools.convert_timeframe(opens_1, highs_1, lows_1, closes_1, 2, 0)
            rsi_2 = talib.RSI(cl2, 14)#16
            if rsi_2[-1]<14:#18
                if tools.check_high_candel(hi2[-1], lo2[-1], 0.026, settings.coin) and closes_1[-1]<opens_1[-1]:#0.028
                    if tools.check_rise(hi2, lo2, 5, 4, 'bigger') and tools.last_lowest(lows_1, 40):
                        low_tail, high_tail, body = tools.get_tail_body(op2[-1], hi2[-1], lo2[-1], cl2[-1])
                        if low_tail < body*0.6 and low_tail > body*0.1:
                            sv.signal.type_os_signal = 'ham_1by'
                            sv.settings.init_stop_loss = 0.006#6
                            sv.settings.target_len = 4#4
                            sv.settings.amount = 20#20
                            signal_1 = 1
                        elif low_tail <= body*0.1:
                            sv.signal.type_os_signal = 'stub'
                            sv.settings.init_stop_loss = 0.006#6
                            sv.settings.target_len = 2
                            sv.settings.amount = 1#20
                            signal_1 = 1

    if signal_1 == 3:
        rsi_1 = talib.RSI(closes_1, 14)
        if rsi_1[-1]<18:#18
            if tools.check_high_candel(closes_1[-1], opens_1[-1], 0.02, settings.coin) and closes_1[-1] < opens_1[-1]:
                if tools.last_lowest(lows_1, 40) and tools.check_rise(highs_1, lows_1, 5, 4, 'bigger'):
                    low_tail, high_tail, body = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
                    if low_tail > body*0.6 and low_tail < body*1.6:
                        if tools.all_True_any_False(closes_1, opens_1, 4, 'any', False):
                            sv.signal.type_os_signal = 'ham_1bx'
                            sv.settings.init_stop_loss = 0.004#4
                            sv.settings.target_len = 4#4
                            sv.settings.amount = 20#20
                            signal_1 = 1

    if signal_1 == 3:
        if closes_1[-1] > opens_1[-1]:
            low_tail_1, high_tail_1, body_1 = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
            if  high_tail_1 < body_1*1:
                if op2 is None:
                    op2, hi2, lo2, cl2 = tools.convert_timeframe(opens_1, highs_1, lows_1, closes_1, 2, 0)
                rsi = talib.RSI(cl2, 22)#22
                if rsi[-1]<20:#18
                    if tools.check_high_candel(hi2[-1], lo2[-1], 0.022, settings.coin):
                        low_tail, high_tail, body = tools.get_tail_body(op2[-1], hi2[-1], lo2[-1], cl2[-1])
                        if low_tail < body*1:
                            sv.signal.type_os_signal = 'ham_2a'
                            sv.settings.init_stop_loss = 0.005
                            sv.settings.target_len = 5#5
                            sv.settings.amount = 20#20
                            signal_1 = 1

    if signal_1 in sv.settings.s:
        sv.signal.volume = abs(util.calculate_percent_difference(highs_1[-3], lows_1[-1]))
        sv.signal.signal = signal_1
        sv.signal.data = 1
        sv.signal.index = i_1
        return

    sv.signal.signal = 3
    return