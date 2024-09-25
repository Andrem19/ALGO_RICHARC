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
import predict as prd



def get_signal(i_1, data_1, settings: Settings):
    koff = 1
    was_pos_before = 0
    if sv.ham_60c_triger > 0:
        sv.ham_60c_triger-=1
    op5, hi5, lo5, cl5 = None, None, None, None
    op2, hi2, lo2, cl2 = None, None, None, None
    sv.signal.signal = 3

    if sv.long_counter >= 1:
        sv.long_counter+=1
    
    lenth = 210
    # btc_rsi = util.get_previous_day_rsi(data_1[i_1][0], sv.btc_rsi_dict)
    # print(btc_rsi)
    # if btc_rsi>48 and btc_rsi<62:
    #     return
    closes_1 = data_1[i_1-lenth:i_1, 4]
    highs_1 = data_1[i_1-lenth:i_1, 2]
    lows_1 = data_1[i_1-lenth:i_1, 3]
    opens_1 = data_1[i_1-lenth:i_1, 1]
    

    signal_1 = 3
    
    rsi_1 = talib.RSI(closes_1, 22)#22
    # btc_rsi = [50]
    # btc_index = util.get_candel_index(data_1[i_1][0], sv.btc_cand_dict)
    # if btc_index != -1:
    #     btc_closes = sv.btc_data[btc_index-210:btc_index, 4]
    #     btc_rsi = talib.RSI(btc_closes, 14)
    # if settings.coin == 'ETHUSDT':
    #     pos = {'open_time': data_1[i_1][0]}
    #     pos_list = util.filter_dicts(sv.etalon_positions, pos, 40, 0, tp='close_time')
    #     types_7 = [val['type_of_signal'] for val in pos_list if val['type_of_signal'] != 'ham_60c']
    #     if len(types_7)>7:
    #         sv.long_counter = 1

    # if sv.long_counter == 25 and settings.coin == 'ETHUSDT':
    #     sv.signal.type_os_signal = 'long_1'
    #     sv.settings.init_stop_loss = 0.02#serv.set_stls(0.020, abs(vol_can))#0.004
    #     sv.settings.target_len = 200#5
    #     sv.settings.amount = 200#20
    #     signal_1 = 1
    #     sv.long_counter = 0

    


    if settings.coin in coins.usdc_set:
        #==================USDC===========================
        if signal_1 == 3:
            if rsi_1[-1]<19:#18
                if closes_1[-1] > opens_1[-1]:
                    if tools.check_high_candel(highs_1[-1], lows_1[-1], 0.018*koff, settings.coin):
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
                                if tools.check_high_candel(hi5[-1], lo5[-1], 0.026*koff, settings.coin): #28#
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
                        if tools.check_high_candel(hi2[-1], lo2[-1], 0.016*koff, settings.coin):
                            low_tail, high_tail, body = tools.get_tail_body(op2[-1], hi2[-1], lo2[-1], cl2[-1])
                            if low_tail < body*1:
                                sv.signal.type_os_signal = 'ham_usdc'
                                sv.settings.init_stop_loss = 0.006
                                sv.settings.target_len = 5#5
                                sv.settings.amount = 20#20
                                signal_1 = 1
        
        if signal_1 == 3:
            if closes_1[-1]>opens_1[-1]:
                rsi_1 = talib.RSI(closes_1, 14)
                koff = 0.0032
                if rsi_1[-1]<35:
                    vol_can_1 = util.calculate_percent_difference(closes_1[-2], opens_1[-1])
                    vol_can_2 = util.calculate_percent_difference(closes_1[-3], opens_1[-2])
                    if ((vol_can_1 < -koff or vol_can_1 > koff) or (vol_can_2 < -koff or vol_can_2 > koff)):
                        sv.signal.type_os_signal = 'ham_usdc_1'
                        sv.settings.init_stop_loss = 0.006
                        sv.settings.target_len = 20#5
                        sv.settings.amount = 20
                        signal_1 = 1
        
        # if signal_1 == 3:
        #     if closes_1[-1] < opens_1[-1]:
        #         rsi_1 = talib.RSI(closes_1, 14)
        #         op15, hi15, lo15, cl15 = tools.convert_timeframe(opens_1, highs_1, lows_1, closes_1, 15, 2)
        #         if rsi_1[-1]<16 and tools.check_high_candel(hi15[-1], lo15[-1], 0.026*koff, sv.settings.coin):
        #             if tools.rsi_repeater(rsi_1[-60:], 5, 0, 46)>5:
        #                 # if not tools.check_high_candel(closes_1[-2], lows_1[-2], 0.018, settings.coin) or closes_1[-2]>opens_1[-2] or closes_1[-1]>opens_1[-1]:
        #                 sv.signal.type_os_signal = 'ham_60c'
        #                 sv.settings.init_stop_loss = 0.006
        #                 sv.settings.target_len = 20#5
        #                 sv.settings.amount = 20
        #                 signal_1 = 1

        
        
        # if signal_1 == 3:
        #     low_tail, high_tail, body = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
        #     if low_tail>body*0.1:
        #         op3, hi3, lo3, cl3 = tools.convert_timeframe(opens_1, highs_1, lows_1, closes_1, 3, 0)
        #         rsi_1 = talib.RSI(cl3, 14)
        #         if rsi_1[-1]<22 and tools.check_high_candel(hi3[-1], lo3[-1], 0.018, sv.settings.coin):#18
        #             if rsi_1[-3] < rsi_1[-4] and rsi_1[-2] < rsi_1[-3] and rsi_1[-1]> rsi_1[-2]:
        #                 sv.signal.type_os_signal = 'ham_60cc'
        #                 sv.settings.init_stop_loss = 0.006
        #                 sv.settings.target_len = 20#5
        #                 sv.settings.amount = 20
        #                 signal_1 = 1

    else:
        #==================USDT===========================
        if signal_1 == 3:
            if rsi_1[-1]<19:#18
                if closes_1[-1]>opens_1[-1]:
                    if tools.check_high_candel(highs_1[-1], lows_1[-1], 0.02*koff, settings.coin):
                        low_tail, high_tail, body = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
                        if high_tail < body*1:
                            low_tail, high_tail, body = tools.get_tail_body(opens_1[-2], highs_1[-2], lows_1[-2], closes_1[-2])
                            if high_tail < body*1:
                                sv.signal.type_os_signal = 'ham_1a'
                                sv.settings.init_stop_loss = 0.005#serv.set_stls(0.020, abs(vol_can))#0.004
                                sv.settings.target_len = 5#5
                                sv.settings.amount = 20#20
                                signal_1 = 1

        if rsi_1[-1]<40 and signal_1 == 3:
            if closes_1[-1]>opens_1[-1]:
                if tools.all_True_any_False(closes_1, opens_1, 5, 'all', True, 3):
                    low_tail, high_tail, body = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
                    if high_tail < body*1:#5 3
                        low_tail, high_tail, body = tools.get_tail_body(opens_1[-2], highs_1[-2], lows_1[-2], closes_1[-2])
                        if high_tail < body*1.5:#5 3
                            if cl5 is None:
                                op5, hi5, lo5, cl5 = tools.convert_timeframe(opens_1, highs_1, lows_1, closes_1, 5, 0)
                            rsi = talib.RSI(cl5, 20)#20
                            if rsi[-1]<18:
                                low_tail, high_tail, body = tools.get_tail_body(op5[-1], hi5[-1], lo5[-1], cl5[-1])
                                if low_tail < body*0.4:
                                    if tools.check_high_candel(hi5[-1], lo5[-1], 0.028*koff, settings.coin): #28#
                                        signal_1 = 1
                                        sv.settings.init_stop_loss = 0.005 #0.004
                                        sv.settings.target_len = 7#7
                                        sv.settings.amount = 20#20
                                        sv.signal.type_os_signal = 'ham_5a'
        
        if signal_1 == 3:
            if rsi_1[-1]<20:# or sv.rsi_was_low10>0:#20
                if closes_1[-1]>opens_1[-1]:
                    low_tail, high_tail, body = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
                    if high_tail < body*1:
                        low_tail, high_tail, body = tools.get_tail_body(opens_1[-2], highs_1[-2], lows_1[-2], closes_1[-2])
                        if high_tail < body*1.5:
                            if op5 is None:
                                op5, hi5, lo5, cl5 = tools.convert_timeframe(opens_1, highs_1, lows_1, closes_1, 5, 0)
                            rsi = talib.RSI(cl5, 26)
                            if rsi[-1]<18: #24
                                low_tail, high_tail, body = tools.get_tail_body(op5[-1], hi5[-1], lo5[-1], cl5[-1])
                                if low_tail > body*0.4 and low_tail < body*0.8:
                                    if tools.check_high_candel(hi5[-1], lo5[-1], 0.028*koff, settings.coin): #28
                                        signal_1 = 1
                                        sv.settings.init_stop_loss = 0.004 #0.004
                                        sv.settings.target_len = 7#5
                                        sv.settings.amount = 20#20
                                        sv.signal.type_os_signal = 'ham_5b'

        if signal_1 == 3:
            if rsi_1[-1]<36:
                if closes_1[-1]<opens_1[-1]:
                    if op2 is None:
                        op2, hi2, lo2, cl2 = tools.convert_timeframe(opens_1, highs_1, lows_1, closes_1, 2, 30)
                    rsi_2 = talib.RSI(cl2, 14)#16
                    if rsi_2[-1]<14:
                        if tools.check_high_candel(hi2[-1], lo2[-1], 0.030, settings.coin):#0.026
                            if tools.check_rise(hi2, lo2, 5, 4, 'bigger') and tools.last_lowest(lows_1, 40):# and tools.all_True_any_False(closes_1, opens_1, 2, 'all', True):
                                low_tail, high_tail, body = tools.get_tail_body(op2[-1], hi2[-1], lo2[-1], cl2[-1])
                                if not tools.check_high_candel(closes_1[-2], lows_1[-2], 0.018*koff, settings.coin) and low_tail < body*0.6 and low_tail > body*0.1 and not tools.has_smaller(rsi_2, rsi_2[-1], 'smaller'):
                                    sv.signal.type_os_signal = 'stub'# 'ham_1by'
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
            if closes_1[-1]>opens_1[-1]:
                low_tail_1, high_tail_1, body_1 = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
                if  high_tail_1 < body_1*1:
                    if op2 is None:
                        op2, hi2, lo2, cl2 = tools.convert_timeframe(opens_1, highs_1, lows_1, closes_1, 2, 30)
                    rsi = talib.RSI(cl2, 22)#22
                    if rsi[-1]<20:#18
                        if tools.check_high_candel(hi2[-1], lo2[-1], 0.022*koff, settings.coin):
                            low_tail, high_tail, body = tools.get_tail_body(op2[-1], hi2[-1], lo2[-1], cl2[-1])
                            if low_tail < body*1:
                                sv.signal.type_os_signal = 'ham_2a'
                                sv.settings.init_stop_loss = 0.005
                                sv.settings.target_len = 5#5
                                sv.settings.amount = 20#20
                                signal_1 = 1
        
        if signal_1 == 3:
            if closes_1[-1]>opens_1[-1]:
                rsi = talib.RSI(closes_1, 22)#22
                if rsi[-1]>70:
                    if tools.check_high_candel(highs_1[-1], lows_1[-1], 0.015*koff, settings.coin):
                        sv.signal.type_os_signal = 'long_1'
                        sv.settings.init_stop_loss = 0.005
                        sv.settings.target_len = 5#5
                        sv.settings.amount = 20#20
                        signal_1 = 2

        # if signal_1 == 3:
        #     rsi_1 = talib.RSI(closes_1, 14)
        #     if closes_1[-1]>opens_1[-1] and closes_1[-2]<opens_1[-2]:
        #         koff = 0.003
        #         if rsi_1[-1]<22:
        #             vol_can_1 = util.calculate_percent_difference(closes_1[-2], opens_1[-1])
        #             vol_can_2 = util.calculate_percent_difference(closes_1[-3], opens_1[-2])
        #             if ((vol_can_1 < -koff or vol_can_1 > koff) or (vol_can_2 < -koff or vol_can_2 > koff)):
        #                 sv.signal.type_os_signal = 'ham_brg'
        #                 sv.settings.init_stop_loss = 0.006
        #                 sv.settings.target_len = 20#5
        #                 sv.settings.amount = 20
        #                 signal_1 = 1

    if signal_1 in sv.settings.s:

        

        sv.signal.signal = signal_1
        # if sv.signal.type_os_signal == 'long_1':
        #     # index = util.find_index(data_1[i_1][0], sv.btc_data)
        #     # if index < 960:
        #     #     sv.signal.signal = 3
        #     #     return
        #     # btc_lows = sv.btc_data[index-960:index, 3]

        #     # rnl = tools.range_not_lowest(btc_lows, 940, 20)
        #     # if rnl:
        #     #     sv.signal.signal = 3
        #     #     return
        #     sv.signal.volume = abs(util.calculate_percent_difference(highs_1[-3], lows_1[-1]))
        #     sv.signal.index = i_1
        #     sv.signal.data = 1
        #     return
        # sv.long_counter = 0

        sv.signal.data = 1
        pos = {'open_time': data_1[i_1][0]}
        pos_list = util.filter_dicts(sv.etalon_positions, pos, 15, 5)
        types_7 = [val['type_of_signal'] for val in pos_list]
        if ('ham_1a' in types_7 or 'ham_2a' in types_7 or 'ham_5b' in types_7 or 'ham_5a' in types_7) and len(types_7)>0:
            if sv.signal.type_os_signal in ['ham_1a', 'ham_2a']:
                sv.signal.data = 5
                sv.settings.init_stop_loss = 0.05
                sv.settings.target_len = 7#20
        
        # pos_list = util.filter_dicts(sv.etalon_positions, pos, 40, 0, tp='close_time')
        # types_7 = [val['type_of_signal'] for val in pos_list if val['type_of_signal'] != 'ham_60c']
        # if len(types_7)>5:
        #     sv.long_counter = 1
        sv.was_pos_before = len(types_7)

        if 'ham_60c' == sv.signal.type_os_signal:
            pos_list = util.filter_dicts(sv.etalon_positions, pos, 5, 0)
            low_tail, high_tail, body = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
            # res = util.at_time_position_opened(sv.unfiltered_positions, data_1[i_1][0])
            if closes_1[-1]> opens_1[-1]:
                sv.settings.amount = 30
            elif len(pos_list)>0:
                sv.settings.amount = 20
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
            # positions_openes_at_time = util.at_time_position_opened(sv.unfiltered_positions, data_1[i_1][0])
            if ('ham_1a' in types_7 or 'ham_2a' in types_7 or 'ham_5b' in types_7):# or res >15:
                sv.signal.type_os_signal = 'stub'
                sv.settings.target_len = 3

        
        # if  sv.signal.data != 5:#sv.signal.type_os_signal == 'ham_60c': #
        #     index = util.find_index(data_1[i_1][0], sv.btc_data_1)
        #     if index is not None and index > 200:
        #         sample_2 = sv.btc_data_1[index-200:index]

        #         last_cand = util.combine_last_candle(sv.btc_data_1[index][0], data_1[i_1][0], sv.btc_data_2)
        #         if last_cand is not None:
        #             sample_2 = np.append(sample_2, [last_cand], axis=0)

        #         index = util.find_index(data_1[i_1][0], sv.btc_data_3)
        #         if index is not None and index>90:
        #             sample_3 = sv.btc_data_3[index-90:index]
                
                
        #             last_cand_3 = util.combine_last_candle(sv.btc_data_3[index][0], data_1[i_1][0], data_1)
        #             if last_cand_3 is not None:
        #                 sample_3 = np.append(sample_3, [last_cand_3], axis=0)

                    
        #             prediction_1 = prd.predict_image_class(sv.model_1, 3, data_1[i_1-60:i_1], sample_2[-100:], None, 2)
        #             prediction_2 = prd.predict_image_class(sv.model_2, 1, data_1[i_1-60:i_1], sample_2, None, 2)
        #             prediction_3 = prd.predict_image_class(sv.model_3, 3, data_1[i_1-25:i_1], sample_2[-100:], sample_3, 3)

        #             lst = [prediction_1, prediction_2, prediction_3]

        #             most_common = max(lst, key=lst.count)

                    # if all(l for l in lst):
                    #     sv.settings.amount *= 2
                    # elif most_common:
                    #     pass

                    # if not most_common:
                    #     sv.signal.signal = 3
                    #     return
                    #     sv.signal.signal = 1
                    #     sv.signal.type_os_signal = 'long_1'
                    #     sv.settings.target_len = 60#4
                    #     sv.settings.init_stop_loss = 0.03
                    #     sv.settings.take_profit = 0.03
                    #     return
        
        # if sv.signal.type_os_signal in ['ham_1a', 'ham_2a', 'ham_5a', 'ham_5b']:
        #     positions_openes_at_time = util.at_time_position_opened(sv.unfiltered_positions, data_1[i_1][0])
        #     pos_types = [val['type_of_signal'] for val in positions_openes_at_time]
        #     if len(pos_types)>5:
        #         if sum(1 for p in pos_types if p == 'ham_60c') > 3:
        #             sv.signal.type_os_signal = 'stub'
        #             sv.settings.target_len = 3

        # pos_list = util.filter_dicts(sv.etalon_positions, pos, 5, 0, 'close_time')
        # res = util.at_time_position_opened(sv.unfiltered_positions, data_1[i_1][0])

        # if len(pos_list)>0:
        #     if all(p['open_time']==p['close_time'] for p in pos_list) or all(p['profit']<0 for p in pos_list):
        #         sv.settings.amount*=0.5
        #     elif any(p['profit']>0 for p in pos_list):
        #         sv.settings.amount*=2

        # if tools.check_high_candel(closes_1[-2], lows_1[-2], 0.018, settings.coin) and closes_1[-2]<opens_1[-2] and closes_1[-1]<opens_1[-1]:
        #     sv.signal.type_os_signal = 'stub'
        #     sv.settings.target_len = 3

        # if 'ham_60cc' == sv.signal.type_os_signal:
        #     sv.signal.type_os_signal = 'ham_60c'
        #     pos_list = util.filter_dicts(sv.etalon_positions, pos, 10, 0)
        #     if len(pos_list)>0:
        #         sv.signal.type_os_signal = 'stub'
        #         sv.settings.target_len = 3


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