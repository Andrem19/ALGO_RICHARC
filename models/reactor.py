import helpers.tools as tools
import numpy as np

class Reactor:
    def __init__(self, methods_list, signal):
        self.methods_list: list[MethodFunc] = methods_list
        self.signal = signal

    def call(self, signal: int, opens: np.ndarray, highs: np.ndarray, lows: np.ndarray, closes: np.ndarray) -> int:
        if signal != 3:
            return
        variables = {'opens': opens, 'highs': highs, 'lows': lows, 'closes': closes, 'opens1': opens[-1], 'highs1': highs[-1], 'lows1': lows[-1], 'closes1': closes[-1]}
        for method in self.methods_list:
            if not method.call_method(variables):
                return 3
        return self.signal
    
    def print_pattern(self):
        print(f'signal: {self.signal}')
        for method in self.methods_list:
            print(method.get_info())

    def pattern_info(self):
        lines = f'signal: {self.signal}\n'
        for method in self.methods_list:
            lines += str(method.get_info())
            lines += '\n'
        return lines
        

class MethodFunc:
    def __init__(self, func, list_args):
        self.func = func
        self.list_args = list_args
    
    def call_method(self, variables: dict) -> bool:
        args = [variables[arg] if arg in variables.keys() else arg for arg in self.list_args]
        res = self.func(*args)
        # if res == True:
        #     print(f'{self.func.__name__} - {res}')
        return res

    
    def get_info(self):
        return {
            'func_name': self.func.__name__,
            'list_args': self.list_args,
        }


