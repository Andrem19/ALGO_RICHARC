import pandas as pd
import shared_vars as sv
import helpers.util as util
import csv

data_path = 'D:\\PYTHON\\Data_Collector\\Datasets'
data_1 = util.read_and_split_csv(data_path + '\\1.csv')
data_2 = util.read_and_split_csv(data_path + '\\2.csv')
data_0 = util.read_and_split_csv(data_path + '\\3.csv')
for i, d in enumerate([data_0, data_1, data_2]):
    for example in d:
        list_to_save = []
        for j in range(len(example)):
            list_to_save.append(round(util.calculate_percent_difference(example[j][1], example[j][4])*100, 3))
            list_to_save.append(round(util.calculate_percent_difference(example[j][1], example[j][2])*100, 3))
            list_to_save.append(round(util.calculate_percent_difference(example[j][1], example[j][3])*100, 3))
        list_to_save.append(i)
        path = f'_train_data/train_data_{sv.model_number}.csv'
        with open(path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(list_to_save)