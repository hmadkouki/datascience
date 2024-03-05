# use packages
import bokeh
import pandas as pd
import numpy as np
import os

# open all  csv in the folder data and save them in a list
path = "data"
files = os.listdir(path)
files_csv = [f for f in files if f[-3:] == "csv"]
print(files_csv)

# create a list of pandas dataframes
data = []
for file in files_csv:
    data.append(pd.read_csv(path + "/" + file))

# print the dataframes
for i in range(len(data)):
    print(data[i])
