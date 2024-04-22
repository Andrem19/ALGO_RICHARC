from models.signal import Signal
import helpers.tools as tools
import talib
import numpy as np
import helpers.util as util
import shared_vars as sv
from datetime import datetime

def get_signal(i, data):
    try:

        ln = 225
        # i_60 = util.get_candel_index(data[i][0], sv.candel_dict[60])
        

        # if i_60 != -1:
        #     sv.prev_index[60] = i_60
        # else:
        #     i_60 = sv.prev_index[60]

        # if i_60<60:
        #     sv.signal.signal = 3
        #     return

        # ln_60 = 60
        
        # closes_60 = sv.data[60][i_60-ln_60:i_60, 4]
        # highs_60 = sv.data[60][i_60-ln_60:i_60, 2]
        # lows_60 = sv.data[60][i_60-ln_60:i_60, 3]
        # opens_60 = sv.data[60][i_60-ln_60:i_60, 1]

        closes = data[i-ln:i, 4]
        highs = data[i-ln:i, 2]
        lows = data[i-ln:i, 3]
        opens = data[i-ln:i, 1]
        # volume = data[i-sv.settings.chunk_len*2:i, 5]
        sg = 3
        #=================START LOGIC===================
        
        # low_tail, high_tail, body = tools.get_tail_body(opens_60[-1], highs_60[-1], lows_60[-1], closes_60[-1])
        # low_tail_15, high_tail_15, body_15 = tools.get_tail_body(opens[-1], highs[-1], lows[-1], closes[-1])
        # if low_tail<high_tail:
        #     if tools.last_lowest(lows, 15) and tools.last_lowest(lows_60, 15):
        #         if tools.check_rise(highs_60, lows_60, 4, 2, 'less') and tools.check_rise(highs, lows, 4, 2, 'less'):
        #             if tools.check_high_candel(highs[-1], lows[-1], 0.02, sv.settings.coin):
        #                 sg = 1
        # sg, targ_len, st_ls = sv.reactor.call(sg, opens, highs, lows, closes, opens_60, highs_60, lows_60, closes_60)
        # if tools.check_high_candel(opens[-1], closes[-1], 0.03, sv.settings.coin):
        #     if tools.last_lowest(lows_60, 10):
        #         if tools.last_close_higher(highs, lows, closes, 'lower', 'high'):
        #             if tools.check_rise(highs, lows, 3,0.5, 'bigger'):
        #                 if tools.open_close(opens[-1], closes[-1], 'lower'):
        #                     if tools.open_close(opens_60[-1], closes_60[-1], 'lower'):
        #                         sg = 1

        # if tools.check_high_candel(opens[-2], closes[-1], 0.03, sv.settings.coin):
        #     if tools.last_lowest(lows_60, 10) and tools.last_lowest(lows, 10):
        #         rsi = talib.RSI(closes_60, 22)
        #         if rsi[-1]>30 and tools.all_True_any_False(closes_60, opens_60, 4, 'any', False):
        #             low_tail, high_tail, body = tools.get_tail_body(opens_60[-1], highs_60[-1], lows_60[-1], closes_60[-1])
        #             if high_tail<body*2:
        #                 low_tail, high_tail, body = tools.get_tail_body(opens_60[-2], highs_60[-2], lows_60[-2], closes_60[-2])
        #                 if high_tail<body*2:
        #                     low_tail, high_tail, body = tools.get_tail_body(opens[-1], highs[-1], lows[-1], closes[-1])
        #                     if low_tail<body*0.4 and high_tail<body*0.4:
        #                         sg = 1
        
        rsi_1 = talib.RSI(closes, 14)
        if rsi_1[-1]<16:
            op15, hi15, lo15, cl15 = tools.convert_timeframe(opens, highs, lows, closes, 15, 2)
            # op5, hi5, lo5, cl5 = tools.convert_timeframe(opens, highs, lows, closes, 5, 2)
            # op2, hi2, lo2, cl2 = tools.convert_timeframe(opens, highs, lows, closes, 5, 2)
            # if tools.check_high_candel(hi2[-1], lo2[-1], 0.024, sv.settings.coin):# vol>0.03:
            #     if sum(1 for r in rsi_1[-70:] if r<28)>15 and closes[-1]<opens[-1]:#28 15
                # if sum(1 for o, h, l, c in zip(opens[-15:], highs[-10:], lows[-10:], closes[-10:]) if tools.low_high_tails(o,h,l,c,'high', 'bigger', 1))<4:
                # tools.check_high_candel(hi15[-1], lo15[-1], 0.026, sv.settings.coin) or 
            if tools.check_high_candel(hi15[-1], lo15[-1], 0.026, sv.settings.coin):# any(o>c and tools.check_high_candel(h, l, 0.026, sv.settings.coin) for o, h, l ,c in zip(op15, hi15, lo15, cl15)):
                # if sum(1 for o, h, l, c in zip(opens[-10:], highs[-10:], lows[-10:], closes[-10:]) if o>c)<8:
                # if not tools.last_highest(highs_60, 24):
                if tools.rsi_repeater(rsi_1[-60:], 5, 0, 46)>5:
                    sg = 1
        #=================END LOGIC=====================

        if sg in sv.settings.s:
            sv.settings.amount = 20#20
            if lows[-2]<lows[-1]:
                sv.settings.amount = 40
            sv.signal.signal = sg
            # pos = {'open_time': data[i][0]}
            # pos_list = util.filter_dicts(sv.etalon_positions, pos, 60, 1)
            # types_7 = [val['type_of_signal'] for val in pos_list]
            # if len(types_7)>1:
            #     # sv.settings.amount*=0.5
            #     sv.signal.signal = 3
            #     return
            sv.signal.data = sv.settings.time
            sv.settings.init_stop_loss = 0.006#0.004
            sv.settings.target_len = 60#3
            sv.signal.type_os_signal = 'ham_60c'
            sv.signal.volume = abs(util.calculate_percent_difference(highs[-3], lows[-1]))
            sv.signal.data = 1
            sv.signal.index = i
        else:
            sv.signal.signal = 3
    except Exception as e:
        print(e, i)
