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

        step_sl = 0.006
        step_up = 0.006
        if sv.signal.signal == 2:
            step_up = 0.006

        take_profit = 0
        price_open = 0
        index = 0
        type_close = ''
        

        s_loss = sv.settings.init_stop_loss
        take_profit = sv.settings.take_profit
        target_len = sv.settings.target_len

        data = dt[ind:ind+target_len]
        # closes = data[:, 4]
        # highs = data[:, 2]
        # lows = data[:, 3]
        # opens = data[:, 1]
        if sv.signal.signal == 1:
            price_open = data[0][1] * (1 - 0.0001)
            stop_loss = (1 - s_loss) * float(price_open)
            take_profit = (1 + take_profit) * float(price_open)
                

        elif sv.signal.signal == 2:
            price_open = data[0][1] * (1 + 0.0001)
            stop_loss = (1 + s_loss) * float(price_open)
            take_profit = (1 - take_profit) * float(price_open)

        border = price_open
        for i in range(target_len):
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
            elif (data[i][2]>take_profit and sv.signal.signal == 1) or (data[i][3]<take_profit and sv.signal.signal == 2):
                type_close = 'target'
                cand_close = data[i]
                price_close = take_profit
                index = i
                break
            else:
                current_state_1 = util.calculate_percent_difference(border, data[i][2])
                current_state_2 = util.calculate_percent_difference(border, data[i][3])
                
                if sv.signal.signal == 1 and current_state_1>step_sl:
                    stop_loss = (1 - step_up) * data[i][2]
                    border = data[i][2]
                elif sv.signal.signal == 2 and current_state_2<-step_sl:
                    stop_loss = (1 + step_up) * data[i][3]
                    border = data[i][3]
                if (data[i][4]<stop_loss and sv.signal.signal == 1) or (data[i][4]>stop_loss and sv.signal.signal == 2):
                    type_close = 'antitarget_plus'
                    cand_close = data[i]
                    price_close = stop_loss
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
            if sv.settings.drawing and profit_list[-1]['profit']<=-0.0:
                title = f'up {index}' if sv.signal.signal == 1 else f'down {index}'
                # viz.draw_candlesticks(dt[ind-100:ind+5], title+f' {sv.signal.type_os_signal}', 5)
                viz.draw_candlesticks(np.append(sv.data_list, sv.next_list, axis=0), title+f' {sv.signal.type_os_signal}', 5)
        index = index-1 if type_close == 'timefinish' or type_close == 'timefinish_plus' else index

        return index+1
    except Exception as e:
        print(e)