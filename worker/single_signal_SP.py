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
        sg = 3
        chunk = data[i-114:i]
        list_to_save = []
       
        # for p in range(len(chunk)):
            # cand = round(util.calculate_percent_difference(chunk[p][1], chunk[p][4])*100, 3)
            # list_to_save.append(cand)  # open-close
            # up_frm = chunk[p][1] if cand <0 else chunk[p][4]
            # list_to_save.append(round(util.calculate_percent_difference(up_frm, chunk[p][2])*100, 3))  # open-high
            # dwn_frm = chunk[p][1] if cand >0 else chunk[p][4]
            # list_to_save.append(round(util.calculate_percent_difference(dwn_frm, chunk[p][3])*100, 3))  # open-low
            # list_to_save.append(round(util.calculate_percent_difference(chunk[p][1], chunk[p][4])*100, 3))
            # list_to_save.append(round(util.calculate_percent_difference(chunk[p][1], chunk[p][2])*100, 3))
            # list_to_save.append(round(util.calculate_percent_difference(chunk[p][1], chunk[p][3])*100, 3))
        rsi = talib.RSI(chunk[:, 4])
        rsi_cleaned = np.round(rsi[~np.isnan(rsi)], 2)
        print('len', len(rsi_cleaned))
        predicted_class_1, prediction_1 = prd.make_prediction(sv.model_4, rsi_cleaned, sv.scaler_1, 1, 100, 1)

          
            
        if prediction_1[0]<rsi[-1]-7:
            sv.signal.type_os_signal = 'short_2'
            sv.settings.init_stop_loss = 0.01#serv.set_stls(0.020, abs(vol_can))#0.004
            sv.settings.take_profit = 0.20
            sv.settings.target_len = 2#5
            sv.settings.amount = 20#20
            # sv.cl = predicted_class
            sg = 2
        elif prediction_1[0]>rsi[-1]+7:
            sv.signal.type_os_signal = 'long_2'
            sv.settings.init_stop_loss = 0.01#serv.set_stls(0.020, abs(vol_can))#0.004
            sv.settings.take_profit = 0.20
            sv.settings.target_len = 2#5
            sv.settings.amount = 20#20
            # sv.cl = predicted_class
            sg = 1
        
        #=================START LOGIC===================
        
                
   
        #=================END LOGIC=====================

        if sg in sv.settings.s:
            sv.settings.amount = 20
            sv.signal.signal = sg
            sv.signal.data = sv.settings.time
            sv.signal.volume = abs(util.calculate_percent_difference(highs[-3], lows[-1]))
            sv.signal.data = 60
            sv.signal.index = i
        else:
            sv.signal.signal = 3
    except Exception as e:
        print(e, i)
