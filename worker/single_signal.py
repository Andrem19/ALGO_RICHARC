from models.signal import Signal
import helpers.tools as tools
import talib
import numpy as np
import helpers.util as util
import shared_vars as sv
from datetime import datetime
import helpers.trend as tr
import predict as prd

def get_signal(i, data):
    try:
        if sv.long_counter >= 1:
            sv.long_counter+=1

        ln = 100
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

        # pos = {'open_time': data[i][0]}
        # pos_list = util.filter_dicts(sv.etalon_positions, pos, 30, 0, tp='close_time')
        # types_7 = [val['type_of_signal'] for val in pos_list]
        # if len(types_7)>10:
        #     sv.long_counter = 1

        # if sv.long_counter == 45 and sv.settings.coin == 'ETHUSDT':

        # sample = data[i-60:i]
        # index = util.find_index(data[i][0], sv.btc_data_1)
        # if index is not None and index > 60:
        #     sample_2 = sv.btc_data_1[index-60:index]
        #     last_cand = util.combine_last_candle(sv.btc_data_1[index][0], data[i][0], sv.btc_data_2)
            
        #     if last_cand is not None:
        #         sample_2 = np.append(sample_2, [last_cand], axis=0)
        #         index = util.find_index(data[i][0], sv.btc_data_3)
        #         if index is not None and index>60:
        #             sample_3 = sv.btc_data_3[index-60:index]
                    
        #             last_cand_3 = util.combine_last_candle(sv.btc_data_3[index][0], data[i][0], data)
        #             if last_cand_3 is not None:
        #                 sample_3 = np.append(sample_3, [last_cand_3], axis=0)
        prediction_1 = False
        prediction_2 = 0
        chunk = data[i-25:i]
        closes = data[i-100:i, 4]
        list_to_save = []
        # rsi = talib.RSI(closes)

        # index = util.find_index(data[i][0], sv.btc_data_1)
        # if index is not None and index > 25:
        #     last_cand = util.combine_last_candle(sv.btc_data_1[index][0], data[i][0], data)
        #     if last_cand is not None:
        #         sample_2 = sv.btc_data_1[index-24:index]
        #         sample_2 = np.append(sample_2, [last_cand], axis=0)
        #     else:
        #         sample_2 = sv.btc_data_1[index-25:index]

        #     for p in range(len(sample_2)):
        #         list_to_save.append(round(util.calculate_percent_difference(sample_2[p][1], sample_2[p][4])*100, 3))
        #         list_to_save.append(round(util.calculate_percent_difference(sample_2[p][1], sample_2[p][2])*100, 3))
        #         list_to_save.append(round(util.calculate_percent_difference(sample_2[p][1], sample_2[p][3])*100, 3))
        # index = util.find_index(data[i][0], sv.btc_data_1)
        trend = None
        # if index is not None and index >= 50:
        #     sample_2 = sv.btc_data_1[index-100:index]
        #     global_trend = tools.what_trend(sample_2[:, 4], 25, 1)
        #     if global_trend == 'up':
        #         sv.signal.signal = sg
        #         return
        index = util.find_index(data[i][0], sv.btc_data_1)
        global_trend = util.calculate_percent_difference(sv.btc_data_1[index-5][1], sv.btc_data_1[index-1][4])
        
        # global_trend = [x[1]<x[4] for x in sv.btc_data_1[index-5:index]]
        # true_count = global_trend.count(True)
        # false_count = global_trend.count(False)

        trend = tools.what_trend(closes[-25:], 5, 5)
        if trend != 'down' or global_trend>0:# or true_count > false_count:
            sv.signal.signal = sg
            return
        for j in range(len(chunk)):
            list_to_save.append(round(util.calculate_percent_difference(chunk[j][1], chunk[j][4])*100, 3))
            list_to_save.append(round(util.calculate_percent_difference(chunk[j][1], chunk[j][2])*100, 3))
            list_to_save.append(round(util.calculate_percent_difference(chunk[j][1], chunk[j][3])*100, 3))
            # list_to_save.append(round(util.calculate_percent_difference(chunk[j][2], chunk[j][3])*100, 3))
            # list_to_save.append(round(rsi[-(25-j)]/100, 2))
            # if j!=0:
            #     # list_to_save.append(round(util.calculate_percent_difference(chunk[j-1][1], chunk[j][1])*100, 3))
            #     list_to_save.append(round(util.calculate_percent_difference(chunk[j-1][2], chunk[j][2])*100, 3))
            #     list_to_save.append(round(util.calculate_percent_difference(chunk[j-1][3], chunk[j][3])*100, 3))
            # elif j==0:
            #     # list_to_save.append(0)
            #     list_to_save.append(0)
            #     list_to_save.append(0)
            
        
        # print(len(list_to_save), list_to_save)
        prediction_2, prediction_1 = prd.make_prediction(sv.model_1, list_to_save, sv.scaler, 1)

    # index = util.find_index(data[i][0], sv.btc_data_1)
    # if index is not None and index >= 50:
    #     sample_2 = sv.btc_data_1[index-50:index]

    #     last_cand = util.combine_last_candle(sv.btc_data_1[index][0], data[i][0], data)
    #     if last_cand is not None:
    #         sample_2 = np.append(sample_2, [last_cand], axis=0)

            # index = util.find_index(data[i][0], data_3)
            # if index is not None and index>60:
            #     sample_3 = data_3[index-60:index]
            
            
            #     last_cand_3 = util.combine_last_candle(data_3[index][0], data[i][0], data)
            #     if last_cand_3 is not None:
            #         sample_3 = np.append(sample_3, [last_cand_3], axis=0)
            # prediction_1 = prd.predict_image_class(sv.model_1, 1, sample, sample_2, None, 2)
            # if prediction_1:
        # prediction_2 = prd.predict_image_class(sv.model_1, 4, sample, sample_2, None, 4)
            # if prediction_2 > 0.4:
            #     prediction_1 = prd.predict_image_class(sv.model_1, 2, sample, sample_2, None, 2)
    # chunk = data[i-72:i]
    # list_to_pred = []
    # for j, ch in enumerate(chunk):
    #     if j >67:
    #         list_to_pred.extend(ch[1:5])
    #     else:
    #         list_to_pred.append(ch[4])

    # pred = prd.make_predictions(list_to_pred)
    # print('pred: ', pred, closes[-1], pred > closes[-1])
    # if pred > closes[-1]:
    
        if prediction_2<=1:# and (prediction_2[2] > -0.15 and prediction_2[1] > 0.20):# and sv.prev_val>0:
            sv.signal.type_os_signal = 'long_1'
            sv.settings.init_stop_loss = 0.01#serv.set_stls(0.020, abs(vol_can))#0.004
            sv.settings.take_profit = 0.10
            sv.settings.target_len = 2#5
            sv.settings.amount = 20#20
            sv.cl = prediction_2
            sg = 2
        # else:
        #     sv.signal.type_os_signal = 'long_1'
        #     sv.settings.init_stop_loss = 0.005#serv.set_stls(0.020, abs(vol_can))#0.004
        #     sv.settings.take_profit = 0.10
        #     sv.settings.target_len = 2#5
        #     sv.settings.amount = 20#20
        #     sg = 2
        #=================START LOGIC===================
        sv.prev_val = prediction_2
        
                
   
        #=================END LOGIC=====================

        if sg in sv.settings.s:
            sv.settings.amount = 20
            sv.signal.signal = sg
            # pos = {'open_time': data[i][0]}
            # pos_list = util.filter_dicts(sv.etalon_positions, pos, 60, 1)
            # types_7 = [val['type_of_signal'] for val in pos_list]
            # if len(types_7)>1:
            #     # sv.settings.amount*=0.5
            #     sv.signal.signal = 3
            #     return
            sv.signal.data = sv.settings.time
            # sv.settings.init_stop_loss = 0.015#0.004
            # sv.settings.take_profit = 0.25
            # sv.settings.take_profit = 0.007#0.004
            # sv.settings.take_profit = 0.004
            # sv.settings.target_len = 2#3
            # sv.signal.type_os_signal = 'ham_60c'
            sv.signal.volume = abs(util.calculate_percent_difference(highs[-3], lows[-1]))
            sv.signal.data = 60
            sv.signal.index = i
        else:
            sv.signal.signal = 3
    except Exception as e:
        print(e, i)
