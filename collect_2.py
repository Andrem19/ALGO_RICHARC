import helpers.get_data as gd
import shared_vars as sv
import csv
import helpers.tools as tools
import helpers.util as util
import talib
import numpy as np
def return_class(diff: float, coefficient: float) -> int:
    if diff <= -0.006 * coefficient:
        return 0
    elif -0.006 * coefficient < diff <= -0.002 * coefficient:
        return 1
    elif -0.002 * coefficient < diff <= 0.002 * coefficient:
        return 2
    elif 0.002 * coefficient < diff <= 0.006 * coefficient:
        return 3
    elif diff > 0.006 * coefficient:
        return 4


sv.settings.coin = 'BTCUSDT'
data_1 = gd.load_data_sets(30)
# data_2 = gd.load_data_sets(240)
# data_3 = gd.load_data_sets(1440)
len_data = len(data_1)
print(f'Data length: {len_data}')
path = f'_train_data/train_data_{sv.model_number}.csv'
for i in range(1200, len_data-4):
    # closes = data_1[i-25:i, 4]
    # trend = tools.what_trend(closes, 5, 5)
    # if trend != 'down':
    #     continue
    # if i%2==0:
    #     diff = round(util.calculate_percent_difference(data_1[i][1], data_1[i][4])*100, 3)
    #     if diff < 0.4 and diff > -0.4:
    #         continue

    chunk = data_1[i-25:i]
    
    list_to_save = []
    # rsi = talib.RSI(closes)
    # index = util.find_index(data_1[i][0], data_3)
    # if index is not None and index > 25:
    #     last_cand = util.combine_last_candle(data_3[index][0], data_1[i][0], data_1)
    #     if last_cand is not None:
    #         sample_3 = data_3[index-24:index]
    #         sample_3 = np.append(sample_3, [last_cand], axis=0)
    #     else:
    #         sample_3 = data_3[index-25:index]

    #     if len(sample_3)==25:
    #         for l in range(len(sample_3)):
    #             list_to_save.append(round(util.calculate_percent_difference(sample_3[l][1], sample_3[l][4])*100, 3))
    #             list_to_save.append(round(util.calculate_percent_difference(sample_3[l][1], sample_3[l][2])*100, 3))
    #             list_to_save.append(round(util.calculate_percent_difference(sample_3[l][1], sample_3[l][3])*100, 3))

    #     index = util.find_index(data_1[i][0], data_2)
    #     if index is not None and index > 25:
    #         last_cand = util.combine_last_candle(data_2[index][0], data_1[i][0], data_1)
    #         if last_cand is not None:
    #             sample_2 = data_2[index-24:index]
    #             sample_2 = np.append(sample_2, [last_cand], axis=0)
    #         else:
    #             sample_2 = data_2[index-25:index]

    #         if len(sample_2)==25:
    #             for p in range(len(sample_2)):
    #                 list_to_save.append(round(util.calculate_percent_difference(sample_2[p][1], sample_2[p][4])*100, 3))
    #                 list_to_save.append(round(util.calculate_percent_difference(sample_2[p][1], sample_2[p][2])*100, 3))
    #                 list_to_save.append(round(util.calculate_percent_difference(sample_2[p][1], sample_2[p][3])*100, 3))
            

    for j in range(len(chunk)):
        list_to_save.append(round(util.calculate_percent_difference(chunk[j][1], chunk[j][4])*100, 3))
        list_to_save.append(round(util.calculate_percent_difference(chunk[j][1], chunk[j][2])*100, 3))
        list_to_save.append(round(util.calculate_percent_difference(chunk[j][1], chunk[j][3])*100, 3))
        # list_to_save.append(round(rsi[-(25-j)]/100, 2))
        # if j!=0:
        # #     # list_to_save.append(round(util.calculate_percent_difference(chunk[j-1][1], chunk[j][1])*100, 3))
        #     list_to_save.append(round(util.calculate_percent_difference(chunk[j-1][2], chunk[j][2])*100, 3))
        #     list_to_save.append(round(util.calculate_percent_difference(chunk[j-1][3], chunk[j][3])*100, 3))
        # elif j==0:
        # #     # list_to_save.append(0)
        #     list_to_save.append(0)
        #     list_to_save.append(0)
        # list_to_save.append(round(rsi[-(25-j)]/100, 2))
    # diff_0 = round(util.calculate_percent_difference(data_1[i][1], data_1[i+2][4]), 3)
    
    # diff_2 = round(util.calculate_percent_difference(data_1[i+1][1], data_1[i+1][4]), 3)
    # diff_3 = round(util.calculate_percent_difference(data_1[i+2][1], data_1[i+2][4]), 3)
    diff_1 = round(util.calculate_percent_difference(data_1[i][1], data_1[i][4]), 4)
    # diff_2 = round(util.calculate_percent_difference(data_1[i][1], data_1[i][2])*100, 3)
    # diff_3 = round(util.calculate_percent_difference(data_1[i][1], data_1[i][3])*100, 3)
    # list_to_save.append(return_class(diff_1, 1.2))
    
    list_to_save.append(return_class(diff_1, 1.6))

        
    # list_to_save.append(diff_2)
    # list_to_save.append(diff_3)
    # if diff_1> 0.008:#all(x > 0 for x in [diff_1, diff_2, diff_3]) and any(x > 0.008 for x in [diff_1, diff_2, diff_3]):
    #     list_to_save.append(1)
    # elif diff_1< -0.08:#all(x < 0 for x in [diff_1, diff_2, diff_3]) and any(x < -0.008 for x in [diff_1, diff_2, diff_3]):
    #     list_to_save.append(2)
    # else:
    #     list_to_save.append(0)

    with open(path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(list_to_save)

    if i%100==0:
        print(i)


    