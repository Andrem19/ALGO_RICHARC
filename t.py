import talib
import pandas as pd
import shared_vars as sv
import helpers.util as util
import csv
import numpy as np

data_path = 'D:\\PYTHON\\Data_Collector\\Datasets'
data_1 = util.read_and_split_csv(data_path + '\\1.csv')
data_2 = util.read_and_split_csv(data_path + '\\2.csv')
data_0 = util.read_and_split_csv(data_path + '\\0.csv')

# Период для RSI и Bollinger Bands
# rsi_period = 14
# bb_period = 20
# bb_stddev = 2

for i, d in enumerate([data_0, data_1, data_2]):
    for example in d:
        list_to_save = []

        # Получаем отдельные списки для расчета индикаторов
        # close_prices = [candle[4] for candle in example]
        # high_prices = [candle[2] for candle in example]
        # low_prices = [candle[3] for candle in example]

        # Рассчитываем RSI и Bollinger Bands
        #rsi = talib.RSI(np.array(close_prices), timeperiod=rsi_period)
        #upperband, middleband, lowerband = talib.BBANDS(np.array(close_prices), timeperiod=bb_period, nbdevup=bb_stddev, nbdevdn=bb_stddev, matype=0)

        for j in range(len(example)):
            # Добавляем процентные изменения (как в исходном коде)
            # list_to_save.append(round(util.calculate_percent_difference(example[j][1], example[j][4])*100, 3))
            # list_to_save.append(round(util.calculate_percent_difference(example[j][1], example[j][2])*100, 3))
            # list_to_save.append(round(util.calculate_percent_difference(example[j][1], example[j][3])*100, 3))

            cand = round(util.calculate_percent_difference(example[j][1], example[j][4])*100, 3)
            list_to_save.append(cand)  # open-close
            up_frm = example[j][1] if cand <0 else example[j][4]
            list_to_save.append(round(util.calculate_percent_difference(up_frm, example[j][2])*100, 3))  # open-high
            dwn_frm = example[j][1] if cand >0 else example[j][4]
            list_to_save.append(round(util.calculate_percent_difference(dwn_frm, example[j][3])*100, 3))  # open-low

            # Добавляем RSI (0, если нет значения)
            # rsi_value = rsi[j] if not np.isnan(rsi[j]) else 0
            # list_to_save.append(round(rsi_value/100, 3))

            # Добавляем Bollinger Bands (0, если нет значения)
            # upperband_value = upperband[j] if not np.isnan(upperband[j]) else 0
            # middleband_value = middleband[j] if not np.isnan(middleband[j]) else 0
            # lowerband_value = lowerband[j] if not np.isnan(lowerband[j]) else 0
            # if upperband_value != 0 and middleband_value != 0 and lowerband_value != 0:
            #     if example[j][4] > upperband_value:
            #         list_to_save.append(1)
            #     elif example[j][4] < upperband_value and example[j][4] > middleband_value:
            #         list_to_save.append(2)
            #     elif example[j][4] < middleband_value and example[j][4] > lowerband_value:
            #         list_to_save.append(3)
            #     elif example[j][4] < lowerband_value:
            #         list_to_save.append(4)
            # else:
            #     list_to_save.append(0)

            # list_to_save.append(round(upperband_value, 3))
            # list_to_save.append(round(middleband_value, 3))
            # list_to_save.append(round(lowerband_value, 3))

        # Добавляем метку класса (i - для каждого набора данных)

        list_to_save.append(i)

        # Сохраняем данные в CSV
        path = f'_train_data/train_data_{sv.model_number}.csv'
        with open(path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(list_to_save)

# import csv

# def filter_csv(input_file, output_file):
#     with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
#         reader = csv.reader(infile)
#         writer = csv.writer(outfile)
        
#         for row in reader:
#             if len(row) == 301:
#                 writer.writerow(row)

# # Использование функции
# input_file = '_train_data/train_data_48.csv'
# output_file = '_train_data/train_data_50.csv'
# filter_csv(input_file, output_file)
