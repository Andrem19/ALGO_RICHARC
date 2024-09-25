import train as tr
import numpy as np
import pandas as pd

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

balance_csv('_train_data/train_data.csv', '_train_data/train_data.csv')

tr.train_lstm_model('_train_data/train_data.csv', 84, 1000, 32)