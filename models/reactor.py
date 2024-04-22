import helpers.tools as tools
import numpy as np

class Reactor:
    def __init__(self, methods_list, signal, targ_len, stop_loss, type = 'standart'):
        self.methods_list: list[MethodFunc] = methods_list
        self.signal = signal
        self.target_len = targ_len
        self.stop_loss = stop_loss
        self.list_of_points = []
        self.type = type

    def call(self, signal: int, opens: np.ndarray, highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, opens_2: np.ndarray, highs_2: np.ndarray, lows_2: np.ndarray, closes_2: np.ndarray) -> int:
        if signal != 3:
            return
        variables = {'opens': opens, 'highs': highs, 'lows': lows, 'closes': closes, 'opens1': opens[-1], 'highs1': highs[-1], 'lows1': lows[-1], 'closes1': closes[-1], 
                     'opens_2': opens_2, 'highs_2': highs_2, 'lows_2': lows_2, 'closes_2': closes_2, 'opens1_2': opens_2[-1], 'highs1_2': highs_2[-1], 'lows1_2': lows_2[-1], 'closes1_2': closes_2[-1]}
        if self.type == 'standart':
            for method in self.methods_list:
                if not method.call_method(variables):
                    return 3, self.target_len, self.stop_loss
            return self.signal, self.target_len, self.stop_loss
        else:
            for method in self.methods_list:
                self.list_of_points.append(method.call_method(variables))
            one = self.list_of_points.count(1)
            two = self.list_of_points.count(2)
            return one, two, self.target_len, self.stop_loss
            

    
    def print_pattern(self):
        print(f'signal: {self.signal}')
        for method in self.methods_list:
            print(method.get_info())
        print(f'targ_len: {self.target_len}')
        print(f'stls: {self.stop_loss}')

    def pattern_info(self):
        lines = f'signal: {self.signal}\n'
        for method in self.methods_list:
            lines += str(method.get_info())
            lines += '\n'
        lines+=f'targ_len: {self.target_len}\n'
        lines+=f'stls: {self.stop_loss}\n'
        return lines
        

class MethodFunc:
    def __init__(self, func, list_args, point = 0):
        self.func = func
        self.list_args = list_args
        self.point = point
    
    def call_method(self, variables: dict) -> bool:
        args = [variables[arg] if arg in variables.keys() else arg for arg in self.list_args]
        res = self.func(*args)
        # if res == True:
        #     print(f'{self.func.__name__} - {res}')
        if self.point == 0:
            return res
        else:
            return self.point

    
    def get_info(self):
        return {
            'func_name': self.func.__name__,
            'list_args': self.list_args,
            'point': self.point,
        }


