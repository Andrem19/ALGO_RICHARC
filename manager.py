import managers_func as mf
from decouple import config
import os
import time
import asyncio
import shared_vars as sv
from datetime import datetime
import helpers.telegram_commander as tel_com
import sys
import helpers.tel as tel


async def main():
    tel_com.init_commander()
    mf.api_token = config("API_TOKEN_1")
    while True:
        current_time = datetime.now()
        await mf.check_and_handle_message()
        if current_time.minute in [3, 7, 13, 17, 22, 27, 23, 37, 43, 47, 53, 57] and current_time.second in [32,33,34,35]:
            if sv.last_command != 'kill' and sv.last_command != 'Kill':
                await mf.check_process_pids()
        time.sleep(4)
        


if __name__ == '__main__':
    asyncio.run(main())