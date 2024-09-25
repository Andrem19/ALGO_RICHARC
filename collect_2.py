import helpers.get_data as gd
import shared_vars as sv
import csv
import helpers.util as util
import talib
import numpy as np


sv.settings.coin = 'BTCUSDT'
data_1 = gd.load_data_sets(30)
data_2 = gd.load_data_sets(1440)
len_data = len(data_1)
print(f'Data length: {len_data}')
path = f'_train_data/train_data_{sv.model_number}.csv'
for i in range(100, len_data-4):
    if i%2==0:
        diff = round(util.calculate_percent_difference(data_1[i][1], data_1[i][4])*100, 3)
        if diff < 0.4 and diff > -0.4:
            continue

    chunk = data_1[i-25:i]
    # closes = data_1[i-100:i, 4]
    list_to_save = []
    # rsi = talib.RSI(closes)
    index = util.find_index(data_1[i][0], data_2)
    if index is not None and index > 25:
        last_cand = util.combine_last_candle(data_2[index][0], data_1[i][0], data_1)
        if last_cand is not None:
            sample_2 = data_2[index-24:index]
            sample_2 = np.append(sample_2, [last_cand], axis=0)
        else:
            sample_2 = data_2[index-25:index]

        if len(sample_2)==25:
            for p in range(len(sample_2)):
                list_to_save.append(round(util.calculate_percent_difference(sample_2[p][1], sample_2[p][4])*100, 3))
                list_to_save.append(round(util.calculate_percent_difference(sample_2[p][1], sample_2[p][2])*100, 3))
                list_to_save.append(round(util.calculate_percent_difference(sample_2[p][1], sample_2[p][3])*100, 3))

            for j in range(len(chunk)):
                list_to_save.append(round(util.calculate_percent_difference(chunk[j][1], chunk[j][4])*100, 3))
                list_to_save.append(round(util.calculate_percent_difference(chunk[j][1], chunk[j][2])*100, 3))
                list_to_save.append(round(util.calculate_percent_difference(chunk[j][1], chunk[j][3])*100, 3))
                # list_to_save.append(round(rsi[-(25-j)]/100, 2))
            diff = round(util.calculate_percent_difference(data_1[i][1], data_1[i][4])*100, 3)
            # list_to_save.append(diff)
            if diff > 0.5:
                list_to_save.append(1)
            elif diff < -0.5:
                list_to_save.append(2)
            else:
                list_to_save.append(0)

            with open(path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(list_to_save)

            if i%100==0:
                print(i)