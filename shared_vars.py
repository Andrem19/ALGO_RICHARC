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

mod_example = 36
# model_1 = tf.keras.models.load_model(f'_models/my_model_35.h5')
# model_2 = tf.keras.models.load_model('_models/my_model_29.h5')
# model_3 = tf.keras.models.load_model('_models/my_model_22.h5')
long_counter = 0

was_pos_before = 0
image_ident = str(uuid.uuid4())[:8]
model_number = 13
prev_val = 0
plus = 0
minus = 0
scaler_1 = joblib.load('scaler_1.pkl')
scaler_2 = joblib.load('scaler_2.pkl')
