import train as tr
import helpers.util as util
import os
import random
import json
import time
import threading
import asyncio
import shared_vars as sv
import requests
import helpers.tel as tel

import os
import random

stop_thread = False

def remove_files_to_limit(directory: str):
    # Получаем список всех папок в указанной директории
    subdirectories = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    
    # Считаем количество файлов в каждой папке
    file_counts = {subdir: len([f for f in os.listdir(subdir) if os.path.isfile(os.path.join(subdir, f))]) for subdir in subdirectories}
    
    # Находим минимальное количество файлов среди всех папок
    min_file_count = min(file_counts.values())
    
    # Удаляем файлы, чтобы количество файлов в каждой папке стало равным минимальному
    for subdir, count in file_counts.items():
        if count > min_file_count:
            files = [os.path.join(subdir, f) for f in os.listdir(subdir) if os.path.isfile(os.path.join(subdir, f))]
            num_files_to_remove = count - min_file_count
            files_to_remove = random.sample(files, num_files_to_remove)
            
            for file in files_to_remove:
                os.remove(file)
    print(f"Files left in each directory: {min_file_count}")

remove_files_to_limit(f'_pic_train_data/{sv.model_number}')


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

tr.train_2Dpic_model_2(2, f'_pic_train_data/{sv.model_number}', True)

stop_thread = True
thread.join()