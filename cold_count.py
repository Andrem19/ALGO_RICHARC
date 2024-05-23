import shared_vars as sv
import helpers.tel as tel
import helpers.get_data as gd
import helpers.statistic_count as stat
from datetime import datetime
from models.settings import Settings
import helpers.vizualizer as viz
import helpers.statistic_count as stat
import helpers.util as util
from datetime import timedelta
import asyncio
import random
import time
import copy

async def count():

    random.shuffle(sv.all_positions)
    filtred_positions = stat.filter_positions(sv.all_positions)

    # util.format_data(filtred_positions)

    dropdowns, type_collection = stat.dangerous_moments(filtred_positions)
    med_dur = stat.calc_med_duration(filtred_positions)
    stat_dict = stat.get_type_statistic(filtred_positions)
    full_report = stat.proceed_positions(filtred_positions)
    additional_statistics = stat.additional_statistics_2(filtred_positions)
    full_report['med_dur'] = med_dur
    full_report['coin'] = 'All contracts'
    sv.percent_accumulate.append(full_report['perc'])
    sv.max_border_accum.append(full_report['med_pl'])
    sv.min_border_accum.append(abs(full_report['med_mn']))
    if sv.settings.cold_count_print_all == 1:
        print(f'\033[0;31mGeneral report:\033[0m')
        print(full_report)
        print(f'\033[0;31mDropdowns:\033[0m')
        print(dropdowns)
        print('\033[0;31mStatistic types:\033[0m')
        print(stat_dict)
        print('\033[0;31mDays gap:\033[0m')
        print(sv.days_gap)
        print('\033[0;31mAdd statistic:\033[0m')
        print(additional_statistics)

    dict_splited = stat.sort_by_type(copy.deepcopy(filtred_positions))
    for key, pos in dict_splited.items():
        if sv.settings.cold_count_print_all or sv.settings.cold_count_print_res[key] ==1:
            drdw, type_collection = stat.dangerous_moments(pos)
            points = util.get_points_value(len(pos))
            path = viz.plot_time_series(pos, True, points, True, drdw, {})
            await tel.send_inform_message(f'{key}', path, True)
            time.sleep(0.5)

    if sv.settings.cold_count_print_all or sv.settings.cold_count_print_res['final'] ==1:
        points = util.get_points_value(len(filtred_positions))
        path = viz.plot_time_series(filtred_positions, True, points, True, dropdowns, {})
        await tel.send_inform_message(f'{full_report}', path, True)
    util.update_dict(sv.dropdowns_accumulate, dropdowns)
    sv.sum_saldo.append(full_report['saldo'])

async def count_run():
    sv.time_start = datetime.now().timestamp()
    sv.settings.amount = 20
    iter = sv.settings.cold_count_iterations
    # sv.all_positions = util.load_positions('_profits')
    positions = util.load_positions('_profits')
    
    sv.all_positions = []
    for d in positions:
        ts = datetime.fromtimestamp(d['open_time']/1000)
        if sv.settings.start_date < ts < sv.settings.finish_date:
            sv.all_positions.append(d)

    for i in range(iter):
        await count()
        
        sv.days_gap = {}
        drpdacc = stat.cross_the_border(sv.dropdowns_accumulate, 2)
        print(f'Left: {iter-i}')
        print(f'Stat dropdowns: {drpdacc}') 
        print(f'Med Saldo: {sum(sv.sum_saldo)/len(sv.sum_saldo)}')
        if sv.settings.cold_count_print_all or sv.settings.cold_count_print_res['final'] ==1:
            time.sleep(2)
    drpdacc = stat.cross_the_border(sv.dropdowns_accumulate, 2)
    print(f'All dropdowns: {drpdacc}') 
    print(f'Median Saldo: {sum(sv.sum_saldo)/len(sv.sum_saldo)}')
    print(f'Max Saldo: {max(sv.sum_saldo)}')
    print(f'Min Saldo: {min(sv.sum_saldo)}')
    print(f'Median percent: {sum(sv.percent_accumulate)/len(sv.percent_accumulate)}')
    print(f'Median max bord: {sum(sv.max_border_accum)/len(sv.max_border_accum)}')
    print(f'Median min bord: {sum(sv.min_border_accum)/len(sv.min_border_accum)}')

    sv.settings.cold_count_print_all=1
    await count()

    sv.time_finish = datetime.now().timestamp()
    seconds = sv.time_finish-sv.time_start
    tm = str(timedelta(seconds=seconds))
    print(f'Exec speed: {tm}')