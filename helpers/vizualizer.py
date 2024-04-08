import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
import matplotlib.dates as mdates
from datetime import datetime
import uuid
import os
import shared_vars as sv
from PIL import Image
import helpers.statistic_count as stat
import numpy as np
from matplotlib.ticker import MultipleLocator
from matplotlib.dates import MonthLocator

binance_dark = {
    "base_mpl_style": "dark_background",
    "marketcolors": {
        "candle": {"up": "#3dc985", "down": "#ef4f60"},  
        "edge": {"up": "#3dc985", "down": "#ef4f60"},  
        "wick": {"up": "#3dc985", "down": "#ef4f60"},  
        "ohlc": {"up": "green", "down": "red"},
        "volume": {"up": "#247252", "down": "#82333f"},  
        "vcedge": {"up": "green", "down": "red"},  
        "vcdopcod": False,
        "alpha": 1,
    },
    "mavcolors": ("#ad7739", "#a63ab2", "#62b8ba"),
    "facecolor": "#1b1f24",
    "gridcolor": "#2c2e31",
    "gridstyle": "--",
    "y_on_right": True,
    "rc": {
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.edgecolor": "#474d56",
        "axes.titlecolor": "red",
        "figure.facecolor": "#161a1e",
        "figure.titlesize": "x-large",
        "figure.titleweight": "semibold",
    },
    "base_mpf_style": "binance-dark",
}

def draw_candlesticks_positions(candles: list, trades: list, title: str):
    images = []
    for trade in trades:
        coin = trade['coin']
        open_time = float(trade['open_time'])
        close_time = float(trade['close_time'])
        direction = trade['signal']
        profit = trade['profit']
        data_s = trade['data_s']
        index_open = next((i for i, v in enumerate(candles) if float(v[0]) == open_time), None)
        index_close = next((i for i, v in enumerate(candles) if float(v[0]) == close_time), None)
        if index_close == None or index_open == None:
            continue
        # if profit > 0:
        #     continue
        plot_candles = candles[index_open-10:index_close+11]
        
        df = pd.DataFrame(plot_candles, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

        df['Date'] = pd.to_datetime(df['Date'], unit='ms')
        df.set_index('Date', inplace=True)

        markers_buy = [np.nan]*len(df)
        markers_sell = [np.nan]*len(df)
        
        if direction == 1:
            markers_buy[10] = df['Low'].iloc[10]
            markers_sell[-11] = df['High'].iloc[-11]
        else:
            markers_buy[10] = df['High'].iloc[10]
            markers_sell[-11] = df['Low'].iloc[-11]


        addplot_buy = None
        addplot_sell = None
        if direction == 1:
            addplot_buy = mpf.make_addplot(markers_sell, panel=0, type='scatter', markersize=200, color='w', marker='v')
            addplot_sell = mpf.make_addplot(markers_buy, panel=0, type='scatter', markersize=200, color='w', marker='^')
        else:
            addplot_buy = mpf.make_addplot(markers_buy, panel=0, type='scatter', markersize=200, color='w', marker='v')
            addplot_sell = mpf.make_addplot(markers_sell, panel=0, type='scatter', markersize=200, color='w', marker='^')
        tt = f'{data_s} sg:{direction} pr:{profit}'
        if not os.path.exists(f'_pic/{coin}/'):
            os.makedirs(f'_pic/{coin}/')
        uid = uuid.uuid4()
        filename = f'_pic/{coin}/{uid}.png'
        mpf.plot(df, type='candle', style=binance_dark, title=tt, addplot=[addplot_buy, addplot_sell], savefig=filename)
        images.append(Image.open(filename))

    # Combine 6 images into one
    while len(images) >= 6:
        new_img = Image.new('RGB', (3 * images[0].width, 2 * images[0].height))
        for i in range(6):
            new_img.paste(images[i], ((i % 3) * images[i].width, (i // 3) * images[i].height))
            os.remove(images[i].filename)  # remove the image after pasting it
        new_img.save(f'_pic/{coin}/combined_{uuid.uuid4()}.png')
        images = images[6:]

    # If there are remaining images, save them as well
    if images:
        new_img = Image.new('RGB', (3 * images[0].width, 2 * images[0].height))
        for i in range(len(images)):
            new_img.paste(images[i], ((i % 3) * images[i].width, (i // 3) * images[i].height))
            os.remove(images[i].filename)  # remove the image after pasting it
        new_img.save(f'_pic/{coin}/combined_{uuid.uuid4()}.png')

def draw_candlesticks(candles: list, type_labels: str, mark_index: int):
    # Convert the candlesticks data into a pandas DataFrame
    df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=False).dt.tz_localize('UTC').dt.tz_convert('Europe/London')
    df.set_index('timestamp', inplace=True)
    figsize = (10, 6)
    # Plot the candlestick chart using mpf.plot()
    fig, axlist = mpf.plot(df, type='candle', style=binance_dark, title=type_labels, returnfig=True, figsize=figsize)

    if type_labels == 'up':
        axlist[0].annotate('MARK', (mark_index, df.iloc[mark_index]['open']), xytext=(mark_index, df.iloc[mark_index]['open']-10),
                    arrowprops=dict(facecolor='black', arrowstyle='->'))
    elif type_labels == 'down':
        axlist[0].annotate('MARK', (mark_index, df.iloc[mark_index]['open']), xytext=(mark_index, df.iloc[mark_index]['open']+10),
                        arrowprops=dict(facecolor='black', arrowstyle='->'))

    # Display the chart
    mpf.show()

def plot_time_series(data_list: list, save_pic: bool, points: int, dont_show: bool, data_items: dict, data_items_2: dict):
    path = f'_pic/{datetime.now().date().strftime("%Y-%m-%d")}'
    timestamps = [item['open_time'] for item in data_list]
    values = [item['saldo'] for item in data_list]
    report = stat.proceed_positions(data_list)
    # Преобразование timestamp в формат даты
    dates = [datetime.fromtimestamp(ts/1000) for ts in timestamps]
    if len(dates) >= 2:
        if dates[0].year < 2017:
            dates[0] = dates[1]
    # Создание графика
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(MonthLocator(interval=2))  # каждый второй месяц
    ax.yaxis.set_major_locator(MultipleLocator(15))  # больше горизонтальных линий
    plt.xticks(rotation=45)  # Поворот дат для лучшей читаемости
    periods = range(1, len(values) + 1)
    cell_text = []
    for key, value in data_items.items():
        cell_text.append([key, '', value])
    table = plt.table(cellText=cell_text,
                  loc='upper left',
                  edges='open')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(0.8, 0.8)
    table.auto_set_column_width([0, 1, 2])

    if len(data_items_2)>0:
        cell_text2 = []
        for key, value in data_items_2.items():
            cell_text2.append([key, '', value])
        table2 = plt.table(cellText=cell_text2,
                    loc='lower right',
                    edges='open')
        table2.auto_set_font_size(False)
        table2.set_fontsize(8)
        table2.scale(0.8, 0.8)
        table2.auto_set_column_width([0, 1, 2])

    # Построение графика
    ax.plot(dates, values, linewidth=0.8)
    
    # Добавление подписей и заголовка
    plt.xlabel('Period')
    plt.ylabel('Value')
    plt.title(f"{report}", fontsize=5.5)

    # Add periods close to the dates
    # for i, (date, value) in enumerate(zip(dates, values)):
    #     if i % points == 0:
    #         ax.text(date, value, f"{i}", verticalalignment='top', horizontalalignment='center', fontsize=9, color='red')
    
    # Add grid lines
    ax.grid(True)
    
    # Отображение графика
    if not dont_show:
        plt.tight_layout()

    if save_pic:
        if not os.path.exists(path):
            os.makedirs(path)
        end_path = f'{path}/{datetime.now().timestamp()}{sv.unique_ident}.png'
        plt.savefig(end_path)
        plt.close(fig)
        return end_path
    if not dont_show:
        plt.show()
        plt.close(fig)
    return None