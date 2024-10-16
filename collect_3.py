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

def return_class(diff: float, coefficient: float) -> int:
    if diff <= -0.006 * coefficient:
        return 0
    elif -0.006 * coefficient < diff <= -0.002 * coefficient:
        return 1
    elif -0.002 * coefficient < diff <= 0.002 * coefficient:
        return 2
    elif 0.002 * coefficient < diff <= 0.006 * coefficient:
        return 3
    elif diff > 0.006 * coefficient:
        return 4


sv.settings.coin = 'BTCUSDT'
data_1 = gd.load_data_sets(1440)
data = gd.load_data_sets(30)

len_data = len(data)-1
print(f'Data length: {len_data}')
for i in range(1000, len_data):
    path = None
    diff_1 = round(util.calculate_percent_difference(data[i][1], data[i][4]), 4)
    cl = return_class(diff_1, 1)
    path = f'_pic_train_data/{sv.model_number}/{cl}/{i}_{sv.settings.coin}.png'
    # if data[i][1]<data[i][4] and tools.check_high_candel(data[i][4], data[i][1], 0.004):
    #     path = f'_pic_train_data/{sv.model_number}/1/{i}_{sv.settings.coin}.png'
    # elif data[i][1]>data[i][4] and tools.check_high_candel(data[i][4], data[i][1], 0.004):
    #     path = f'_pic_train_data/{sv.model_number}/2/{i}_{sv.settings.coin}.png'
    # else:
    #     path = f'_pic_train_data/{sv.model_number}/0/{i}_{sv.settings.coin}.png'
    #     if i%2==0:
    #             continue
    closes = data[i-25:i, 4]
    trend = tools.what_trend(closes, 5, 5)
    if trend != 'down':
        continue
    if path:
        sample = data[i-25:i]

        index = util.find_index(data[i][0], data_1)
        if index is not None and index > 25:
            sample_2 = data_1[index-25:index]

            last_cand = util.combine_last_candle(data_1[index][0], data[i][0], data)
            if last_cand is not None:
                sample_2 = np.append(sample_2, [last_cand], axis=0)

                viz.save_candlesticks_pic_2(sample, sample_2, path)
                if i%100==0:
                    print(path)