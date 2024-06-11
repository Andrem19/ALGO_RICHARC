# import helpers.profit as pr
# import shared_vars as sv
# import helpers.util as util
# import coins
# full_sum = 0
# sum = 130000
# one_m = sum / (30*12)
# one_y = sum/30
# perc = (one_y*0.04)

# num = 0
# while sum>0:
#     num+=1
    
#     res = one_m+perc
#     full_sum+=res
#     sum-=one_m
#     print(f'month: {num}', round(res, 2))

# print(f'full_sum: {full_sum} full overpay: {full_sum-130000}')

deals = [{"type_of_signal": "ham_60c", "volume": 14}, {"type_of_signal": "ham_60c", "volume": 8}, {"type_of_signal": "ham_60cc", "volume": 12}, {"type_of_signal": "ham_usdc", "volume": 2}, {"type_of_signal": "ham_1b", "volume": 7}, {"type_of_signal": "ham_60cc", "volume": 12}, {"type_of_signal": "ham_60c", "volume": 12}]


deals.sort(key=lambda d: (not('ham_usdc' in d["type_of_signal"]), not('ham_60cc' == d["type_of_signal"]), not('ham_60c' == d["type_of_signal"]), not('ham_1b' in d["type_of_signal"]), -d["volume"]))

print(deals)