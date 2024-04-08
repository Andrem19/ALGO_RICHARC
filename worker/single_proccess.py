import shared_vars as sv
import helpers.vizualizer as viz
import numpy as np
import traceback
import helpers.profit as prof
import helpers.print_info as printer

def position_proccess(i: int, profit_list: list, d: np.ndarray, is_first_iter: bool):
    try:
        sv.settings.counter+=1
        stop_loss = 0
        close_time = None

        take_profit = 0
        price_open = 0
        close = 0
        index = 0
        type_close = ''

        s_loss = sv.settings.init_stop_loss
        take_profit = sv.settings.take_profit
        target_len = sv.settings.target_len

        data = d[i:i+target_len]

        data_high = data[:-1, 2]
        data_low = data[:-1, 3]
        index_tp = 0
        index_sl = 0

        if sv.signal.signal == 1:
            price_open = data[0][1] * (1 - 0.0001)
            stop_loss = (1 - s_loss) * float(price_open)
            take_profit = (1 + take_profit) * float(price_open)

            index_tp = next((i for i, x in enumerate(data_high) if x > take_profit), None)
            index_sl = next((i for i, x in enumerate(data_low) if x < stop_loss), None)

        elif sv.signal.signal == 2:
            price_open = data[0][1] * (1 + 0.0001)
            stop_loss = (1 + s_loss) * float(price_open)
            take_profit = (1 - take_profit) * float(price_open)

            index_tp = next((i for i, x in enumerate(data_low) if x < take_profit), None)
            index_sl = next((i for i, x in enumerate(data_high) if x > stop_loss), None)

        if index_tp is not None and index_sl is not None:
            if index_tp < index_sl:
                type_close = 'target'
                close = take_profit
                index = index_tp
            else:
                type_close = 'antitarget'
                close = stop_loss
                index = index_sl
        elif index_sl is not None:
            type_close = 'antitarget'
            close = stop_loss
            index = index_sl
        elif index_tp is not None:
            type_close = 'target'
            close = take_profit
            index = index_tp
        else:
            type_close = 'timefinish'
            close = data[-1][1]
            index = len(data)-1
        last_type_of_close = type_close

        dt = {
            'open_time': float(data[0][0]),
            'profit_list': profit_list,
            'type_close': type_close,
            'price_open': price_open,
            'cand_close': data[index],
            'price_close': close
        }
        position = prof.process_profit(dt, is_first_iter)
        

        if sv.settings.printer and sv.settings.counter%sv.settings.iter_count==0:
            printer.print_position(position)
            if sv.settings.drawing:
                sett = f'tp: {sv.settings.take_profit} sl: {sv.settings.init_stop_loss}'
                title = f'up {index} - {sett}' if sv.signal.signal == 1 else f'down {index} - {sett}'
                viz.draw_candlesticks(data[i-sv.settings.chunk_len:i+index+1], title, sv.settings.chunk_len)
        index = index-1 if last_type_of_close == 'timefinish' else index

        return index+1

    except Exception as e:
        print(f'Error [position_proccess] {e}')
        print(traceback.format_exc())