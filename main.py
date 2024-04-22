import shared_vars as sv
import coins as coins
from datetime import datetime
import setup as setup
import helpers.util as util
from itertools import product
import random
import variant.single_saldo as ss
import variant.multi_saldo as ms
from datetime import timedelta
import helpers.tools as tools
from models.settings import Settings
import cold_count as cc
import asyncio
from models.reactor import MethodFunc
from models.reactor import Reactor
import io
import time as tm
import sys
import uuid
import helpers.tel as tel

sv.telegram_api = 'API_TOKEN_1'
coin_list = coins.best_set# coins.long_str_collection# coins.best_set

async def main(args):
    # coin_list = []
    # for c in coins.all_coins:
    #     if c not in coins.best_set:
    #         coin_list.append(c)
    # coin_list_2 = []
    # exchanges = util.load_data_from_file('contracts.json')
    # coin_list.clear()
    # for c in exchanges['HL']:
    #     if c in coins.best_set:
    #         coin_list.append(c)
    # for c in exchanges['HL']:
    #     if c in coins.all_coins:
    #         coin_list_2.append(c)
    #         num = 0
    # for co in coin_list_2:
    #     if co not in coin_list:
    #         num+=1
    #         print(num, co)

    sv.time_start = datetime.now().timestamp()
    sv.unique_ident = str(uuid.uuid4())[:8]
    print(f'uid: {sv.unique_ident}')

    if len(args)>0:
        pass

    if sv.settings.main_variant == 1:
        await ss.mp_saldo(coin_list, True)
    elif sv.settings.main_variant == 2:
        if sv.settings.hot_count_on_off==1:
            await ms.mp_saldo(coin_list, True)
        if sv.settings.cold_count_on_off==1:
            if sv.settings.hot_count_on_off==0:
                sv.unique_ident = sv.settings.curren_uid
            await cc.count_run()
    elif sv.settings.main_variant == 3:
        num=0
        while True:
            sv.unique_ident = str(uuid.uuid4())[:8]

            min_br = random.randint(4, 30)
            max_br = min_br + random.randint(10, 40)
            method_1 = MethodFunc(tools.check_rsi, ['closes', 14, min_br, max_br])
            min_br = random.randint(4, 30)
            max_br = min_br + random.randint(10, 40)
            method_2 = MethodFunc(tools.check_rsi, ['closes_2', 14, min_br, max_br])

            first_can = random.choice(['highs1', 'opens1'])
            sec_can = 'lows1' if first_can == 'highs1' else 'closes1'
            ch = [0.02, 0.03, 0.034] if first_can == 'highs1' else [0.02, 0.01, 0.014]
            method_3 = MethodFunc(tools.check_high_candel, [first_can, sec_can, random.choice(ch)])

            first_can = random.choice(['highs1_2', 'opens1_2'])
            sec_can = 'lows1_2' if first_can == 'highs1_2' else 'closes1_2'
            ch = [0.04, 0.054, 0.07] if first_can == 'highs1_2' else [0.03, 0.04, 0.05]
            method_4 = MethodFunc(tools.check_high_candel, [first_can, sec_can, random.choice(ch)])

            opcl = random.choice(['lower', 'bigger', 'none'])
            method_5 = MethodFunc(tools.open_close, ['opens1', 'closes1', opcl])

            opcl = random.choice(['lower', 'bigger', 'none'])
            method_6 = MethodFunc(tools.open_close, ['opens1_2', 'closes1_2', opcl])

            method_7 = MethodFunc(tools.low_high_tails, ['opens1', 'highs1', 'lows1', 'closes1', random.choice(['low', 'high', 'none']), random.choice(['lower', 'bigger']), random.choice([0.4, 0.8, 1.2, 2])])
            method_8 = MethodFunc(tools.low_high_tails, ['opens1_2', 'highs1_2', 'lows1_2', 'closes1_2', random.choice(['low', 'high', 'none']), random.choice(['lower', 'bigger']), random.choice([0.4, 0.8, 1.2, 2])])
            
            method_9 = MethodFunc(tools.last_lowest, ['lows', random.choice([10, 20, 30])])
            method_10 = MethodFunc(tools.last_lowest, ['lows_2', random.choice([10, 20, 30])])

            method_11 = MethodFunc(tools.last_close_higher, ['highs', 'lows', 'closes', random.choice(['lower', 'higher', 'none']), random.choice(['low', 'high'])])
            method_12 = MethodFunc(tools.last_close_higher, ['highs_2', 'lows_2', 'closes_2', random.choice(['lower', 'higher', 'none']), random.choice(['low', 'high'])])

            method_13 = MethodFunc(tools.check_rise, ['highs', 'lows', random.choice([5, 3]), random.choice([2, 1, 0.5, 3]), random.choice(['less', 'bigger'])])
            method_14 = MethodFunc(tools.check_rise, ['highs_2', 'lows_2', random.choice([5, 3]), random.choice([2, 1, 0.5, 3]), random.choice(['less', 'bigger'])])
            
            methods = [method_1, method_2, method_3, method_4, method_5, method_6, method_7, method_8, method_9, method_10, method_11, method_12, method_13, method_14]
            num_elements = random.randint(4, 7)
            selected_methods = random.sample(methods, num_elements)

            reactor = Reactor(selected_methods, 1, random.choice([5, 9, 13, 17, 21, 25]), random.choice([0.04, 0.03, 0.02, 0.05, 0.06, 0.07]))
            reactor.print_pattern()
            sv.reactor = reactor
            try:
                await ss.mp_saldo(coin_list, False)
                num+=1
            except Exception as e:
                print(e)
    # elif sv.settings.main_variant == 4:
    #     num=0
    #     while True:
    #         sv.unique_ident = str(uuid.uuid4())[:8]

    #         min_br = random.randint(4, 30)
    #         max_br = min_br + random.randint(10, 40)
    #         method_1 = MethodFunc(tools.check_rsi, ['closes', 14, min_br, max_br], random.choice([1,2]))
    #         min_br = random.randint(4, 30)
    #         max_br = min_br + random.randint(10, 40)
    #         method_2 = MethodFunc(tools.check_rsi, ['closes_2', 14, min_br, max_br], random.choice([1,2]))

    #         first_can = random.choice(['highs1', 'opens1'])
    #         sec_can = 'lows1' if first_can == 'highs1' else 'closes1'
    #         ch = [0.02, 0.03, 0.034] if first_can == 'highs1' else [0.02, 0.01, 0.014]
    #         method_3 = MethodFunc(tools.check_high_candel, [first_can, sec_can, random.choice(ch)], random.choice([1,2]))

    #         first_can = random.choice(['highs1_2', 'opens1_2'])
    #         sec_can = 'lows1_2' if first_can == 'highs1_2' else 'closes1_2'
    #         ch = [0.04, 0.054, 0.07] if first_can == 'highs1_2' else [0.03, 0.04, 0.05]
    #         method_4 = MethodFunc(tools.check_high_candel, [first_can, sec_can, random.choice(ch)], random.choice([1,2]))

    #         opcl = random.choice(['lower', 'bigger', 'none'])
    #         method_5 = MethodFunc(tools.open_close, ['opens1', 'closes1', opcl], random.choice([1,2]))

    #         opcl = random.choice(['lower', 'bigger', 'none'])
    #         method_6 = MethodFunc(tools.open_close, ['opens1_2', 'closes1_2', opcl], random.choice([1,2]))

    #         method_7 = MethodFunc(tools.low_high_tails, ['opens1', 'highs1', 'lows1', 'closes1', random.choice(['low', 'high', 'none']), random.choice(['lower', 'bigger']), random.choice([0.4, 0.8, 1.2, 2])], random.choice([1,2]))
    #         method_8 = MethodFunc(tools.low_high_tails, ['opens1_2', 'highs1_2', 'lows1_2', 'closes1_2', random.choice(['low', 'high', 'none']), random.choice(['lower', 'bigger']), random.choice([0.4, 0.8, 1.2, 2])], random.choice([1,2]))
            
    #         method_9 = MethodFunc(tools.last_lowest, ['lows', random.choice([10, 20, 30])], random.choice([1,2]))
    #         method_10 = MethodFunc(tools.last_lowest, ['lows_2', random.choice([10, 20, 30])], random.choice([1,2]))

    #         method_11 = MethodFunc(tools.last_close_higher, ['highs', 'lows', 'closes', random.choice(['lower', 'higher', 'none']), random.choice(['low', 'high'])], random.choice([1,2]))
    #         method_12 = MethodFunc(tools.last_close_higher, ['highs_2', 'lows_2', 'closes_2', random.choice(['lower', 'higher', 'none']), random.choice(['low', 'high'])], random.choice([1,2]))

    #         method_13 = MethodFunc(tools.check_rise, ['highs', 'lows', random.choice([5, 3]), random.choice([2, 1, 0.5, 3]), random.choice(['less', 'bigger'])],random.choice([1,2]))
    #         method_14 = MethodFunc(tools.check_rise, ['highs_2', 'lows_2', random.choice([5, 3]), random.choice([2, 1, 0.5, 3]), random.choice(['less', 'bigger'])], random.choice([1,2]))
            
    #         methods = [method_1, method_2, method_3, method_4, method_5, method_6, method_7, method_8, method_9, method_10, method_11, method_12, method_13, method_14]
    #         num_elements = random.randint(4, 14)
    #         selected_methods = random.sample(methods, num_elements)

    #         reactor = Reactor(selected_methods, 1, random.choice([5, 9, 13, 17, 21, 25]), random.choice([0.04, 0.03, 0.02, 0.05, 0.06, 0.07]), 'opt')
    #         reactor.print_pattern()
    #         sv.reactor = reactor
    #         try:
    #             await ss.mp_saldo(coin_list, False)
    #             num+=1
    #         except Exception as e:
    #             print(e)
    
    sv.time_finish = datetime.now().timestamp()
    seconds = sv.time_finish-sv.time_start
    tm = str(timedelta(seconds=seconds))
    print(f'uid: {sv.unique_ident}')
    print(f'Exec speed: {tm}')

if __name__ == "__main__":
    setup.setup()
    setup.ad_set()
    asyncio.run(main(sys.argv[1:]))