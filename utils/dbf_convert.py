from simpledbf import Dbf5
import os

files = os.listdir('../dbfs')

for f in files:
    if f[-3:].lower() == 'dbf':
        dbf = Dbf5('../dbfs/' + f)
        print(f.replace('.dbf', '.csv'))
        dbf.to_csv(f.replace('.dbf', '.csv'))
