import numpy as np
import setup as set
from models.signal import Signal
from models.settings import Settings
from datetime import datetime, timedelta
from commander.com import Commander
from database.core import RycharaDB
from models.reactor import Reactor
import joblib
import tensorflow as tf
import uuid

days_gap = {}
telegram_api = 'API_TOKEN_1'
commander: Commander = None

signal: Signal = Signal()
counter = 0
unique_ident = None
time_start = 0
time_finish = 0

preload_sets = {}
preload = False
all_positions = None

data: np.ndarray = None

data = {
1: None,
5: None,
15: None,
30: None,
60: None,
1440: None,
}

candel_dict = {
    1: {},
    5: {},
    15: {},
    30: {},
    60: {},
    1440: {},
}
prev_index = {
    1: 0,
    5: 0,
    15: 0,
    30: 0,
    60: 0,
    1440: 0,
}

settings: Settings = set.setup()
additional_settings = RycharaDB.get_dict('ad_set')

dropdowns_accumulate = {}
percent_accumulate = []
max_border_accum = []
min_border_accum = []
sum_saldo = []

mx_one_counter = 0
mx_block = 0

saldo_sum = 0
btc_data_1 = None
btc_data_2 = None
btc_data_3 = None
btc_cand_dict = {}
btc_rsi_dict = {}

last_command = ''

price_close = 0
delay = 0
frozen = 0

etalon_positions = None
unfiltered_positions = None
ham_60c_triger = 0
reactor: Reactor = None
treshold = 22
vol_triger = 0
base_data = 'D:\\PYTHON\\MARKET_DATA'

month_profit = {}
month_deal_count = {}

prev_plus = True
mexc = False


def custom_loss(y_true, y_pred):
    # Матрица штрафов
    penalty_matrix = tf.constant([
        [0.0, 1.0, 2.0, 3.0, 4.0],  # Штрафы для ошибки в классе 0
        [1.0, 0.0, 1.0, 3.0, 3.0],  # Штрафы для ошибки в классе 1
        [2.0, 1.0, 0.0, 1.0, 2.0],  # Штрафы для ошибки в классе 2
        [3.0, 3.0, 1.0, 0.0, 1.0],  # Штрафы для ошибки в классе 3
        [4.0, 3.0, 2.0, 1.0, 0.0],  # Штрафы для ошибки в классе 4
    ], dtype=tf.float32)
    
    # Получение индексов реальных классов
    true_idx = tf.argmax(y_true, axis=-1)

    # Применение softmax к предсказаниям
    y_pred_softmax = tf.nn.softmax(y_pred)

    # Использование индексов для нахождения штрафов для каждого предсказанного класса
    penalties = tf.tensordot(y_pred_softmax, penalty_matrix, axes=1)
    
    # Выбор штрафа в зависимости от правильного класса
    true_penalties = tf.gather_nd(penalties, tf.expand_dims(true_idx, axis=-1), batch_dims=1)

    # Среднее значение штрафов для всех примеров в батче
    penalty_loss = tf.reduce_mean(true_penalties)

    # Основная функция потерь - categorical crossentropy
    cross_entropy_loss = tf.reduce_mean(tf.keras.losses.categorical_crossentropy(y_true, y_pred))

    # Совмещение штрафов и crossentropy
    return cross_entropy_loss + 0.1 * penalty_loss

mod_example = 59
# model_1 = tf.keras.models.load_model(f'_models/my_model_{mod_example}.h5')#, custom_objects={'custom_loss': custom_loss})
model_1 = tf.keras.models.load_model('_models/1h2_trend/model_0.7124.h5')#model_0.7124
model_2 = tf.keras.models.load_model('_models/1h_trend/model_0.8358.h5')#1h_trend/model_0.8358.h5
model_3 = tf.keras.models.load_model('_models/4h_trend/model_0.9098.h5')

# model_4 = tf.keras.models.load_model('_models/1m_ham60/model_0.6280.h5')
# model_5 = tf.keras.models.load_model('_models/1h_arb_long2/model_0.6631.h5')
# model_6 = tf.keras.models.load_model('_models/1h_short/model_0.7881.h5')
long_counter = 0

was_pos_before = 0
image_ident = str(uuid.uuid4())[:8]
model_number = 94
prev_val = 0
plus = 0
minus = 0
scaler = joblib.load('_models/1h2_trend/scaler_1h.pkl')
scaler_1 = joblib.load('_models/1h_trend/scaler_1h.pkl')
scaler_2 = joblib.load('_models/4h_trend/scaler_4h.pkl')

# scaler_3 = joblib.load('_models/1m_ham60/scaler_1h.pkl')
scaler_4 = joblib.load('_models/1h_arb_long/scaler_1h.pkl')
# scaler_5 = joblib.load('_models/1h_short/scaler_1h.pkl')
report = {}
cl = 0
data_list = []
next_list = []

pass_next_pos = False