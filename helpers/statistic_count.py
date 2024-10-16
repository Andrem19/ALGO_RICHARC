import shared_vars as sv
import copy
from datetime import datetime
from datetime import timedelta
import helpers.util as util

def get_type_statistic(positions: list) -> dict:
    stat_dict = {}
    for pos in positions:
        plus_key = f'{pos["type_of_signal"]}plus'
        minus_key = f'{pos["type_of_signal"]}minus'
        prof_key = f'{pos["type_of_signal"]}prof'
        stls_close = f'{pos["type_of_signal"]}_Stls'
        
        if plus_key in stat_dict and pos['profit']> 0:
            stat_dict[plus_key]+=1
        elif minus_key in stat_dict and pos['profit']<= 0:
            stat_dict[minus_key]+=1
        else:
            if pos['profit']> 0:
                stat_dict[plus_key]=1
            else:
                stat_dict[minus_key]=1
        
        if prof_key in stat_dict:
            stat_dict[prof_key]+=pos['profit'] 
        else:
            stat_dict[prof_key]=pos['profit']

        if pos["open_time"] == pos["close_time"] and pos['profit'] < 0:
            if stls_close in stat_dict:
                stat_dict[stls_close]+=1
            else:
                stat_dict[stls_close]=1
    new_dict = {}
    for pos in positions:
        plus_key = f"{pos['type_of_signal']}plus"
        minus_key = f"{pos['type_of_signal']}minus"
        prof_key = f'{pos["type_of_signal"]}prof'
        stls_close = f'{pos["type_of_signal"]}_Stls'
        
        if plus_key in stat_dict and minus_key in stat_dict and prof_key in stat_dict and stls_close in stat_dict:
            plus = stat_dict[plus_key]
            minus = stat_dict[minus_key]
            prof = stat_dict[prof_key]
            stls = stat_dict[stls_close]
            new_dict[pos["type_of_signal"]] = f'{plus}/{minus}'
            new_dict[prof_key] = prof
            new_dict[stls_close] = f'{stls}/{round(stls/minus, 2)}%'
    return new_dict

def type_of_closes_stat(positions: list):
    dict_pos = {}
    data_5 = 0
    for pos in positions:
        if pos['data_s'] == 5:
            data_5 += 1
        if pos['type_close'] in dict_pos:
            dict_pos[pos['type_close']]+=1
        else:
            dict_pos[pos['type_close']]=1
    print(f'data_s 5 = {data_5}')
    return dict_pos

def sort_by_type(positions: list):
    dict_split = {}
    for pos in positions:
        if pos['type_of_signal'] in dict_split:
            dict_split[f"{pos['type_of_signal']}"].append(pos)
        else:
            dict_split[f"{pos['type_of_signal']}"] = []
            dict_split[f"{pos['type_of_signal']}"].append(pos)

    for key, val in dict_split.items():
        val[0]['saldo'] = val[0]['profit']
        for i in range(1, len(val)):
            val[i]['saldo'] = val[i-1]['saldo']+val[i]['profit']    
    return dict_split

def additional_statistics(positions: list):
    max_plus_in_row = 0
    max_minus_in_row = 0
    plus_in_row = 0
    minus_in_row = 0

    for position in positions:
        if position['profit'] > 0:
            plus_in_row += 1
            minus_in_row = 0
            if plus_in_row > max_plus_in_row:
                max_plus_in_row = plus_in_row
        elif position['profit'] < 0:
            minus_in_row += 1
            plus_in_row = 0
            if minus_in_row > max_minus_in_row:
                max_minus_in_row = minus_in_row

    result = {
        'max_plus_in_row': max_plus_in_row,
        'max_minus_in_row': max_minus_in_row
    }
    return result

def additional_statistics_2(positions: list):
    stats = {}

    for position in positions:
        type_of_signal = position['type_of_signal']

        if type_of_signal not in stats:
            stats[type_of_signal] = {
                'max_plus_in_row': 0,
                'max_minus_in_row': 0,
                'plus_in_row': 0,
                'minus_in_row': 0
            }

        if position['profit'] > 0:
            stats[type_of_signal]['plus_in_row'] += 1
            stats[type_of_signal]['minus_in_row'] = 0
            if stats[type_of_signal]['plus_in_row'] > stats[type_of_signal]['max_plus_in_row']:
                stats[type_of_signal]['max_plus_in_row'] = stats[type_of_signal]['plus_in_row']
        elif position['profit'] < 0:
            stats[type_of_signal]['minus_in_row'] += 1
            stats[type_of_signal]['plus_in_row'] = 0
            if stats[type_of_signal]['minus_in_row'] > stats[type_of_signal]['max_minus_in_row']:
                stats[type_of_signal]['max_minus_in_row'] = stats[type_of_signal]['minus_in_row']

    return stats


def cross_the_border(dropdowns: dict, border: int = 30):
    result = {}
    for key, value in dropdowns.items():
        counter_value = int(key.split('_')[1])
        if counter_value >= border and value > 0:
            result[key] = value
    return result

def proceed_positions(positions: list):
    plus = 0
    minus = 0
    percent = 0
    short_plus = 0
    short_minus = 0
    long_plus = 0
    long_minus = 0
    close_antitarget = 0
    len_pos = len(positions)
    all_plus = []
    all_minus = []
    if len_pos>2:
        for pos in positions:
            if pos['type_close'] == 'antitarget':
                close_antitarget+=1
            if pos['profit'] > 0:
                all_plus.append(pos['profit'])
                plus+=1
                if pos['signal'] == 1:
                    long_plus+=1
                elif pos['signal'] == 2:
                    short_plus+=1
            elif pos['profit'] < 0:
                all_minus.append(pos['profit'])
                minus+=1
                if pos['signal'] == 1:
                    long_minus+=1
                elif pos['signal'] == 2:
                    short_minus+=1
        if plus > 0:
            percent = plus / len_pos
        else:
            percent = 0.5
        saldo = positions[-1]['saldo'] if len_pos > 0 else 0
        am = 1
        if len(all_minus)>0:
            am = round(sum(all_minus) / len(all_minus), 3)
        ap = 1
        if len(all_plus)>0:
            ap = round(sum(all_plus) / len(all_plus), 3)

        result = {
            'saldo': round(saldo, 3),
            'all': len_pos,
            'perc': round(percent,3),
            'short_pl': short_plus,
            'long_pl': long_plus,
            'short_mn': short_minus,
            'long_mn': long_minus,
            'med_pl': ap if am != 0 else 1,
            'med_mn': am if am != 0 else 1,
            'anttrg': round(close_antitarget/len_pos,2),
            'k': round((abs(ap)/abs(am))*percent, 2),
        }
        return result
    return {
        'saldo': 0
    }

def filter_positions(deals, i5 = True):
    # print(len(deals))
    # deals = util.filter_dicts_less_10(deals, 3, 'more')
    # ham_1adict = [d for d in deals if d["type_of_signal"] == "ham_1a"]
    # ham_1adict.sort(key=itemgetter("open_time", "volume"), reverse=True)

    # # группируем по минутам и выбираем запись с наибольшим объемом
    # result = []
    # for _, items in groupby(ham_1adict, key=lambda d: d["open_time"] // 60000):
    #     result.append(max(items, key=itemgetter("volume")))
    # deals = [d for d in deals if d.get('type_of_signal') != 'ham_1a']
    # deals += result

    deals.sort(key=lambda d: (d["open_time"], not ('ham_usdc' in d["type_of_signal"]), not('ham_60c' == d["type_of_signal"]), 'ham_1b' in d["type_of_signal"], -d["volume"]))
    
    filtered_deals = []

    filter_val = {
        'stub': 1,
        'ham_1a': 5,#5
        'ham_1az': 1,
        'ham_1aa': 1,
        'ham_2a': 1,
        'ham_1bx': 1,
        'ham_1by': 1,
        'ham_1bz': 1,
        'ham_60c': 1,
        'ham_60cc': 1,
        'ham_brg': 1,
        'ham_usdc': 2 if sv.mexc == False else 1,#
        'ham_usdc_1': 1,
        'ham_usdc_2': 1,
        'ham_usdc_3': 5,
        'ham_5a': 3,#3
        'ham_5b': 2,#2
        'test_5': 5,
        'test_10': 5,
        'long_1': 3,
    }
    on_off = {
        'stub': 1,
        'ham_1a': 1,
        'ham_1aa': 1,
        'ham_1az': 1,
        'ham_2a': 1,
        'ham_1bx': 1,
        'ham_1by': 1,
        'ham_60c': 1,
        'ham_60cc': 1,
        'ham_brg': 1,
        'ham_usdc': 1,
        'ham_usdc_1': 1,
        'ham_usdc_2': 1,
        'ham_usdc_3': 1,
        'ham_1bz': 1,
        'ham_5a': 1,
        'ham_5b': 1,
        'test_5': 1,
        'test_10': 1,
        'long_1': 1,
    }

    for i in range(len(deals)):
        # if i%1000==0:
        #     print(i)
        active = [d for d in filtered_deals if d["close_time"] >= deals[i]["open_time"]]
        # last_7_min = [d for d in filtered_deals if d["open_time"] >= deals[i]["open_time"] - 7*60*1000]
        last_7 = util.filter_dicts(filtered_deals, deals[i], 7, 2)
        last_0 = util.filter_dicts(filtered_deals, deals[i], 10, 0)
        # last_60 = util.filter_dicts(filtered_deals, deals[i], 60, 15)
        lenth_active = len(active)
        # lenth_active_without_ham_60c = sum(1 for d in active if d.get('type_of_signal')!= 'ham_60c')
        # types_7 = [val['type_of_signal'] for val in last_7]

        # time_X = 'ham_1a' in types_7 or 'ham_2a' in types_7 or 'ham_5b' in types_7 or 'ham_5a' in types_7
        
        if on_off[deals[i]["type_of_signal"]] == 1:
            if all(d['coin'] != deals[i]["coin"] for d in active):
                # types = [t['type_of_signal'] for t in active if 'type_of_signal' in t]
                ham_5a = sum(1 for d in active if d.get('type_of_signal') == 'ham_5a')
                ham_5b = sum(1 for d in active if d.get('type_of_signal') == 'ham_5b')
                ham_1a = sum(1 for d in active if d.get('type_of_signal') == 'ham_1a')
                long_1 = sum(1 for d in active if d.get('type_of_signal') == 'long_1')
                ham_2a = sum(1 for d in active if d.get('type_of_signal') == 'ham_2a')
                ham_60c = sum(1 for d in active if 'ham_60c' in d.get('type_of_signal'))
                ham_60cc = sum(1 for d in active if 'ham_60c' in d.get('type_of_signal'))
                ham_usdc = sum(1 for d in active if 'ham_usdc' in d.get('type_of_signal'))
                # ham_1aa = sum(1 for d in active if d.get('type_of_signal') == 'ham_1aa')
                ham_1b = sum(1 for d in active if 'ham_1b' in d.get('type_of_signal'))
                ham_brg = sum(1 for d in active if 'ham_brg' in d.get('type_of_signal'))

                limit = filter_val[deals[i]["type_of_signal"]]
                # if not time_X and deals[i]['data_s'] != 5:
                #     limit = 1
                if ('ham_1b' in deals[i]["type_of_signal"] and lenth_active<limit)\
                    or (deals[i]["type_of_signal"] == 'long_1')\
                    or (deals[i]["type_of_signal"] == 'ham_1a' and ham_1a<limit)\
                    or (deals[i]["type_of_signal"] == 'ham_1aa' and lenth_active<limit)\
                    or (deals[i]["type_of_signal"] == 'ham_5a' and ham_5a<limit)\
                    or (deals[i]["type_of_signal"] == 'ham_5b' and ham_5b<limit)\
                    or (deals[i]["type_of_signal"] == 'ham_brg' and ham_brg<limit)\
                    or (deals[i]["type_of_signal"] == 'ham_60c' and ham_60c<limit)\
                    or (deals[i]["type_of_signal"] == 'ham_60cc' and ham_60cc<limit)\
                    or ('ham_usdc' in deals[i]["type_of_signal"] and ham_usdc<limit)\
                    or (deals[i]["type_of_signal"] == 'ham_2a' and ham_2a<limit and lenth_active > 1 )\
                    or (deals[i]["type_of_signal"] == 'stub' and lenth_active<limit):

                    if len(filtered_deals)>= 2 and sv.mexc:
                        if all(d['profit']<0 and d['coin'] == deals[i]['coin'] and d['close_time']+1200000>deals[i]['open_time'] for d in filtered_deals[-2:]):
                            continue
                    if len(filtered_deals)>= 2 and sv.mexc and deals[i]["type_of_signal"] == 'ham_60c':
                        if all(d['profit']<0 and d['close_time']+1800000>deals[i]['open_time'] for d in filtered_deals[-2:]):
                            continue
                    pos = set_koof(copy.copy(deals[i]), last_7, last_0)
                    filtered_deals.append(pos)
    
    if i5:
        filtered_list = list(filter(lambda d: d['type_of_signal'] != 'stub', filtered_deals))
        for d in filtered_list:
            if d['data_s'] == 5:
                open_dt = datetime.fromtimestamp(d['open_time']/1000)
                close_dt = datetime.fromtimestamp(d['close_time']/1000)
                duration = close_dt - open_dt
                print(f'Profit: {d["profit"]} Duration: {duration.total_seconds()/60}')
                d['type_of_signal'] = 'ham_long'
    else:
        filtered_list = filtered_deals
    return recount_saldo(filtered_list)


def calc_med_duration(positions):
    durations = []
    for pos in positions:
        durations.append(pos['close_time']-pos['open_time'])

    return round((sum(durations) / len(durations)) /60000, 2)

def recount_saldo(filtered_deals):
    if len(filtered_deals)>0:
        sv.days_gap = {}
        filtered_deals[0]['saldo'] = filtered_deals[0]['profit']
        monthly_saldo = {}
        month_deal_count = {}

        for i in range(1, len(filtered_deals)):
            dt1 = datetime.fromtimestamp(filtered_deals[i]['open_time']/1000)
            dt2 = datetime.fromtimestamp(filtered_deals[i-1]['open_time']/1000)
            days = abs(dt1 - dt2).days
            month_year = (dt1.year, dt1.month)

            if days in sv.days_gap:
                sv.days_gap[days]+=1
            else:
                sv.days_gap[days]=1

            filtered_deals[i]['saldo'] = filtered_deals[i-1]['saldo']+filtered_deals[i]['profit']

            # Update monthly saldo
            if month_year in monthly_saldo:
                monthly_saldo[month_year] += filtered_deals[i]['profit']
            else:
                monthly_saldo[month_year] = filtered_deals[i]['profit']

            if month_year in month_deal_count:
                month_deal_count[month_year] += 1
            else:
                month_deal_count[month_year] = 1

        sv.month_profit = {k: monthly_saldo[k] for k in sorted(monthly_saldo)}
        sv.month_deal_count = {k: month_deal_count[k] for k in sorted(month_deal_count)}
        return filtered_deals

def set_koof(position, types_7_last, types_0_last):
    types_7 = [val['type_of_signal'] for val in types_7_last]
    types_0 = [val['type_of_signal'] for val in types_0_last]

    time_X = 'ham_1a' in types_7 or 'ham_2a' in types_7 or 'ham_5b' in types_7 or 'ham_5a' in types_7

    if position['data_s'] == 5:
        position["profit"]*=2
    elif position["type_of_signal"] in ['ham_2a', 'ham_5b', 'ham_1a'] and not time_X:
        position["profit"]*=0.25
    elif position["type_of_signal"] in ['ham_2a', 'ham_5b', 'ham_1a'] and time_X:
        position["profit"]*=2
    elif 'ham_5a' == position["type_of_signal"] and not time_X:
        position["profit"]*=0.25
    elif 'ham_5a' == position["type_of_signal"] and time_X:
        position["profit"]*=1.5
    elif 'ham_usdc' == position["type_of_signal"] and time_X:
        position["profit"]*=2
    elif 'ham_usdc' == position["type_of_signal"] and not time_X:
        position["profit"]*=0.5 if not sv.mexc else 2
    elif 'ham_usdc_1' == position["type_of_signal"] and time_X:
        position["profit"]*=1 if not sv.mexc else 1.5
    elif 'ham_usdc_1' == position["type_of_signal"] and not time_X:
        position["profit"]*=0.5 if not sv.mexc else 1
    elif 'ham_60c' ==  position["type_of_signal"] and any(p['coin'] == position["coin"] for p in types_0_last) and sv.mexc: #???
        position["profit"]*=0.5
    elif 'ham_60c' ==  position["type_of_signal"]:
        position["profit"]*=1
    else:
        position["profit"]*=1
    return position

def collect_all_types(positions, start, finish, dict_collection):
    types_dict = {}
    for i in range(start, finish):
        type_of_signal = positions[i]['type_of_signal']
        if type_of_signal in types_dict:
            types_dict[type_of_signal]+=1
        else:
            types_dict[type_of_signal]=1
    dict_3 = {k: types_dict.get(k, 0) + dict_collection.get(k, 0) for k in set(types_dict) | set(dict_collection)}
    return dict_3

def dangerous_moments(positions: list) -> dict:
    amount = sv.settings.amount
    dict_collection = {}
    start = 0
    finish = 0
    drowdowns = []
    highest_moment = 0
    lowest_moment = 0
    for i, pos in enumerate(positions):
        if pos['saldo'] > highest_moment:
            percentage = ((highest_moment-lowest_moment) / amount)*100
            if percentage > 30:
                dict_collection = collect_all_types(positions, start, finish, dict_collection)
            drowdowns.append(highest_moment-lowest_moment)
            highest_moment = pos['saldo']
            lowest_moment = pos['saldo']
            start = i
        elif pos['saldo'] < lowest_moment:
            lowest_moment = pos['saldo']
            finish = i

    counter_150 = 0
    counter_100 = 0
    counter_90 = 0
    counter_80 = 0
    counter_70 = 0
    counter_60 = 0
    counter_50 = 0
    counter_40 = 0
    counter_30 = 0
    counter_20 = 0
    counter_10 = 0
    counter_8 = 0
    counter_6 = 0
    counter_4 = 0
    counter_2 = 0
    
    for drdw in drowdowns:
        percentage = (drdw / amount)*100
        if percentage > 150:
            counter_150 += 1
        elif percentage > 100:
            counter_100 +=1
        elif percentage > 90:
            counter_90 +=1
        elif percentage > 80:
            counter_80 += 1
        elif percentage > 70:
            counter_70 += 1
        elif percentage > 60:
            counter_60 += 1
        elif percentage > 50:
            counter_50 += 1
        elif percentage > 40:
            counter_40 += 1
        elif percentage > 30:
            counter_30 += 1
        elif percentage > 20:
            counter_20 += 1
        elif percentage > 10:
            counter_10 += 1
        elif percentage > 8:
            counter_8 += 1
        elif percentage > 6:
            counter_6 += 1
        elif percentage > 4:
            counter_4 += 1
        elif percentage > 2:
            counter_2 += 1
        
    down_result = {
    'counter_150': counter_150,
    'counter_100': counter_100,
    'counter_90': counter_90,
    'counter_80': counter_80,
    'counter_70': counter_70,
    'counter_60': counter_60,
    'counter_50': counter_50,
    'counter_40': counter_40,
    'counter_30': counter_30,
    'counter_20': counter_20,
    'counter_10': counter_10,
    'counter_8': counter_8,
    'counter_6': counter_6,
    'counter_4': counter_4,
    'counter_2': counter_2
    }
    return down_result, dict_collection

def stat_of_close(positions):
    close_types = {}
    data_5 = 0
    for pos in positions:
        if pos['data_s'] == 5:
            data_5 += 1
        if pos['type_close'] in close_types:
            close_types[pos['type_close']]+=1
        else:
            close_types[pos['type_close']] = 1
    print(f'data_s 5 = {data_5}')
    return close_types
