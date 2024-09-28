from models.signal import Signal
import helpers.tools as tools
import talib
import numpy as np
import helpers.util as util
import shared_vars as sv
from datetime import datetime
import helpers.trend as tr
import random
import predict as prd

def get_signal(i, data):
    try:
        ln = 100
        block_long_token = False
        block_short_token = False
        closes = data[i-ln:i, 4]
        highs = data[i-ln:i, 2]
        lows = data[i-ln:i, 3]
        opens = data[i-ln:i, 1]

        # index = util.find_index(data[i][0], sv.btc_data_1)
        # timestamp = sv.btc_data_1[index][0]
        # hour = datetime.fromtimestamp(timestamp/1000).hour+1
        # global_vol = util.calculate_percent_difference(sv.btc_data_1[index-hour][1], sv.btc_data_1[index-1][4])
        # global_direction = util.calculate_percent_difference(sv.btc_data_1[index-48][1], sv.btc_data_1[index-1][4])
        # trend = tools.what_trend(closes[-25:], 5, 5)
        
        # if global_vol > 0:
        #     block_short_token = True
        # if global_vol < 0:
        #     block_long_token = True
        # if global_vol < -0.05:
        #     block_short_token = True
        #     block_long_token = True

        # if block_short_token and block_long_token:
        #     sv.signal.signal = 3
        #     return

        
        sg = 3

        
        prediction_1 = False
        prediction_2 = 0

        chunk = data[i-100:i]
        list_to_save = []
        list_to_save_2 = []
        # index = util.find_index(data[i][0], sv.btc_data_2)
        # if index is not None and index > 25:
        #     last_cand = util.combine_last_candle(sv.btc_data_2[index][0], data[i][0], data)
        #     if last_cand is not None:
        #         sample_3 = sv.btc_data_2[index-24:index]
        #         sample_3 = np.append(sample_3, [last_cand], axis=0)
        #     else:
        #         sample_3 = sv.btc_data_2[index-25:index]

        #     if len(sample_3)==25:
        #         for l in range(len(sample_3)):
        #             list_to_save.append(round(util.calculate_percent_difference(sample_3[l][1], sample_3[l][4])*100, 3))
        #             list_to_save.append(round(util.calculate_percent_difference(sample_3[l][1], sample_3[l][2])*100, 3))
        #             list_to_save.append(round(util.calculate_percent_difference(sample_3[l][1], sample_3[l][3])*100, 3))

        index = util.find_index(data[i][0], sv.btc_data_1)
        if index is not None and index > 100:
            last_cand = util.combine_last_candle(sv.btc_data_1[index][0], data[i][0], data)
            if last_cand is not None:
                sample_2 = sv.btc_data_1[index-99:index]
                sample_2 = np.append(sample_2, [last_cand], axis=0)
            else:
                sample_2 = sv.btc_data_1[index-100:index]
        # sample_2 = data[i-100:i]
            for p in range(len(sample_2)):
                list_to_save_2.append(round(util.calculate_percent_difference(sample_2[p][1], sample_2[p][4])*100, 3))
                list_to_save_2.append(round(util.calculate_percent_difference(sample_2[p][1], sample_2[p][2])*100, 3))
                list_to_save_2.append(round(util.calculate_percent_difference(sample_2[p][1], sample_2[p][3])*100, 3))
    
            
            # trend = tools.what_trend(closes[-25:], 5, 5)
            # if global_vol < -0.05:# or true_count > false_count:
            #     sv.signal.signal = sg
            #     return
            for j in range(len(chunk)):
                list_to_save.append(round(util.calculate_percent_difference(chunk[j][1], chunk[j][4])*100, 3))
                list_to_save.append(round(util.calculate_percent_difference(chunk[j][1], chunk[j][2])*100, 3))
                list_to_save.append(round(util.calculate_percent_difference(chunk[j][1], chunk[j][3])*100, 3))

            # predicted_class, prediction = prd.make_prediction(sv.model_1, list_to_save, sv.scaler_1, 1, 25)
            predicted_class_1, prediction_1 = prd.make_prediction(sv.model_1, list_to_save, sv.scaler, 1, 100)
            predicted_class_2, prediction_2 = prd.make_prediction(sv.model_2, list_to_save_2, sv.scaler, 1, 100)
                # predicted_class, prediction = prd.make_prediction_2(sv.model_1, list_to_save, sv.scaler_1, sv.scaler_2, sv.scaler_3, 1)
        # predicted_class_2, prediction_2 = prd.make_prediction(sv.model_2, list_to_save, sv.scaler, 1)
        # sv.data_list = list_to_save
        # trend = tools.what_trend(closes[-25:], 5, 5)
        # if trend != 'down':# or global_trend>0:# or true_count > false_count:
        #     sv.signal.signal = sg
        #     return
        # index = util.find_index(data[i][0], sv.btc_data_1)
        # if index is not None and index >= 25:
        #     sample_2 = sv.btc_data_1[index-25:index]

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
            # prediction_2, predicted_class = prd.predict_image_class(sv.model_1, 4, chunk, sample_2, None, 2)
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
                #predicted_class>=3 and predicted_class<=1 and 
        if predicted_class_1 in [1] and predicted_class_2 not in [2]:# and not block_long_token:# and predicted_class_2!=1:# and (prediction_2[2] > -0.15 and prediction_2[1] > 0.20):# and sv.prev_val>0:
            sv.signal.type_os_signal = 'long_1'
            sv.settings.init_stop_loss = 0.01#serv.set_stls(0.020, abs(vol_can))#0.004
            sv.settings.take_profit = 0.10
            sv.settings.target_len = 4#5
            sv.settings.amount = 20#20
            # sv.cl = predicted_class
            sg = 1
        if predicted_class_1 in [2] and predicted_class_2 not in [1]:
            sv.signal.type_os_signal = 'long_1'
            sv.settings.init_stop_loss = 0.01#serv.set_stls(0.020, abs(vol_can))#0.004
            sv.settings.take_profit = 0.10
            sv.settings.target_len = 4#5
            sv.settings.amount = 20#20
            # sv.cl = predicted_class
            sg = 2
        #=================START LOGIC===================
        
                
   
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
