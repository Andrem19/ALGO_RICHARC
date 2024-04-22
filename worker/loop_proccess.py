import shared_vars as sv
import helpers.vizualizer as viz
import helpers.profit as prof
import helpers.print_info as printer
import numpy as np
import helpers.util as util
import traceback
import helpers.tools as tools
import copy

def position_proccess(profit_list: list, dt: np.ndarray, is_first_iter: bool):
    try:
        ind = sv.signal.index

        sv.settings.counter+=1
        stop_loss = 0

        take_profit = 0
        price_open = 0
        index = 0
        type_close = ''

        s_loss = sv.settings.init_stop_loss
        take_profit = sv.settings.take_profit
        target_len = sv.settings.target_len

        data = dt[ind:ind+target_len]
        closes = data[:, 4]
        highs = data[:, 2]
        lows = data[:, 3]
        opens = data[:, 1]
        if sv.signal.signal == 1:
            price_open = data[0][1] * (1 - 0.0001)
            stop_loss = (1 - s_loss) * float(price_open)
            take_profit = (1 + take_profit) * float(price_open)
                

        elif sv.signal.signal == 2:
            price_open = data[0][1] * (1 + 0.0001)
            stop_loss = (1 + s_loss) * float(price_open)
            take_profit = (1 - take_profit) * float(price_open)

        for i in range(target_len):
            low_tail_1, high_tail_1, body_1 = tools.get_tail_body(data[i][1], data[i][2], data[i][3], data[i][4])
            if i == target_len-1:
                type_close = 'timefinish'
                cand_close = data[i]
                price_close = data[i][1]
                index = len(data)-1
                break
            elif (data[i][3]<stop_loss and sv.signal.signal == 1) or (data[i][2]>stop_loss and sv.signal.signal == 2):
                type_close = 'antitarget'
                cand_close = data[i]
                price_close = stop_loss
                index = i
                break
            elif high_tail_1>body_1*2 and data[i][1] < data[i][4] and sv.signal.type_os_signal in ['ham_1by', 'ham_1bx', 'ham_1a', 'ham_1aa', 'ham_5a', 'ham_60c']:
                #if price_open*1.000<data[i+1][1]:
                    type_close = 'high_tail'
                    cand_close = data[i+1]
                    price_close = data[i+1][1]
                    index = i
                    break
            elif i > 0 and data[i][1] > data[i][4] and data[i-1][1] < data[i-1][4]:
                vol_can_1 = util.calculate_percent_difference(data[i][1], data[i][4])
                vol_can_2 = util.calculate_percent_difference(data[i-1][4], data[i-1][1])
                if vol_can_1>vol_can_2:# and price_open*1.000<data[i+1][1]:
                    type_close = 'engulfing'
                    cand_close = data[i+1]
                    price_close = data[i+1][1]
                    index = i
                    break

        data_dict = {
            'open_time': float(data[0][0]),
            'profit_list': profit_list,
            'type_close': type_close,
            'price_open': price_open,
            'cand_close': cand_close,
            'price_close': price_close
        }

        position = prof.process_profit(data_dict, is_first_iter)
        
        if sv.settings.printer and sv.settings.counter%sv.settings.iter_count==0:
            printer.print_position(copy.deepcopy(position))
            if sv.settings.drawing:
                sett = f'tp: {sv.settings.take_profit} sl: {sv.settings.init_stop_loss}'
                title = f'up {index} - {sett}' if sv.signal.signal == 1 else f'down {index} - {sett}'
                viz.draw_candlesticks(dt[ind-30:ind+target_len+1], title, 30)
        index = index-1 if type_close == 'timefinish' else index

        return index+1

    except Exception as e:
        print(f'Error [position_proccess] {e}')
        print(traceback.format_exc())
        print(sv.signal.data, sv.signal.index, len(dt), len(data))




