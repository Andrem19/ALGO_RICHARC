import helpers.get_data as gd

import shared_vars as sv
import talib
import random
import time
import helpers.util as util
import numpy as np
import helpers.tools as tools
import helpers.vizualizer as viz


sv.settings.coin = 'BTCUSDT'
data_1 = gd.load_data_sets(1440)
data = gd.load_data_sets(60)

len_data = len(data)-1
print(f'Data length: {len_data}')
for i in range(2880, len_data):
    open = data[i][1]
    close = data[i][4]
    diff = util.calculate_percent_difference(open, close)
    if abs(diff) > 0.0001:
        path = f'_pic_train_data/12/{i}_{round(diff*100, 4)}.png'

        sample = data[i-50:i]

        index = util.find_index(data[i][0], data_1)
        if index is not None and index > 50:
            sample_2 = data_1[index-50:index]

            last_cand = util.combine_last_candle(data_1[index][0], data[i][0], data)
            if last_cand is not None:
                sample_2 = np.append(sample_2, [last_cand], axis=0)

            viz.save_candlesticks_pic_2BB(sample, sample_2, path)
            if i%100==0:
                print(path)