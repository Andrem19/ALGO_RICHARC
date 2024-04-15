import helpers.profit as pr
import shared_vars as sv
# dict_parse = [{'type_of_signal': 'ham_1bz'}, {'type_of_signal': 'ham_1a'}, {'type_of_signal': 'ham_1bz'}, {'type_of_signal': 'ham_1aa'},{'type_of_signal': 'ham_1aa'}]

# dict_parse.sort(key=lambda d: ('ham_1b' in d["type_of_signal"], 'ham_1aa' in d["type_of_signal"],))
# print(dict_parse)

open_price = 3452
sv.settings.amount = 20
sv.settings.maker_fee = 0.12
sv.settings.taker_fee = 0.12
close_price = 3482


# close_price = close_price*(1-0.0004)
# sv.settings.maker_fee = 0.08
# sv.settings.taker_fee = 0.08

res = pr.profit_counter(True, open_price, 'Buy', close_price)
print(res)