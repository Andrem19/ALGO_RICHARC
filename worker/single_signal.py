from models.signal import Signal
import helpers.tools as tools
import talib
import numpy as np
import helpers.util as util
import shared_vars as sv

def get_signal(i, data):
    ln = 210
    closes = data[i-ln:i, 4]
    highs = data[i-ln:i, 2]
    lows = data[i-ln:i, 3]
    opens = data[i-ln:i, 1]
    # volume = data[i-sv.settings.chunk_len*2:i, 5]
    sg = 3

    #=================START LOGIC===================
    
    if sg == 3:
        rsi_1 = talib.RSI(closes, 22)
        if rsi_1[-1]<30 and rsi_1[-1]>19:#18
            if tools.check_high_candel(opens[-1], closes[-1], 0.018, sv.settings.coin):
                low_tail, high_tail, body = tools.get_tail_body(opens[-1], highs[-1], lows[-1], closes[-1])
                if high_tail > body*1:
                    # vol_can1 = util.calculate_percent_difference(highs[-1], lows[-1])
                    # vol_can2 = util.calculate_percent_difference(highs[-2], lows[-2])
                    # vol_can3 = util.calculate_percent_difference(highs[-3], lows[-3])
                    # if vol_can1*1.5<vol_can2*1.2<vol_can3:
                    if closes[-1]>opens[-1]:
                        sv.signal.type_os_signal = 'ham_1aa'
                        sv.settings.init_stop_loss = 0.005#serv.set_stls(0.020, abs(vol_can))#0.004
                        sv.settings.target_len = 3#5
                        sv.settings.amount = 20#20 
                        sg = 1


    #=================END LOGIC=====================

    if sg in sv.settings.s:
        sv.signal.signal = sg
        sv.signal.data = sv.settings.time
        sv.settings.init_stop_loss = 0.004 #0.004
        sv.settings.target_len = 3#3
        sv.settings.amount = 20#20
        sv.signal.type_os_signal = 'ham_1aa'
        sv.signal.volume = abs(util.calculate_percent_difference(highs[-3], lows[-1]))
        sv.signal.data = 1
        sv.signal.index = i
    else:
        sv.signal.signal = 3
