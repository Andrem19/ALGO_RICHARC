from models.signal import Signal
import helpers.tools as tools
import talib
import numpy as np
import helpers.util as util
import shared_vars as sv

def get_signal(i, data):

    closes = data[i-sv.settings.chunk_len*2:i, 4]
    highs = data[i-sv.settings.chunk_len*2:i, 2]
    lows = data[i-sv.settings.chunk_len*2:i, 3]
    opens = data[i-sv.settings.chunk_len*2:i, 1]
    # volume = data[i-sv.settings.chunk_len*2:i, 5]
    sg = 3

    #=================START LOGIC===================
    
    if sg == 3:
        if closes[-1]> opens[-1]:
            if tools.check_high_candel(highs[-1], lows[-1], 0.01, sv.settings.coin):# and tools.check_rise(highs, lows, 5, 4, 'bigger'):
                # low_tail, high_tail, body = tools.get_tail_body(opens[-1], highs[-1], lows[-1], closes[-1])
                # if low_tail> body*0.6:
                sg = 1



    #=================END LOGIC=====================

    if sg in sv.settings.s:
        sv.signal.signal = sg
        sv.signal.data = sv.settings.time
        sv.settings.init_stop_loss = 0.004 #0.004
        sv.settings.target_len = 2#3
        sv.settings.amount = 20#20
        sv.signal.type_os_signal = 'ham_2a'
    else:
        sv.signal.signal = 3
