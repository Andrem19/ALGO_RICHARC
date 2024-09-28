import shared_vars as sv
import os
import helpers.tel as tel
import helpers.get_data as gd
import helpers.util as util
import helpers.statistic_count as stat
import multiprocessing
from datetime import datetime
import worker.single_worker as w
import concurrent.futures
import helpers.vizualizer as viz
import helpers.print_info as printer
import time
import random
output_lock = multiprocessing.Lock()

async def process_result(result, coin, coin_list_len):
    report = stat.proceed_positions(result)
    report['coin'] = coin
    report = util.insert(report, 'Num', coin_list_len, 0)
    printer.print_colored_dict(report)
    # if sv.settings.send_pic:
    #     pt = util.get_points_value(len(result))
    #     drpd, tp_cl = stat.dangerous_moments(result)
    #     with output_lock:
    #         path = viz.plot_time_series(result, True, pt, True, drpd, {})
    #         await tel.send_inform_message(f'{coin}', path, True)
    #         pause = random.randint(10, 20)
    #         time.sleep(pause)
    return report

def do_job(coin: str, profit_path: str, lock):
    file_coin = f'_crypto_data/{coin}/{coin}_1m.csv'
    if not os.path.exists(file_coin):
        print(f'{coin} doesnt exist')
        return
    
    sv.settings.coin = 'BTCUSDT'
    sv.btc_data_1 = gd.load_data_sets(240)
    # sv.btc_data_2 = gd.load_data_sets(1440)
    
    etalon_positions = util.load_etalon_positions()
    sv.etalon_positions = stat.filter_positions(etalon_positions)
    util.load_add_data()
    sv.settings.coin = coin

    # sv.btc_data_3 = gd.load_data_sets(60)

    if sv.settings.multi_tf == 0:
        data_gen = gd.load_data_in_chunks(sv.settings, 100000, sv.settings.time)
    else:
        for key, val in sv.data.items():
            if val is not None:
                data_gen = gd.load_data_in_chunks(sv.settings, 100000, key)
                break

    position_collector = []
    last_position = {}
    is_first_iter = True
    for data in data_gen:
        for key, val in sv.prev_index.items():
            sv.prev_index[key] = 0
        profit_list = w.run(data, last_position, is_first_iter)

        if len(profit_list) > 0:
            is_first_iter = False
            last_position = profit_list[-1]
            with lock:
                util.save_list(profit_list, profit_path)
                position_collector.extend(profit_list)
                if sv.settings.pic_collections:
                    list_of_lists = data.tolist()
                    viz.draw_candlesticks_positions(list_of_lists, profit_list, f'{sv.settings.coin}-{datetime.fromtimestamp(float(data[0][0])/1000)}-{datetime.fromtimestamp(float(data[-1][0])/1000)}')
        elif len(profit_list) == 0:
            is_first_iter = True

    return position_collector

def unpack_and_call(args):
    return do_job(*args, output_lock)

async def mp_saldo(coin_list, use_multiprocessing=True):
    sv.saldo_sum = 0
    zero_saldo_count = 0
    coin_list_len = len(coin_list)
    util.start_of_program_preparing()
    profit_path = f'_profits/{sv.unique_ident}_profits.txt'
    if use_multiprocessing:
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            for coin, result in zip(coin_list, executor.map(unpack_and_call, [(coin, profit_path) for coin in coin_list])):
                report = await process_result(result, coin, coin_list_len)
                coin_list_len-=1
    else:
        for coin in coin_list:
            result = unpack_and_call((coin, profit_path))
            report = await process_result(result, coin, coin_list_len)
            sv.saldo_sum += report['saldo']
            report['allSaldo'] = round(sv.saldo_sum, 2)
            printer.print_colored_dict(report)
            coin_list_len-=1
            # print(f'saldo: {sv.saldo_sum}')
            # if coin_list_len<5:
            #     if (coin_list_len<5 and sv.saldo_sum<=0) or (coin_list_len<5 and sv.saldo_sum==0) or sv.saldo_sum<-20:
            #         print(f'Saldo: {sv.saldo_sum} Next iteration =====>')
            #         return


    if os.path.exists(f'_profits/{sv.unique_ident}_profits.txt'):
        all_positions = util.load_positions('_profits')
        if len(all_positions) > 0:
            filtred_positions = all_positions# stat.filter_positions(all_positions)
            dropdowns, type_collection = stat.dangerous_moments(filtred_positions)
            med_dur = stat.calc_med_duration(filtred_positions)
            stat_dict = stat.get_type_statistic(filtred_positions)
            full_report = stat.proceed_positions(filtred_positions)
            close_types = stat.stat_of_close(filtred_positions)
            if 'saldo' not in full_report:
                full_report['saldo'] = 0
            full_report['med_dur'] = med_dur
            full_report['close_types'] = close_types
            print(full_report)
            print(stat_dict)
            print(dropdowns)
            print(sv.days_gap)
            # sv.reactor.print_pattern()
            points = util.get_points_value(len(filtred_positions))
            path = viz.plot_time_series(filtred_positions, True, points, True, dropdowns, full_report)
            # if sv.saldo_sum>70 and len(filtred_positions)>600:
            await tel.send_inform_message(f'{full_report}', path, True)
            path_3 = viz.plot_types(filtred_positions)
            await tel.send_inform_message(f'', path_3, True)
            print('REPORT: ', sv.report)
            #     time.sleep(2)
            #await tel.send_inform_message(f'{sv.reactor.pattern_info()}', path, True)
                