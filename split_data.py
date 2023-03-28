import csv
from datetime import datetime, timedelta
import pandas as pd
import sys
df = pd.read_csv('data/GBPUSD_20211231.csv', sep='\t', usecols=['<DATE>', '<TIME>','<BID>','<ASK>','<FLAGS>'])


df.rename(columns = {'<DATE>':'DATE'}, inplace = True)
df.rename(columns = {'<TIME>':'TIME'}, inplace = True)
df.rename(columns = {'<BID>':'BID'}, inplace = True)
df.rename(columns = {'<ASK>':'ASK'}, inplace = True)
df.rename(columns = {'<FLAGS>':'FLAGS'}, inplace = True)
df['DateTime_tran'] = df['DATE'] + ' ' + df['TIME']
# df.drop(['DATE'], axis = 1)
# df.drop(['TIME'], axis = 1)
df.drop(df.columns[[0, 1]], axis=1, inplace=True)
df['DateTime_tran'] = pd.to_datetime(df['DateTime_tran'])
df = df.set_index(df['DateTime_tran'])
print("Lenghth", len(df))

df = df[df['FLAGS'] == 6][:-1]
# df.drop(df['FLAGS'],inplace=True)
df.drop(['FLAGS'], axis=1, inplace=True)
prev_index = df.index[0]
first_index = df.index[0]
last_index = df.index[-1]
delta = timedelta(days=1)
current_date =first_index.to_pydatetime()
while current_date < last_index.to_pydatetime():
    print(current_date)
    current_day = str(current_date.year) +  str(current_date.month).rjust(2, '0') + str(current_date.day).rjust(2, '0')
    future_time = current_date + timedelta(seconds=100800)
    df.query("DateTime_tran >= @current_date and DateTime_tran < @future_time").sort_index(ascending=True).to_csv(f'data/splitted/{current_day}.csv')
    current_date += delta

