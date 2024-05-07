import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

datapath = '../data/Project_2_data_{proj}h.txt'
ds_list = []
projections = [24, 48, 72, 96, 120]
for proj in projections:
    df = pd.read_table(datapath.format(proj=proj))
    df['Projection'] = proj
    df = df.set_index(['Date', 'Projection'])
    ds_list.append(df)
df = pd.concat(ds_list, axis=0)
