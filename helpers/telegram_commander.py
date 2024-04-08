import shared_vars as sv
from commander.com import Commander
from managers_func import *
import os
import traceback
import helpers.tel as tel

async def info():
    await tel.send_inform_message(sv.commander.show_tree(), '', False) 

async def start():
    start_program()

async def kill():
    await kill_processes(read_pids_from_file('process_pids.txt'))

def init_commander():
    sv.commander = Commander(logs=True)

    sv.commander.add_command(["info"], info)
    sv.commander.add_command(["start"], start)
    sv.commander.add_command(["kill"], kill)