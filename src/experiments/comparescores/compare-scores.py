""" Compares two Mosamatic score CSV files
"""
import os
import pandas as pd

FILE1 = 'MW-scores-20240105-1230.csv'
FILE2 = 'MD-scores-20240105135514057.csv'

df1 = pd.read_csv(FILE1)
df1 = df1.drop(df1.columns[0], axis=1)

columns = ['muscle_area', 'vat_area', 'sat_area', 'muscle_ra', 'vat_ra', 'sat_ra']

def get_row_items(row):
    items = []
    for column in columns:
        items.append(str(row[column]))
    return items

data1 = {}
for idx, row in df1.iterrows():
    filePath = row['file']
    fileName = os.path.split(filePath)[1]
    data1[fileName] = get_row_items(row)

df2 = pd.read_csv(FILE2)

data2 = {}
for idx, row in df2.iterrows():
    filePath = row['file']
    fileName = os.path.split(filePath)[1]
    data2[fileName] = get_row_items(row)

for key in data1.keys():
    fileMatch = True
    for i in range(6):
        value1 = data1[key]
        value2 = data2[key]
        if value1 != value2:
            print(f'mismatch: {value1} != {value2}')
            fileMatch = False
    print(f'Files match: {fileMatch}')