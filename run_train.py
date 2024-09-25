import train as tr
import helpers.util as util
import os
import random
import json
import time
import threading
import asyncio
import shared_vars as sv
import train_regression as trr
import requests
import helpers.tel as tel
import pandas as pd
import numpy as np
import os
import random

stop_thread = False

def check_new_message():
    path = 'message.json'
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        default_data = {
            'is_new_message': False,
            'message': '',
            'stop': False
        }
        with open(path, 'w') as file:
            json.dump(default_data, file)
    
    while not stop_thread:
        with open(path, 'r') as file:
            data = json.load(file)
            if data['is_new_message']:
                asyncio.run(tel.send_inform_message(data['message'], '', False))
                data['is_new_message'] = False
                with open(path, 'w') as file:
                    json.dump(data, file)
        time.sleep(60)

thread = threading.Thread(target=check_new_message)
thread.start()

def balance_csv(file_path, output_path):
    # Загрузка данных из CSV файла
    data = pd.read_csv(file_path, header=None)
    
    # Разделение данных на признаки и ответы
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    
    # Подсчет количества классов
    class_counts = y.value_counts()
    
    # Определение меньшего класса
    minority_class = class_counts.idxmin()
    majority_class = class_counts.idxmax()
    
    # Количество элементов в меньшем классе
    minority_count = class_counts.min()
    print('min_count: ', minority_count)
    
    # Индексы меньшего и большего классов
    minority_indices = y[y == minority_class].index
    majority_indices = y[y == majority_class].index
    
    # Рандомное удаление элементов из большего класса
    np.random.seed(42)
    drop_indices = np.random.choice(majority_indices, size=(class_counts[majority_class] - minority_count), replace=False)
    
    # Создание сбалансированного набора данных
    balanced_indices = y.index.difference(drop_indices)
    balanced_data = data.loc[balanced_indices]
    
    # Сохранение сбалансированного набора данных в новый CSV файл
    balanced_data.to_csv(output_path, header=False, index=False)

balance_csv(f'_train_data/train_data_{sv.model_number}.csv', f'_train_data/train_data_{sv.model_number}.csv')

# trr.train_2Dpic_model_regression(f'_pic_train_data/{sv.model_number}')
trr.train_model_with_two_series(f'_train_data/train_data_{sv.model_number}.csv')

stop_thread = True
thread.join()