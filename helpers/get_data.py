import pandas as pd
import shared_vars as sv
from datetime import datetime
import numpy as np
from models.settings import Settings

def get_csv_data(path):
    if sv.preload == True:
        return sv.preload_sets[sv.settings.coin]
    data = np.genfromtxt(path, delimiter=',')
    return data

from datetime import datetime

def load_data_sets(timeframe: int):
    tm = ''
    if timeframe == 60:
        tm = '1h'
    else:
        tm = f'{timeframe}m'

    d = get_csv_data(f'_crypto_data/{sv.settings.coin}/{sv.settings.coin}_{tm}.csv')

    filtered_data = d[(d[:, 0] / 1000 >= sv.settings.start_date.timestamp()) & (d[:, 0] / 1000 <= sv.settings.finish_date.timestamp())]
    # filtered_data[np.argsort(filtered_data[:, 0])]

    # # Проверка на последовательность временных меток
    # time_diff = np.diff(data[:, 0]) / 1000  # Разница в секундах
    # expected_diff = sv.settings.time * 60  # Ожидаемая разница в секундах
    # gaps = np.where(time_diff != expected_diff)[0]  # Индексы пропусков

    # if gaps.size > 0:
    #     print("Внимание: данные содержат пропуски или неупорядочены.")
    #     for gap in gaps:
    #         gap_start = datetime.fromtimestamp(data[gap, 0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    #         gap_end = datetime.fromtimestamp(data[gap + 1, 0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    #         print(f"Пропуск между {gap_start} и {gap_end}")
    # else:
    #     print("Данные упорядочены правильно и не содержат пропусков.")

    # print(f'Data {sv.settings.coin} {tm} downloaded successfuly')
    return filtered_data

def load_data_in_chunks(settings: Settings, chunk_size, timeframe):
    tm = ''
    if timeframe == 60:
        tm = '1h'
    else:
        tm = f'{timeframe}m'
    with open(f'_crypto_data/{settings.coin}/{settings.coin}_{tm}.csv', 'r') as file:
        lines = file.readlines()
    for i in range(0, len(lines), chunk_size):
        chunk = np.genfromtxt(lines[i:i+chunk_size], delimiter=',')
        filtered_chunk = chunk[(chunk[:, 0] / 1000 >= settings.start_date.timestamp()) & (chunk[:, 0] / 1000 <= settings.finish_date.timestamp())]
        yield filtered_chunk

def ml_load_data_sets(start: datetime, finish: datetime, settings: Settings):
    tm = ''
    if settings.time == 60:
        tm = '1h'
    else:
        tm = f'{settings.time}m'
    d = get_csv_data(f'_crypto_data/{settings.coin}/{settings.coin}_{tm}.csv')

    filtered_data = d[(d[:, 0] / 1000 >= start.timestamp()) & (d[:, 0] / 1000 <= finish.timestamp())]

    data = filtered_data


    print(f'Data {settings.coin} {tm} downloaded successfuly')
    return data




