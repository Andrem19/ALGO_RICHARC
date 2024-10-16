import numpy as np
import datetime
import shared_vars as sv
import helpers.get_data as gd
import traceback
import helpers.tools as tools
import coins as coins
import random
import json
import pandas as pd
from statistics import mean
from collections import Counter
import msvcrt
import time
import os
from collections import defaultdict
from sortedcontainers import SortedDict

def sum_profits_by_day(trades):
    daily_profits_positive = defaultdict(float)
    daily_profits_negative = defaultdict(float)
    first_trade_time = {}

    for trade in trades:
        # Преобразуем время закрытия в дату
        close_time = datetime.datetime.fromtimestamp(trade['close_time'] / 1000)
        date = close_time.date()

        # Суммируем profit по дням
        if trade['profit'] >= 0:
            daily_profits_positive[date] += trade['profit']
        else:
            daily_profits_negative[date] += trade['profit']

        # Сохраняем время первой сделки за день
        if date not in first_trade_time:
            first_trade_time[date] = close_time

    # Формируем результат в нужном формате
    result = []

    for date in daily_profits_positive.keys() | daily_profits_negative.keys():
        if date in daily_profits_positive:
            result.append({
                'close_time': int(first_trade_time[date].timestamp() * 1000),
                'profit': daily_profits_positive[date],
                'type': 'positive'
            })
        if date in daily_profits_negative:
            result.append({
                'close_time': int(first_trade_time[date].timestamp() * 1000),
                'profit': daily_profits_negative[date],
                'type': 'negative'
            })

    return result

def filter_dicts_less_10(dict_list, number, more_less):
    count_dict = defaultdict(int)
    for d in dict_list:
        count_dict[d['open_time']] += 1
    filtered_list = None
    if more_less == 'more':
        filtered_list = [d for d in dict_list if count_dict[d['open_time']] > number or 'ham_1b' in d['type_of_signal']]
    elif more_less == 'less':
        filtered_list = [d for d in dict_list if count_dict[d['open_time']] < number or 'ham_1b' in d['type_of_signal']]
    return filtered_list


def save_list(my_list, path):
    try:
        with open(path, 'a') as file:
            for item in my_list:
                if all(key in item for key in ['open_time', 'close_time', 'signal', 'profit', 'coin', 'saldo', 'data_s', 'type_of_signal', 'volume']):
                    
                    file.write(f"{item['open_time']},{item['close_time']},{item['signal']},{item['profit']},{item['coin']},{item['saldo']},{item['data_s']},{item['type_of_signal']},{item['type_close']},{item['volume']}" + "\n")
                else:
                    print(f'Some keys are missing {item}')
    except Exception as e:
        print(f'Error [save_list] {e}')
        print(traceback.format_exc())


def load_positions(folder_path: str):
    data = []
    
    file_name = f'{sv.unique_ident}_profits.txt'
    file_path = os.path.join(folder_path, file_name)
    
    if not os.path.exists(file_path):
        print(f'File {file_path} does not exist')
        return data

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) < 10:
                print(f'Invalid line: {line}')
                continue

            try:
                timestamp_open = float(parts[0])
                timestamp_close = float(parts[1])
                signal = int(parts[2])
                value = float(parts[3])
                coin = str(parts[4])
                saldo = float(parts[5])
                data_s = int(parts[6])
                type_of_signal = str(parts[7])
                type_close = str(parts[8])
                volume = float(parts[9])

                position = {
                    'open_time': timestamp_open,
                    'close_time': timestamp_close,
                    'signal': signal,
                    'profit': value,
                    'coin': coin,
                    'saldo': saldo,
                    'data_s': data_s,
                    'type_of_signal': type_of_signal,
                    'type_close': type_close,
                    'volume': volume,
                }
                data.append(position)
            except ValueError as e:
                print(f'Error parsing line: {line}. Error: {e}')
                continue

    sorted_data = sorted(data, key=lambda x: x['open_time'])
    return sorted_data
# def load_positions(folder_path: str):
#     data = []
    
#     curent_line = ''
#     file_name = f'{sv.unique_ident}_profits.txt'
#     file_path = os.path.join(folder_path, file_name)
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#         for line in lines:
#             try:
#                 curent_line = line
#                 if line != '':
#                     parts = line.strip().split(',')
#                     timestamp_open = float(parts[0])
#                     timestamp_close = float(parts[1])
#                     signal = int(parts[2])
#                     value = float(parts[3])
#                     coin = str(parts[4])
#                     saldo = float(parts[5])
#                     data_s = int(parts[6])
#                     type_of_signal = str(parts[7])
#                     type_close = str(parts[8])
#                     volume = float(parts[9])

#                     position = {
#                         'open_time': timestamp_open,
#                         'close_time': timestamp_close,
#                         'signal': signal,
#                         'profit': value,
#                         'coin': coin,
#                         'saldo': saldo,
#                         'data_s': data_s,
#                         'type_of_signal': type_of_signal,
#                         'type_close': type_close,
#                         'volume': volume,
#                     }
#                     data.append(position)
#             except Exception as e:
#                 print(traceback.format_exc())
#                 print(curent_line)
#                 print(e)
#                 continue
    
    
#     sorted_data = sorted(data, key=lambda x: x['open_time'])
#     return sorted_data

# def last_closed_multiplier(data, time_in_milliseconds):
#     # Конвертируем 10 минут в миллисекунды
#     ten_minutes_in_milliseconds = 10 * 60 * 1000

#     data.sort(key=lambda x: x['close_time'], reverse=True)

#     for position in data:
#         # Проверяем, что позиция закрылась не позднее, чем 10 минут назад
#         if position['close_time'] < time_in_milliseconds and position['close_time'] >= time_in_milliseconds - ten_minutes_in_milliseconds:
#             if position['profit']>0:
#                 return True
#             else:
#                 return False

#     return None
def at_time_position_opened(data, time_in_milliseconds):
    positions_open_at_time = [p for p in data if p['open_time'] == time_in_milliseconds]

    return positions_open_at_time


def load_etalon_positions():
    data = []
    
    curent_line = ''
    file_path = f'etalon_profits.txt' if sv.mexc == False else f'etalon_profits_mexc.txt'
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            try:
                curent_line = line
                if line != '':
                    parts = line.strip().split(',')
                    timestamp_open = float(parts[0])
                    timestamp_close = float(parts[1])
                    signal = int(parts[2])
                    value = float(parts[3])
                    coin = str(parts[4])
                    saldo = float(parts[5])
                    data_s = int(parts[6])
                    type_of_signal = str(parts[7])
                    type_close = str(parts[8])
                    volume = float(parts[9])

                    position = {
                        'open_time': timestamp_open,
                        'close_time': timestamp_close,
                        'signal': signal,
                        'profit': value,
                        'coin': coin,
                        'saldo': saldo,
                        'data_s': data_s,
                        'type_of_signal': type_of_signal,
                        'type_close': type_close,
                        'volume': volume,
                    }
                    data.append(position)
            except Exception as e:
                print(traceback.format_exc())
                print(curent_line)
                print(e)
                continue
    
    
    sorted_data = sorted(data, key=lambda x: x['open_time'])
    return sorted_data

def insert(dict_1, key, value, index):
    keys = list(dict_1.keys())
    values = list(dict_1.values())

    keys.insert(index, key)
    values.insert(index, value)

    return dict(zip(keys, values))

def count_strings(lst):
    counts = {}
    for string in lst:
        if string in counts:
            counts[string] += 1
        else:
            counts[string] = 1
    return counts

def get_candel_index(timestamp, candeldict):
    if timestamp in candeldict:
        candle_index = candeldict[timestamp]
        return candle_index
    else: return -1


def find_candle_index(timestamp, candles):
    start = 0
    end = len(candles) - 1
    
    while start <= end:
        mid = (start + end) // 2
        if candles[mid][0] == timestamp:
            return mid
        elif candles[mid][0] < timestamp:
            start = mid + 1
        else:
            end = mid - 1
    
    return -1

def get_points_value(saldos_list_len: int):
    points = 10
    if saldos_list_len < 1000 and saldos_list_len > 200:
        points = 50
    elif saldos_list_len > 1000 and saldos_list_len < 5000:
        points = 250
    elif saldos_list_len > 5000 and saldos_list_len < 15000:
        points = 500
    elif saldos_list_len > 15000 and saldos_list_len < 25000:
        points = 1000
    elif saldos_list_len > 25000 and saldos_list_len < 40000:
        points = 2000
    elif saldos_list_len > 40000:
        points = 5000
    return points

def get_profit_percent(profit: float):
    profit = profit / sv.settings.amount * 100
    return profit

def chose_arr(start_ind: int, arr: np.ndarray, step: int):
    new_arr = []
    for i in range(start_ind, len(arr), step):
        new_arr.append(arr[i])
    return np.array(new_arr)

def calculate_percent_difference(close, high_or_low):
    return (high_or_low - close) / close

def compare_perc(close, hl, close_2, hl_2):
    r1 = (hl - close) / close
    r2 = (hl_2 - close_2) / close_2
    return abs(r2)>abs(r1)
    
def spread_imitation(profit: float) -> float:
    choice_list = [False, False, False, True]
    ch = random.choice(choice_list)
    if ch:
        pr = abs(profit)*2
        return -pr
    return profit

def reverse():
    if sv.signal.signal == 2:
        sv.signal.signal = 1 
    elif sv.signal.signal == 1:
        sv.signal.signal = 2

def create_candle_dict(candles):
    candle_dict = {}
    for i, candle in enumerate(candles):
        candle_dict[candle[0]] = i
    return candle_dict

#==========CLEAN FOR SESSION ==================

def start_of_program_preparing():

    remove_files('_profits')
    delete_folder_contents('_pic')

def delete_folder_contents(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.rmdir(dir_path)

def remove_files(directory):
    hours_ago = time.time() - 60*60  # Time 1 hours ago

    file_list = os.listdir(directory)
    for file_name in file_list:
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            file_modification_time = os.path.getmtime(file_path)
            if file_modification_time < hours_ago:
                os.remove(file_path)

def remove_one_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)

#=============================================

def find_matching_timestamp(data_frame_1, data_frame_2):
    for i in range(len(data_frame_1)):
        for j in range(len(data_frame_2)):
            if data_frame_1[i][0] == data_frame_2[j][0]:
                return i, j
    return None, None

def preload(coins_list: list):
    for coin in coins_list:
        sv.settings.coin = coin
        sv.preload_sets[coin] = gd.load_data_sets(sv.start_date, sv.finish_date, sv.settings.time)

def update_dict(existing_dict, new_values):
    for key, value in new_values.items():
        if key in existing_dict:
            existing_dict[key] += value
        else:
            existing_dict[key] = value
    return existing_dict

import csv
import os

def check_and_clean_data(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    cleaned_data = [row for row in data if all(cell != '' for cell in row)]

    if len(cleaned_data) != len(data):
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(cleaned_data)
        print("File was changed")
    else:
        print("File didnt change")

def format_data(data):
    result = ''
    prev_date = None

    for item in data:
        date = datetime.datetime.fromtimestamp(item['open_time'] / 1000).date()

        if prev_date is not None:
            while date - prev_date > datetime.timedelta(days=1):
                prev_date += datetime.timedelta(days=1)
                result += '='

        if item['profit'] > 0:
            result += '⋀'
        elif item['profit'] < 0:
            result += '⋁'

        prev_date = date
    print(result)
    return result


def get_previous_day_rsi(timestamp: float, sorted_rsi_dict: SortedDict):
    index = sorted_rsi_dict.bisect_left(timestamp)
    if index == 0:
        return None

    return sorted_rsi_dict.peekitem(index - 1)[1]

def load_data_from_file(filename):
    with open(filename, 'r') as f:
        exchanges = json.load(f)
    return exchanges

def filter_dicts(dicts, cur_pos, from_c, to_c, tp = 'open_time'):
    current_time = cur_pos['open_time']  # текущее время в миллисекундах
    two_minutes_ago = current_time - to_c * 60 * 1000  # время 2 минуты назад в миллисекундах
    seven_minutes_ago = current_time - from_c * 60 * 1000  # время 7 минут назад в миллисекундах

    # отфильтровать словари, время которых позднее 2х минут назад, но не позднее 7 минут назад
    return [d for d in dicts if seven_minutes_ago <= d[tp] < two_minutes_ago]

def filter_dicts_signal(dicts, cur_pos):
    current_time = cur_pos['open_time']  # текущее время в миллисекундах
    two_minutes_ago = current_time - 1 * 60 * 1000  # время 2 минуты назад в миллисекундах
    seven_minutes_ago = current_time - 10 * 60 * 1000  # время 7 минут назад в миллисекундах

    # отфильтровать словари, время которых позднее 2х минут назад, но не позднее 7 минут назад
    return [d for d in dicts if seven_minutes_ago <= d['open_time'] < two_minutes_ago], [d for d in dicts if two_minutes_ago <= d['open_time'] < current_time]


def load_add_data():
    first = False
    if sv.settings.multi_tf == 1:
        for key, val in sv.settings.aditional_timeframes.items():
            if val == 1 and first == False:
                sv.data[key] = 1
                first = True
                continue
            elif val == 1:
                sv.data[key] = gd.load_data_sets(key)
                sv.candel_dict[key] = create_candle_dict(sv.data[key])

def process_month_saldo_dict(d):
    bin_width=0.8
    rounded_dict = {k: round(v, 2) for k, v in d.items()}

    min_key = min(rounded_dict.items(), key=lambda x: x[1])[0]

    max_key = max(rounded_dict.items(), key=lambda x: x[1])[0]

    avg_value = round(mean(rounded_dict.values()), 2)

    # counter = Counter(rounded_dict.values())
    # most_common_value = counter.most_common(1)[0][0]
    # Group values into bins and count the number of occurrences in each bin
    bins = Counter(round(v/bin_width)*bin_width for v in rounded_dict.values())

    # Find the bin with the most occurrences
    most_common_bin = bins.most_common(1)[0][0]
    
    # Print the results nicely
    print("Rounded dictionary:")
    for k, v in rounded_dict.items():
        print(f"  {k}: {v} - {sv.month_deal_count[k]} - {round((v/sv.settings.amount)*100, 0)}%")
    print(f"Minimum value: {sv.month_profit[min_key]}")
    print(f"Maximum value: {sv.month_profit[max_key]}")
    print(f"Average value: {avg_value}")
    print(f"Value that occurs most frequently: {most_common_bin}")


def find_index(timestamp, data):

    for i in range(len(data)):
        if data[i][0] > timestamp:
            if i > 0:
                return i - 1
            else:
                print(datetime.datetime.fromtimestamp(int(timestamp/1000)))
                return None

    return len(data) - 1


def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

def get_time_segment(start_timestamp, end_timestamp, data):
    result = []
    for sublist in data:
        timestamp = sublist[0]
        if start_timestamp <= timestamp < end_timestamp:
            result.append(sublist)
    return np.array(result)

def combine_last_candle(start_timestamp, end_timestamp, dt):
    data = get_time_segment(start_timestamp, end_timestamp, dt)
    if len(data) < 2:
        return None

    close = data[-1][4]
    highs = data[:, 2]
    lows = data[:, 3]
    open = data[0][1]

    high = np.max(highs)
    low = np.min(lows)

    return [data[0][0], open, high, low, close, 999]

def check_long_rise(data, border):

    close = data[-1][4]
    highs = data[:, 2]
    lows = data[:, 3]
    open = data[0][1]

    high = np.max(highs)
    low = np.min(lows)

    if open > close:
        return False
    
    if tools.check_high_candel(open, low, 0.015):
        return False

    return tools.check_high_candel(close, open, border)


def get_viz_time(h: int) -> str:
    line = '|'
    for _ in range(h):
        line += '=|'
    return line

def get_ident_type(signal: str):
    signals = {
            'ham_1a': '**',
            'ham_2a': '//',
            'ham_5a': '()()',
            'ham_5b': '##',
            'ham_60c': '<>',
            'ham_usdc': '==',
            'ham_usdc_1': "__",
            'ham_long': 'WW',
            'long_1': '@@',
        }
    return signals.get(signal, '')


def combine_time_candles(days, hours, d1, d2):

    combined = days[-d1:]
    # ind = d2-1
    # last_day_timestamp = combined[ind][0]
    
    combined = combined[:-d2]
    
    last_day_timestamp = combined[-1][0] + 86400000
    
    h_list = [hour for hour in hours if hour[0] >= last_day_timestamp]
    combined = np.vstack((combined, h_list))
    
    return combined

def balance_csv(file_path, output_path):
    # Загрузка данных из CSV файла
    data = pd.read_csv(file_path, header=None)
    
    # Разделение данных на признаки и ответы
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    
    # Подсчет количества классов
    class_counts = y.value_counts()
    print('class_counts: ', class_counts)
    
    # Определение меньшего класса
    minority_count = class_counts.min()
    print('min_count: ', minority_count)
    
    # Индексы классов
    indices_to_keep = []
    
    for class_value, count in class_counts.items():
        class_indices = y[y == class_value].index
        if count > minority_count:
            np.random.seed(42)
            class_indices = np.random.choice(class_indices, size=minority_count, replace=False)
        indices_to_keep.extend(class_indices)
    
    # Создание сбалансированного набора данных
    balanced_data = data.loc[indices_to_keep]
    
    # Сохранение сбалансированного набора данных в новый CSV файл
    balanced_data.to_csv(output_path, header=False, index=False)


def read_and_split_csv(file_path):
    result = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                # Разделить строку на 2D массивы по 6 значений в каждом внутреннем массиве
                split_row = [[float(row[i])] + [float(x) for x in row[i+1:i+6]] for i in range(0, len(row), 6)]
                result.append(split_row)
            except ValueError:
                # Пропустить строку, если возникает ошибка преобразования
                continue
    return result

