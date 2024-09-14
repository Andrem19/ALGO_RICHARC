import worker.multi_proccess as prc
import helpers.util as util
import shared_vars as sv
import worker.multi_signal as sg
import worker.loop_proccess as prc_2
import worker.mexc_signals as mx
import copy
from models.settings import Settings
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

                if sv.signal.type_os_signal != 'stub':# and (profit_list[-1]['profit'] < -0.05 or profit_list[-1]['profit'] > 0.05):
                    if profit_list[-1]['profit']<0:
                        path = f'_pic_train_data/0/{i_1}_{sv.settings.coin}.png'
                    elif profit_list[-1]['profit']>0:
                        path = f'_pic_train_data/1/{i_1}_{sv.settings.coin}.png'
                    
                    sample = data[i_1-100:i_1]

                    # index = util.find_index(data[i_1][0], sv.btc_data_1)
                    # if index is not None and index > 100:
                    #     sample_2 = sv.btc_data_1[index-100:index]

                    #     index = util.find_index(data[i_1][0], sv.btc_data_2)
                    #     if index is not None and index>40:
                    #         sample_3 = sv.btc_data_2[index-40:index]

                    #         # viz.save_candlesticks_pic_3(sample, sample_2, sample_3, path)

                    #     viz.save_candlesticks_pic_2(sample, sample_2, path)

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