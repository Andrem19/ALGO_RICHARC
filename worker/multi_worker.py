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
                # tm = prc_2.position_proccess(profit_list, data, is_first_iter)
                if 'ham_60c' in sv.signal.type_os_signal or sv.signal.data == 5 or sv.signal.type_os_signal == 'ham_1by' or 'ham_usdc' in sv.signal.type_os_signal or 'ham_brg' in sv.signal.type_os_signal:
                    tm = prc_2.position_proccess(profit_list, data, is_first_iter)
                else:
                    tm = prc.position_proccess(profit_list, data, is_first_iter)
                i_1+=tm
            else: 
                i_1+=1

        if is_first_iter == False:
            del profit_list[0]
        return profit_list
    except Exception as e:
        print(f'Error [run] {e}')
        print(traceback.format_exc())