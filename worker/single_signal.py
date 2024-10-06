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
        # block_long_token = False
        # block_short_token = False
        # closes = data[i-ln:i, 4]
        # highs = data[i-ln:i, 2]
        # lows = data[i-ln:i, 3]
        # opens = data[i-ln:i, 1]

        # rsi_period = 14
        # bb_period = 20
        # bb_stddev = 2

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
        if datetime.fromtimestamp(data[i-1][0]/1000).minute !=59:
            sv.signal.signal = 3
            return
        
        # prediction_1 = False
        # prediction_2 = 0

        # chunk = data[i-100:i]
        list_to_save_1 = []
        list_to_save_2 = []
        list_to_save_3 = []

        index = util.find_index(data[i][0], sv.btc_data_2)
        if index is not None and index > 100:
            last_cand = util.combine_last_candle(sv.btc_data_2[index][0], data[i][0], data)
            if last_cand is not None:
                sample_3 = sv.btc_data_2[index-99:index]
                sample_3 = np.append(sample_3, [last_cand], axis=0)
            else:
                sample_3 = sv.btc_data_2[index-100:index]

            if len(sample_3)==100:
                for l in range(len(sample_3)):
                    list_to_save_3.append(round(util.calculate_percent_difference(sample_3[l][1], sample_3[l][4])*100, 3))
                    list_to_save_3.append(round(util.calculate_percent_difference(sample_3[l][1], sample_3[l][2])*100, 3))
                    list_to_save_3.append(round(util.calculate_percent_difference(sample_3[l][1], sample_3[l][3])*100, 3))

            index = util.find_index(data[i][0], sv.btc_data_1)
            if index is not None and index > 100:
                last_cand = util.combine_last_candle(sv.btc_data_1[index][0], data[i][0], data)
                if last_cand is not None:
                    sample_2 = sv.btc_data_1[index-99:index]
                    sample_2 = np.append(sample_2, [last_cand], axis=0)
                else:
                    sample_2 = sv.btc_data_1[index-100:index]
                
                #close_prices = [candle[4] for candle in sample_2]
                # high_prices = [candle[2] for candle in sample_2]
                # low_prices = [candle[3] for candle in sample_2]

                #rsi = talib.RSI(np.array(close_prices), timeperiod=rsi_period)
                #upperband, middleband, lowerband = talib.BBANDS(np.array(close_prices), timeperiod=bb_period, nbdevup=bb_stddev, nbdevdn=bb_stddev, matype=0)
            # sample_2 = data[i-100:i]
                for p in range(len(sample_2)):
                    cand = round(util.calculate_percent_difference(sample_2[p][1], sample_2[p][4])*100, 3)

                    list_to_save_2.append(cand)
                    list_to_save_2.append(round(util.calculate_percent_difference(sample_2[p][1], sample_2[p][2])*100, 3))
                    list_to_save_2.append(round(util.calculate_percent_difference(sample_2[p][1], sample_2[p][3])*100, 3))

                    
                    list_to_save_1.append(cand)  # open-close
                    up_frm = sample_2[p][1] if cand <0 else sample_2[p][4]
                    list_to_save_1.append(round(util.calculate_percent_difference(up_frm, sample_2[p][2])*100, 3))  # open-high
                    dwn_frm = sample_2[p][1] if cand >0 else sample_2[p][4]
                    list_to_save_1.append(round(util.calculate_percent_difference(dwn_frm, sample_2[p][3])*100, 3))  # open-low

                    # rsi_value = rsi[p] if not np.isnan(rsi[p]) else 0
                    # list_to_save_2.append(round(rsi_value/100, 3))

                    # # Добавляем Bollinger Bands (0, если нет значения)
                    # upperband_value = upperband[p] if not np.isnan(upperband[p]) else 0
                    # middleband_value = middleband[p] if not np.isnan(middleband[p]) else 0
                    # lowerband_value = lowerband[p] if not np.isnan(lowerband[p]) else 0

                    # close_cand = sample_2[p][4]
                    # if upperband_value != 0 and middleband_value != 0 and lowerband_value != 0:
                    #     if close_cand > upperband_value:
                    #         list_to_save_2.append(1)
                    #     elif close_cand < upperband_value and close_cand > middleband_value:
                    #         list_to_save_2.append(2)
                    #     elif close_cand < middleband_value and close_cand > lowerband_value:
                    #         list_to_save_2.append(3)
                    #     elif close_cand < lowerband_value:
                    #         list_to_save_2.append(4)
                    # else:
                    #     list_to_save_2.append(0)

                    # list_to_save_2.append(round(upperband_value, 3))
                    # list_to_save_2.append(round(middleband_value, 3))
                    # list_to_save_2.append(round(lowerband_value, 3))

                # sv.data_list = list_to_save_2
                sv.data_list = sample_2
                sv.next_list = sv.btc_data_1[index:index+5]
                # trend = tools.what_trend(closes[-25:], 5, 5)
                # if global_vol < -0.05:# or true_count > false_count:
                #     sv.signal.signal = sg
                #     return
            # for j in range(len(chunk)):
            #     list_to_save.append(round(util.calculate_percent_difference(chunk[j][1], chunk[j][4])*100, 3))
            #     list_to_save.append(round(util.calculate_percent_difference(chunk[j][1], chunk[j][2])*100, 3))
            #     list_to_save.append(round(util.calculate_percent_difference(chunk[j][1], chunk[j][3])*100, 3))

    # predicted_class, prediction = prd.make_prediction(sv.model_1, list_to_save, sv.scaler_1, 1, 25)
            predicted_class_3 = 0
            predicted_class_2 = 0
            predicted_class_1 = 0
            prediction_1 = [0,0,0]
            
            # if predicted_class_3 == 1:
            predicted_class_1, prediction_1 = prd.make_prediction(sv.model_1, list_to_save_1, sv.scaler, 1, 100, 3)
            predicted_class_2, prediction_2 = prd.make_prediction(sv.model_2, list_to_save_2, sv.scaler_1, 1, 100, 3)
            if prediction_2[1]>0.60 and prediction_1[1]>0.50:
                predicted_class_3, prediction_3 = prd.make_prediction(sv.model_3, list_to_save_3, sv.scaler_2, 1, 100, 3)

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

  
            if prediction_1[2]>0.60 and predicted_class_2 != 1 and (sample_2[-1][3]<sample_2[-2][3] and sample_2[-1][3]<sample_2[-3][3]):#prediction_2[2]>0.65
                sv.signal.type_os_signal = 'short_2'
                sv.settings.init_stop_loss = 0.012
                sv.settings.take_profit = 0.10
                sv.settings.target_len = 179#5
                sv.settings.amount = 20#20
                # sv.cl = predicted_class
                sg = 2
            elif (
                (prediction_2[1]>0.60 and prediction_1[1]>0.50 and prediction_3[2]<prediction_3[1]) and
                (sample_2[-1][2]>sample_2[-2][2] and sample_2[-1][2]>sample_2[-3][2]) and 
                (sample_2[-1][3]>sample_2[-2][3] or sample_2[-1][3]>sample_2[-3][3])
                  ):
                    sv.signal.type_os_signal = 'long_2'
                    sv.settings.init_stop_loss = 0.01
                    sv.settings.take_profit = 0.10
                    sv.settings.target_len = 200#5
                    sv.settings.amount = 20#20
                    # sv.cl = predicted_class
                    sg = 1
                #(prediction_1[1]>0.60 and predicted_class_3==1 and predicted_class_2!=2)
                #(prediction_2[1]>0.60 and predicted_class_3!=2)  and (sample_2[-1][3]>sample_2[-2][3] and sample_2[-1][3]>sample_2[-3][3]) (sample_2[-1][2]>sample_2[-2][2] and sample_2[-1][2]>sample_2[-3][2]) and 
        #=================START LOGIC===================
        
                
   
        #=================END LOGIC=====================

        if sg in sv.settings.s:
            sv.settings.amount = 20
            sv.signal.signal = sg
            sv.signal.data = sv.settings.time
            sv.signal.volume = abs(util.calculate_percent_difference(data[i-1][3], data[i-1][2]))
            sv.signal.data = 60
            sv.signal.index = i
        else:
            sv.signal.signal = 3
    except Exception as e:
        print(e, i)
