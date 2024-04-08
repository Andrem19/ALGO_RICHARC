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

output_lock = multiprocessing.Lock()

async def process_result(result, coin, coin_list_len):
    report = stat.proceed_positions(result)
    report['coin'] = coin
    report = util.insert(report, 'Num', coin_list_len, 0)
    # printer.print_colored_dict(report)
    return report

def do_job(coin: str, profit_path: str, lock):
    file_coin = f'_crypto_data/{coin}/{coin}_1m.csv'
    if not os.path.exists(file_coin):
        print(f'{coin} doesnt exist')
        return

    sv.settings.coin = coin
    data_gen = gd.load_data_in_chunks(sv.settings, 100000, sv.settings.time)
    position_collector = []
    last_position = {}
    is_first_iter = True

    for data in data_gen:

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
            if coin_list_len>10:
                if (coin_list_len<60 and sv.saldo_sum<=0) or (coin_list_len<66 and sv.saldo_sum==0) or sv.saldo_sum<-100:
                    print('Next iteration =====>')
                    return


    if os.path.exists(f'_profits/{sv.unique_ident}_profits.txt'):
        all_positions = util.load_positions('_profits')
        if len(all_positions) > 0:
            filtred_positions = stat.filter_positions(all_positions)
            dropdowns, type_collection = stat.dangerous_moments(filtred_positions)
            med_dur = stat.calc_med_duration(filtred_positions)
            full_report = stat.proceed_positions(filtred_positions)
            if 'saldo' not in full_report:
                full_report['saldo'] = 0
            full_report['med_dur'] = med_dur
            full_report['coin'] = 'All contracts'
            print(full_report)
            print(dropdowns)
            # sv.reactor.print_pattern()
            points = util.get_points_value(len(filtred_positions))
            path = viz.plot_time_series(filtred_positions, True, points, True, dropdowns, full_report)
            await tel.send_inform_message(f'{full_report}', path, True)
                