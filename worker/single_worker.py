import worker.multi_proccess as prc
import worker.loop_proccess as prc_2
import worker.loop_proccess_3 as prc_3
import worker.single_signal_SP as signalSP
import signal as sg
import shared_vars as sv
import worker.single_signal as sg
import csv
import traceback
import worker.loop_dynamic_sl as prc_4


def run(data, last_position, is_first_iter: bool):
    try:
        data_len = len(data)
        data_len_for_loop = data_len - 180
        profit_list: list = []
        if last_position:
            profit_list.append(last_position)


        i = 1000

        while i < data_len_for_loop:
            
            sg.get_signal(i, data)

            if sv.signal.signal in sv.settings.s:
                tm1 = prc_4.position_proccess(profit_list, data, is_first_iter)
                # if sv.signal.signal == 1:
                #     path = f'_train_data/train_data_{sv.model_number+1}.csv'
                #     if profit_list[-1]['profit']>0.20:
                #         sv.data_list.append(1)
                #     elif profit_list[-1]['profit']<=-0.20:
                #         sv.data_list.append(0)
                # elif sv.signal.signal == 2:
                #     path = f'_train_data/train_data_{sv.model_number}.csv'
                #     if profit_list[-1]['profit']>0.20:
                #         sv.data_list.append(1)
                #     elif profit_list[-1]['profit']<=-0.20:
                #         sv.data_list.append(0)
                
                # with open(path, mode='a', newline='') as file:
                #     writer = csv.writer(file)
                #     writer.writerow(sv.data_list)
                i+=tm1
            else: 
                i+=1

        if is_first_iter == False:
            del profit_list[0]
        return profit_list
    except Exception as e:
        print(f'Error [run] {e}')
        print(traceback.format_exc())