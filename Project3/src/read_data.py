import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

datapath = '../data/'
projections = range(3,48+1,3)
for proj in projections:
    print("projection:",proj)
    df = pd.read_csv(f'../data/Projection_{proj}h.txt')
    print("ECMWF bias:",np.mean(df["ECM_IS"]-df["WSP_OBS"]))
