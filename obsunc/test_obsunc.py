
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PertEns import *

#read data
filepath = '../Project1/data/merged_step_24hrs.txt'
df = pd.read_csv(filepath)

ens_cols = [ df.columns[ii][0:6] == "ECMWF_" for ii in range(len(df.columns))]
ens = df[df.columns[ens_cols]].values

#perturb the ensemble
delta_x = 18 # grid-resolution in km
sigma = sigma_TP(delta_x)
ens_new = perturb_TP(ens,sigma)

#check impact
std_ens = ens.std(axis=1).mean()
std_ens_new = ens_new.std(axis=1).mean()
