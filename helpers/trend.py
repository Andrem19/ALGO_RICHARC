import numpy as np
from sklearn.linear_model import LinearRegression
import math

def analyze_trend(nums, exp_len, r_squared_threshold=0.7):
    # Создаем массивы X и Y для линейной регрессии
    numlen = len(nums)
    X = np.array(range(numlen)).reshape(-1, 1)
    Y = np.array(nums).reshape(-1, 1)

    # Обучаем модель линейной регрессии
    model = LinearRegression()
    model.fit(X, Y)

    # Вычисляем R-квадрат
    r_squared = model.score(X, Y)

    # Если R-квадрат меньше порогового значения, значит, у нас нет четкого тренда
    if r_squared < r_squared_threshold:
        return None, None

    # Получаем угол наклона линии
    angle = math.degrees(math.atan(model.coef_[0][0]))

    # Продолжаем линию на 15 точек вперед
    X_future = np.array(range(len(nums), len(nums) + exp_len)).reshape(-1, 1)
    future_trend = model.predict(X_future)

    return angle, future_trend.flatten()

def analyze_pattern(future_trend_expect, future_trend_real):
    threshold = 0.006 * future_trend_real[-1]
    deviation = future_trend_real - future_trend_expect

    high_growth_indices = np.where(deviation > threshold)[0]
    if len(high_growth_indices)<1:
        return False

    recovery_threshold = 0.0010 * future_trend_expect[-1]
    if abs(future_trend_real[-1] - future_trend_expect[-1]) <= recovery_threshold:
        return True
    else:
        return False