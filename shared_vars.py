import numpy as np
import setup as set
from models.signal import Signal
from models.settings import Settings
from datetime import datetime, timedelta
from commander.com import Commander
from database.core import RycharaDB
from models.reactor import Reactor

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



saldo_sum = 0
btc_data = None
btc_rsi_dict = {}

last_command = ''

price_close = 0
delay = 0
frozen = 0

etalon_positions = None
ham_60c_triger = 0
reactor: Reactor = None
treshold = 22
vol_triger = 0
base_data = 'D:\\PYTHON\\MARKET_DATA'

month_profit = {}
month_deal_count = {}
