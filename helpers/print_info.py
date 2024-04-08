import colorama
from colorama import Fore, Style
from datetime import datetime

def print_position(position: dict): 

    type_close = position['type_close']
    profit = position['profit']
    position['open_time'] = datetime.fromtimestamp(position['open_time']/1000)
    position['close_time'] = datetime.fromtimestamp(position['close_time']/1000)
    if type_close == 'antitarget' and profit > 0:
        color = Fore.GREEN
    elif type_close == 'antitarget' and profit < 0:
        color = Fore.RED
    elif type_close == 'timefinish' and profit > 0:
        color = Fore.CYAN
    elif type_close == 'timefinish' and profit < 0:
        color = Fore.YELLOW
    elif type_close == 'target' and profit > 0:
        color = Fore.MAGENTA
    elif type_close == 'trailing_stop' and profit > 0:
        color = Fore.LIGHTBLUE_EX
    else:
        color = Fore.BLUE
    colorama.init()
    print(color + str(position) + Style.RESET_ALL)
    colorama.deinit()

def print_colored_dict(dictionary):
    colors = [
        "\033[0;31m",  # красный
        "\033[0;32m",  # зеленый
        "\033[0;33m",  # желтый
        "\033[0;34m",  # синий
        "\033[0;35m",  # фиолетовый
        "\033[0;36m",  # голубой
    ]
    color_index = 0
    output = ""
    for key, value in dictionary.items():
        color = colors[color_index % len(colors)]
        output += f"{color}{key}: {value} "
        color_index += 1
    print(output.rstrip())
    print("\033[0m")