import subprocess
from telegram import Bot
from decouple import config
import time
import helpers.tel as tel
import shared_vars as sv
import os
import platform
from datetime import datetime

old_timestamp = 0

api_token = None

def start_program(arg_1: int, arg_2: int, arg_3: int):
    python_command = ['python3', '-u'] if platform.system() == 'Linux' else ['python', '-u']
    process = subprocess.Popen(python_command + ['main.py', str(arg_1), str(arg_2), str(arg_3),], stdout=subprocess.DEVNULL, stderr=open(f'output.log', 'w'))
    write_pids_to_file('process_pids.txt', process.pid)




def write_pids_to_file(filename, pid):
    with open(filename, 'a') as file:
        file.writelines(f"{pid}\n")

def read_pids_from_file(filename):
    with open(filename, 'r') as file:
        pids = [int(pid.strip()) for pid in file.readlines()]
    return pids

async def kill_processes(pids):
    for pid in pids:
        try:
            os.kill(pid, 9)  # Sends a SIGKILL signal to the process
            msg = f"Process with PID {pid} killed successfully"
            await tel.send_inform_message(msg, '', False)
            print(msg)
        except OSError:
            print(f"Failed to kill process with PID {pid}")
    os.remove('process_pids.txt')

async def check_process_pids():
    if not os.path.exists('process_pids.txt'):
        return
    pids = read_pids_from_file('process_pids.txt')

    for pid in pids:
        try:
            os.kill(pid, 0)  # Check if process exists
        except OSError:
            await tel.send_inform_message('Not all process runing...', '', False)



    
async def check_and_handle_message():
    global old_timestamp, api_token
    try:
        bot = Bot(token=api_token)

        updates = await bot.get_updates()
        message = None
        if len(updates) > 0:
            message = updates[-1].message
        else: 
            return
        if message is not None and old_timestamp != message.date.timestamp() and (time.time() - message.date.timestamp()) <= 30:
            chatID = config("CHAT_ID")
            chat_id = message.chat.id
            if str(chat_id) == chatID:
                print('equal')
                old_timestamp = message.date.timestamp()
                await sv.commander.exec_command(message.text)

    except Exception as e:
        import traceback
        print(f'Error [check_and_handle_message]: {e}')
        print(f"Exception type: {type(e)}")
        print(traceback.format_exc())