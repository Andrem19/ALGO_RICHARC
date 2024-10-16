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
        step = 0.0005
        trailing_init = False
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
            elif (i>3 or tools.check_high_candel(data[i][2], data[i][3], sv.signal.volume*0.50, sv.settings.coin)) and high_tail_1>body_1*2 and data[i][1] < data[i][4] and data[i+1][1]>price_open and sv.signal.type_os_signal in ['ham_1by', 'ham_usdc', 'ham_1bx', 'ham_1a', 'ham_1aa', 'ham_5a', 'ham_60c', 'ham_60cc', 'ham_brg'] or 'ham_usdc' in sv.signal.type_os_signal:
                type_close = 'high_tail'
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
        
        if sv.settings.printer and sv.settings.counter%sv.settings.iter_count==0 and sv.signal.type_os_signal == 'ham_60cc':
            printer.print_position(copy.deepcopy(position))
            if sv.settings.drawing:
                title = f'up {index}' if sv.signal.signal == 1 else f'down {index}'
                viz.draw_candlesticks(dt[ind-30:ind+5], title+f' {sv.signal.type_os_signal}', 5)
        index = index-1 if type_close == 'timefinish' else index

        return index+1

    except Exception as e:
        print(f'Error [position_proccess] {e}')
        print(traceback.format_exc())
        print(sv.signal.data, sv.signal.index, len(dt), len(data))




