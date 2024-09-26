from models.settings import Settings
import shared_vars as sv
from datetime import datetime
from database.core import RycharaDB

def setup():
    settings = Settings()
    settings.target_len = 2
    settings.init_stop_loss = 0.01
    settings.take_profit = 0.20

    settings.main_variant = 1
    settings.printer = True
    settings.drawing = False
    settings.send_pic = False
    settings.pic_collections = False
    settings.iter_count = 1
    settings.time = 30
    settings.coin = 'BTCUSDT'
    settings.amount = 20
    settings.only = 0
    settings.s = [1] if settings.only == 1 else [2] if settings.only == 2 else (1,2)
    settings.counter = 0
    settings.multi_tf = 0
    settings.aditional_timeframes = {
            1:0,
            5:1,
            15:0,
            30:0,
            60:0,
            1440:0,
        }
    switch = 1
    tren_s = datetime(2021, 1, 1)
    tren_f = datetime(2024, 5, 1)
    val_s = datetime(2024, 5, 1)
    val_f = datetime(2024, 10, 1)

    settings.start_date = tren_s if switch == 0 else val_s
    settings.finish_date = tren_f if switch == 0 else val_f

    settings.taker_fee = 0.01
    settings.maker_fee = 0.04

    settings.curren_uid = '696cd5bf'
    settings.hot_count_on_off = 1
    settings.cold_count_on_off = 0
    settings.cold_count_iterations = 1
    settings.cold_count_print_all = 1
    settings.cold_count_print_res = {
                                    'final': 0,
                                    'ham_1a': 0,
                                    'ham_1aa': 0,
                                    'ham_2a': 0,
                                    'ham_5a': 0,
                                    'ham_5b': 0,
                                    'ham_60c': 0,
                                    'ham_60cc': 0,
                                    'ham_usdc': 0,
                                    'ham_brg': 0,
                                    'ham_usdc_1': 0,
                                    'ham_usdc_2': 0,
                                    'ham_usdc_3': 0,
                                    'ham_1bx': 0,
                                    'ham_1by': 0,
                                    'ham_1bz': 0,
                                    'ham_1az': 0,
                                    'test_5': 0,
                                    'ham_long': 0,
                                    'long_1': 0,
                                }
    sv.settings = settings

    return settings

def ad_set():
    aditional_settings = {
        'test': 'test',
    }
    RycharaDB.write_dict('ad_set', aditional_settings)