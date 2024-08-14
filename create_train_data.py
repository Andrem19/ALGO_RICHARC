import numpy as np
import helpers.vizualizer as viz

def get_csv_data(path):
    data = np.genfromtxt(path, delimiter=',', skip_header=1)
    return data

data = get_csv_data('undefined_BTCUSDT_60.csv')
counter = 0

for d in data:
    counter+=1
    if d[-2] == 1:
        continue
    path = f'_pic_train_data/{0 if d[-1] == 0 else 1}/{counter}.png'
    trimmed_list = d[:-2]
    c = [trimmed_list[i:i + 6] for i in range(0, len(trimmed_list), 6)]
    viz.save_candlesticks_pic(c, path)