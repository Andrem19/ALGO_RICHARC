from binance_historical_data import BinanceDataDumper
import multiprocessing
import coins as coins
import datetime
import pandas as pd
import glob
import os

def main():
    symbols = ['BTCUSDT']
    
    times =['1d']# ['1m', '5m']#, '15m', '30m', '1h']
    for t in times:
        for symbol in symbols:
            data_dumper = BinanceDataDumper(
                path_dir_where_to_dump="newdata",
                asset_class="um",  # spot, um, cm
                data_type="klines",  # aggTrades, klines, trades
                data_frequency=t,
            )
            data_dumper.dump_data(
                tickers=symbol,
                date_start=None,
                date_end=None,
                is_to_update_existing=True,
                tickers_to_exclude=["UST"],
            )

    #====================TRANSFORM=========================
    for t in times:
        for s in symbols:
            file_list = glob.glob(f'newdata/futures/um/monthly/klines/{s}/{t}/{s}-{t}-*.csv')
            file_list.sort()
            
            if len(file_list) == 0:
                continue
            
            df_final = pd.DataFrame()

            for file_path in file_list:   
                try:
                    df = pd.read_csv(file_path, header=None, usecols=[0, 1, 2, 3, 4, 5])
                    df_final = pd.concat([df_final, df], ignore_index=True)  # Set ignore_index=True
                    
                except FileNotFoundError:
                    continue
            
            # Exclude lines containing "ignore"
            df_final = df_final[~df_final[0].astype(str).str.contains('open_time')]
            
            # Print first index in datetime format
            first_index_ms = df_final.iloc[0, 0]
            first_index_dt = datetime.datetime.fromtimestamp(int(first_index_ms) / 1000)
            print(f"First Index ({s}): {first_index_dt}")
            
            # Print last index in datetime format
            last_index_ms = df_final.iloc[-1, 0]
            last_index_dt = datetime.datetime.fromtimestamp(int(last_index_ms) / 1000)
            print(f"Last Index ({s}): {last_index_dt}")

            os.makedirs(f'_crypto_data/{s}', exist_ok=True)
            df_final.to_csv(f'_crypto_data/{s}/{s}_{t}.csv', header=False, index=False)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
