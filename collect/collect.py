import helpers.get_data as gd
import shared_vars as sv
import talib
import random
import time
import helpers.util as util
import numpy as np
import helpers.tools as tools
import helpers.vizualizer as viz

import train as tr
import os
import json
import threading
import asyncio
import helpers.tel as tel

def create_candle(opens, highs, lows, closes):
    open = opens[0]
    high = np.max(highs)
    low = np.min(lows)
    close = closes[-1]
    return [open, high, low, close]

sv.settings.coin = 'BTCUSDT'
data_1 = gd.load_data_sets(1440)
data = gd.load_data_sets(60)

len_data = len(data)-1
print(f'Data length: {len_data}')
for i in range(2160, len_data):
    # rsi_1 = talib.RSI(data[i-90:i, 4], 14)
    # op15, hi15, lo15, cl15 = tools.convert_timeframe(data[i-45:i, 1], data[i-45:i, 2], data[i-45:i, 3], data[i-45:i, 4], 15, 2)
    # if rsi_1[-1]<18 and tools.check_high_candel(hi15[-1], lo15[-1], 0.03, sv.settings.coin):
    #     if tools.rsi_repeater(rsi_1[-60:], 5, 0, 46)>5:
            next_4h = create_candle(data[i:i+4, 1], data[i:i+4, 2], data[i:i+4, 3], data[i:i+4, 4])

            if next_4h[0]<next_4h[3] and tools.check_high_candel(next_4h[3], next_4h[0], 0.01):
                path = f'_pic_train_data/1/{i}_{sv.settings.coin}.png'
            elif next_4h[0]>next_4h[3] and tools.check_high_candel(next_4h[0], next_4h[3], 0.01):
                path = f'_pic_train_data/0/{i}_{sv.settings.coin}.png'
            else:
                 continue

            sample = data[i-200:i]
            index = util.find_index(data[i][0], data_1)
            if index is not None and index > 120 and path:
                sample_2 = data_1[index-120:index]

                last_cand = util.combine_last_candle(data_1[index][0], data[i][0], data)
                if last_cand is not None:
                    sample_2 = np.append(sample_2, [last_cand], axis=0)

                # index = util.find_index(data[i][0], data_3)
                # if index is not None and index>60:
                #     sample_3 = data_3[index-60:index]
                
                
                #     last_cand_3 = util.combine_last_candle(data_3[index][0], data[i][0], data)
                #     if last_cand_3 is not None:
                #         sample_3 = np.append(sample_3, [last_cand_3], axis=0)

                    viz.save_candlesticks_pic_2(sample, sample_2, path)
                    print(f'{path}')




# stop_thread = False

# def remove_files_to_limit(directory: str):
#     # Получаем список всех папок в указанной директории
#     subdirectories = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    
#     # Считаем количество файлов в каждой папке
#     file_counts = {subdir: len([f for f in os.listdir(subdir) if os.path.isfile(os.path.join(subdir, f))]) for subdir in subdirectories}
    
#     # Находим минимальное количество файлов среди всех папок
#     min_file_count = min(file_counts.values())
    
#     # Удаляем файлы, чтобы количество файлов в каждой папке стало равным минимальному
#     for subdir, count in file_counts.items():
#         if count > min_file_count:
#             files = [os.path.join(subdir, f) for f in os.listdir(subdir) if os.path.isfile(os.path.join(subdir, f))]
#             num_files_to_remove = count - min_file_count
#             files_to_remove = random.sample(files, num_files_to_remove)
            
#             for file in files_to_remove:
#                 os.remove(file)
#     print(f"Files left in each directory: {min_file_count}")

# remove_files_to_limit('_pic_train_data')


# def check_new_message():
#     path = 'message.json'
#     if not os.path.exists(path) or os.stat(path).st_size == 0:
#         default_data = {
#             'is_new_message': False,
#             'message': '',
#             'stop': False
#         }
#         with open(path, 'w') as file:
#             json.dump(default_data, file)
    
#     while not stop_thread:
#         with open(path, 'r') as file:
#             data = json.load(file)
#             if data['is_new_message']:
#                 asyncio.run(tel.send_inform_message(data['message'], '', False))
#                 data['is_new_message'] = False
#                 with open(path, 'w') as file:
#                     json.dump(data, file)
#         time.sleep(60)

# thread = threading.Thread(target=check_new_message)
# thread.start()

# tr.train_2Dpic_model_2(2, '_pic_train_data', True)

# stop_thread = True
# thread.join()