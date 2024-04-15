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
        if closes[-1]>opens[-1]:
            pos = {'open_time': data[i][0]}
            types_10, types_5 = util.filter_dicts_signal(sv.etalon_positions, pos)
            # types_10 = [val['type_of_signal'] for val in types_10]
            # types_5 = [val['type_of_signal'] for val in types_5]
            if len(types_10)>10 and len(types_5)<1:
                sg = 1


    #=================END LOGIC=====================

    if sg in sv.settings.s:
        sv.signal.signal = sg
        sv.signal.data = sv.settings.time
        sv.settings.init_stop_loss = 0.03 #0.004
        sv.settings.target_len = 240#3
        sv.settings.amount = 20#20
        sv.signal.type_os_signal = 'ham_1a'
        sv.signal.volume = abs(util.calculate_percent_difference(highs[-3], lows[-1]))
        sv.signal.data = 1
        sv.signal.index = i
    else:
        sv.signal.signal = 3
