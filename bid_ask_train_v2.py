import csv
from datetime import datetime
from datetime import datetime, timedelta
import pandas as pd
import sys,shutil


import pandas as pd
from datetime import datetime, timedelta
import sys,os
import datetime

files_ ="data/splitted"
for file_ in os.listdir(files_):
    os.system('cls')
    print(f' Current File In Execution: {file_}')
    df = pd.read_csv(os.path.join(files_,file_)) # usecols=['<DATE>', '<TIME>','<BID>','<ASK>','<FLAGS>']) 
    if len(df) ==0:
        print(f'Empty File In Execution Moving To Next File')
        print(f'Moving file: {files_}/{file_} to arch folder')
        shutil.move(f'{files_}/{file_}', f'data/arch/{file_}')
        
        continue

    df['DateTime_tran'] =pd.to_datetime(df['DateTime_tran'])
    df = df.set_index(df['DateTime_tran'])
    #TODO Need to change the line above as all the formatting is done in the file by other code.
    # df.rename(columns = {'<DATE>':'DATE'}, inplace = True)
    # df.rename(columns = {'<TIME>':'TIME'}, inplace = True)
    # df.rename(columns = {'<BID>':'BID'}, inplace = True)
    # df.rename(columns = {'<ASK>':'ASK'}, inplace = True)
    # df.rename(columns = {'<FLAGS>':'FLAGS'}, inplace = True)

    

    print("Lenghth", len(df))

    # df = df[df['FLAGS'] == 6][:-1]
    # # df.drop(df['FLAGS'],inplace=True)
    # df.drop(['FLAGS'], axis=1, inplace=True)

    df['Predicted_Buy'] = 1
    df['Predicted_Sell'] = 1 

    df['Buy_Profit_1Min'] = 0
    df['Sell_Profit_1Min'] = 0

    df['Buy_Profit_5Min'] = 0
    df['Sell_Profit_5Min'] = 0

    df['Buy_Profit_15Min'] = 0
    df['Sell_Profit_15Min'] = 0

    df['Buy_Profit_30Min'] = 0
    df['Sell_Profit_30Min'] = 0

    df['Buy_Profit_60Min'] = 0
    df['Sell_Profit_60Min'] = 0

    df['Buy_Profit_240Min'] = 0
    df['Sell_Profit_240Min'] = 0

    df['Buy_Profit_1Min_dt'] =pd.Timestamp('1900-01-01 0:00.00')
    df['Sell_Profit_1Min_dt'] = pd.Timestamp('1900-01-01 0:00.00')

    df['Buy_Profit_5Min_dt'] =pd.Timestamp('1900-01-01 0:00.00')
    df['Sell_Profit_5Min_dt'] = pd.Timestamp('1900-01-01 0:00.00')

    df['Buy_Profit_15Min_dt'] =pd.Timestamp('1900-01-01 0:00.00')
    df['Sell_Profit_15Min_dt'] = pd.Timestamp('1900-01-01 0:00.00')

    df['Buy_Profit_30Min_dt'] =pd.Timestamp('1900-01-01 0:00.00')
    df['Sell_Profit_30Min_dt'] = pd.Timestamp('1900-01-01 0:00.00')

    df['Buy_Profit_60Min_dt'] =pd.Timestamp('1900-01-01 0:00.00')
    df['Sell_Profit_60Min_dt'] = pd.Timestamp('1900-01-01 0:00.00')

    df['Buy_Profit_240Min_dt'] =pd.Timestamp('1900-01-01 0:00.00')
    df['Sell_Profit_240Min_dt'] = pd.Timestamp('1900-01-01 0:00.00')

    for i in range(0,17):
        print(f'cols {i}:, {df.columns[i]}')
    # for i in range(17,29):
    #     print(f'cols {i}:, {df.columns[i]}')
    pip = 250
    point = 0.00001 # This value is supposed to be populated through MetaTrader
    pips = pip * point
    print("-------",len(df))
    i = 0
    prev_index = df.index[0]
    first_index = df.index[0]
    # print(df)
    # print(type(first_index))
    for index, row  in df.iterrows():
        if (index.to_pydatetime() - first_index.to_pydatetime()).seconds >= 86400:
            break
        datem = row.DateTime_tran.to_pydatetime()
        bid = row.BID
        ask = row.ASK
        future_times =[]
        future_times.append(datem + timedelta(minutes =1))
        future_times.append(datem + timedelta(minutes =5))
        future_times.append(datem + timedelta(minutes =15))
        future_times.append(datem + timedelta(minutes =30))
        future_times.append(datem + timedelta(minutes =60))
        future_times.append(datem + timedelta(minutes =240))
        # print(future_times)
        
        i += 1
        j = 6 # Buy 1 minute start condition
        for future_time in future_times:
            row_minute_buy = df.query("DateTime_tran >= @datem and DateTime_tran < @future_time and BID > @bid + @pips").sort_index(ascending=True)
            if not row_minute_buy.empty:
                for k in range(j,17,2):
                    df.loc[index, df.columns[k]] = 1
                    df.loc[index, df.columns[k+12]] = row_minute_buy.index[0].to_pydatetime()
                    
                break
            j += 2
        j = 7 # Sell 1 minute start condition
        for future_time in future_times:
            row_minute_sell = df.query("DateTime_tran >= @datem and DateTime_tran < @future_time and ASK < @ask - @pips").sort_index(ascending=True) 
            if not row_minute_sell.empty:
                for k in range(j,17,2):
                    df.loc[index, df.columns[k]] = 1
                    df.loc[index, df.columns[k+12]] = row_minute_sell.index[0].to_pydatetime()
                    
                break
            j += 2
        if i % 10000 == 0: 
            # df.to_csv(f'data/processed/{file_}')
            print(f'For file: {file_} Records done {i}, time: {datetime.datetime.now()} , from : {prev_index} - to: {index}')
            prev_index = index
        
        
    df.to_csv(f'data/processed/{file_}')
    print(f'Moving file: {files_}/{file_} to arch folder')
    shutil.move(f'{files_}/{file_}', f'data/arch/{file_}')

    

