import numpy as np
import setup as set
from models.signal import Signal
from models.settings import Settings
from datetime import datetime, timedelta
from commander.com import Commander
from database.core import RycharaDB

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
data_1: np.ndarray = None
data_2: np.ndarray = None
data_5: np.ndarray = None

settings: Settings = set.setup()
additional_settings = RycharaDB.get_dict('ad_set')

dropdowns_accumulate = {}
percent_accumulate = []
max_border_accum = []
min_border_accum = []
sum_saldo = []

candel_dict_1 = {}
candel_dict_2 = {}

saldo_sum = 0
btc_data = None
btc_rsi_dict = {}

last_command = ''

price_close = 0
delay = 0
frozen = 0

etalon_positions = None
rsi_was_low10 = 0