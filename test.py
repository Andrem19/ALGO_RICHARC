import helpers.profit as pr
import shared_vars as sv
import helpers.util as util
import coins


exchanges = util.load_data_from_file('contracts.json')

for coin in coins.usdc_set:
    if coin not in coins.best_set:
        print(coin)
