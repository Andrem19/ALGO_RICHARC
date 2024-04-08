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
import io
import time as tm
import sys
import uuid
import helpers.tel as tel

sv.telegram_api = 'API_TOKEN_1'
coin_list = coins.best_set

async def main(args):
    sv.time_start = datetime.now().timestamp()
    global coin_list
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
    
    sv.time_finish = datetime.now().timestamp()
    seconds = sv.time_finish-sv.time_start
    tm = str(timedelta(seconds=seconds))
    print(f'uid: {sv.unique_ident}')
    print(f'Exec speed: {tm}')

if __name__ == "__main__":
    setup.setup()
    setup.ad_set()
    asyncio.run(main(sys.argv[1:]))