import pandas as pd
import glob,os

path = 'Data/processed' # use your path
# all_files = os.path.join(path, "/*.csv")

li = []

for filename in os.listdir(path):
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

multi_df = pd.concat(li, axis=0, ignore_index=True)