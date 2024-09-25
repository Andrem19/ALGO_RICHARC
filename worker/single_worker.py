import worker.multi_proccess as prc
import worker.loop_proccess as prc_2
import worker.loop_proccess_3 as prc_3
import signal as sg
import shared_vars as sv
import worker.single_signal as sg
import traceback


def run(data, last_position, is_first_iter: bool):
    try:
        data_len = len(data)
        data_len_for_loop = data_len - 90
        profit_list: list = []
        if last_position:
            profit_list.append(last_position)


        i = 1200

        while i < data_len_for_loop:
            
            sg.get_signal(i, data)

            if sv.signal.signal in sv.settings.s:
                tm1 = prc.position_proccess(profit_list, data, is_first_iter)
                if profit_list[-1]['profit']<=0:
                    sv.minus+=1
                else:
                    sv.plus+=1
                i+=tm1
            else: 
                i+=1

        if is_first_iter == False:
            del profit_list[0]
        return profit_list
    except Exception as e:
        print(f'Error [run] {e}')
        print(traceback.format_exc())