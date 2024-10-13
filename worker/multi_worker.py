import worker.multi_proccess as prc
import helpers.util as util
import shared_vars as sv
import worker.multi_signal as sg
import worker.loop_proccess as prc_2
import worker.mexc_signals as mx
import copy
from models.settings import Settings
import helpers.tools as tools
import numpy as np
import csv
import traceback
from models.signal import Signal
import helpers.vizualizer as viz


def run(data, last_position, is_first_iter: bool):
    try:
        data_len = len(data)
        data_len_for_loop = data_len - 60
        profit_list: list = []

        if last_position:
            profit_list.append(last_position)

        i_1 = 301 if is_first_iter else 211

        while i_1 < data_len_for_loop:

            sg.get_signal(i_1, data, sv.settings)

            if sv.signal.signal in sv.settings.s:
                tm = 1
                # if sv.signal.type_os_signal == 'long_1':
                #     tm = prc.position_proccess(profit_list, data, is_first_iter)
                # else:
                #     tm = prc_2.position_proccess(profit_list, data, is_first_iter)
                if 'ham_60c' in sv.signal.type_os_signal or sv.signal.type_os_signal == 'ham_1by' or 'ham_usdc' in sv.signal.type_os_signal:#or sv.signal.data == 5
                    tm = prc_2.position_proccess(profit_list, data, is_first_iter)
                else:
                    tm = prc.position_proccess(profit_list, data, is_first_iter)

                
                if 'ham_60c' in sv.signal.type_os_signal:
                    list_to_save = []
                    path = f'_train_data/train_data_{sv.model_number}.csv'
                    for j in range(len(sv.data_list)):
                        cand = round(util.calculate_percent_difference(sv.data_list[j][1], sv.data_list[j][4])*100, 3)
                        list_to_save.append(cand)  # open-close
                        up_frm = sv.data_list[j][1] if cand <0 else sv.data_list[j][4]
                        list_to_save.append(round(util.calculate_percent_difference(up_frm, sv.data_list[j][2])*100, 3))  # open-high
                        dwn_frm = sv.data_list[j][1] if cand >0 else sv.data_list[j][4]
                        list_to_save.append(round(util.calculate_percent_difference(dwn_frm, sv.data_list[j][3])*100, 3))
                    if profit_list[-1]['profit']<=0 and profit_list[-1]['type_close'] == 'antitarget':
                        list_to_save.append(0)
                    elif profit_list[-1]['profit']>0:
                        list_to_save.append(1)
                    
                    with open(path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(list_to_save)
                    
                    
                    # if util.check_long_rise(data[i_1:i_1+60], 0.03):
                    #     path = f'_pic_train_data/1/{i_1}_{sv.settings.coin}.png'
                    # else:
                    #     path = f'_pic_train_data/0/{i_1}_{sv.settings.coin}.png'
                    
                    # sample = data[i_1-60:i_1]

                    # index = util.find_index(data[i_1][0], sv.btc_data_1)
                    # if index is not None and index > 100 and path:
                    #     sample_2 = sv.btc_data_1[index-100:index]

                    #     tms = sample_2[:, 0]
                    #     op = sample_2[:, 1]
                    #     hi = sample_2[:, 2]
                    #     lo = sample_2[:, 3]
                    #     cl = sample_2[:, 4]
                        # sample_2 = tools.convert_timeframe_with_timestamps(tms, op, hi, lo, cl, 2, 200)

                    #===================   
                        # last_cand = util.combine_last_candle(sv.btc_data_1[index][0], data[i_1][0], sv.btc_data_2)
                        # if last_cand is not None:
                        #     sample_2 = np.append(sample_2, [last_cand], axis=0)

                        # index = util.find_index(data[i_1][0], sv.btc_data_3)
                        # if index is not None and index>90:
                        #     sample_3 = sv.btc_data_3[index-90:index]
                        
                        
                        #     last_cand_3 = util.combine_last_candle(sv.btc_data_3[index][0], data[i_1][0], data)
                        #     if last_cand_3 is not None:
                        #         sample_3 = np.append(sample_3, [last_cand_3], axis=0)

                            # viz.save_candlesticks_pic_2(sample, sample_2, path)
                        #         viz.save_candlesticks_pic_3(sample_2, sample, sample_3, path)
                    #============================
                i_1+=tm

                # if profit_list[-1]['profit']<0:
                #     sv.mx_one_counter+=1
                # else:
                #     sv.mx_one_counter=0
                # if sv.mx_one_counter>3:
                #     sv.mx_block=15
                #     sv.mx_one_counter=0
            else: 
                i_1+=1

        if is_first_iter == False:
            del profit_list[0]
        return profit_list
    except Exception as e:
        print(f'Error [run] {e}')
        print(traceback.format_exc())