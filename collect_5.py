import talib
import pandas as pd
import shared_vars as sv
import helpers.util as util
import helpers.vizualizer as viz
import csv
import numpy as np

data_path = 'D:\\PYTHON\\Data_Collector\\Datasets'
data_1 = util.read_and_split_csv(data_path + '\\2.csv')
# data_2 = util.read_and_split_csv(data_path + '\\2.csv')
data_0 = util.read_and_split_csv(data_path + '\\1.csv')
num = 0
for i, d in enumerate([data_0, data_1]):
    for example in d:
        num+=1
        # if i == 0:
        #     if num%2==0 or num %3==0 or num%5==0:
        #         continue
        
        path = f'_pic_train_data/{sv.model_number}/{i}/{num}_{sv.settings.coin}.png'
        viz.save_candlesticks_pic_1(example, path)
        if num%100==0:
            print(path)