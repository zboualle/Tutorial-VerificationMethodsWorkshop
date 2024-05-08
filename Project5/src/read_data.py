import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

datapath = '../data/Project5_fobs_jja2022_step{step}_00.csv'
climpath = '../data/Project5_clim_jja2022_step{step}_00.csv'

step = 24

df_fobs = pd.read_csv(datapath.format(step=step))
df_clim = pd.read_csv(climpath.format(step=step))

#SEEPS
# local 3x3 SEEPS matrices
seeps_mtx = np.zeros((len(df_clim),9))
for ii in range(9):
    seeps_mtx[:,ii] = df_clim[f"value_{ii}"]

#SEEPS for FCT_ifs
ob_ind = (df_fobs["OBS"] > df_clim["t1"]).astype(int) + (df_fobs["OBS"]  >= df_clim["t2"]).astype(int)
fc_ind = (df_fobs["FCT_ifs"] > df_clim["t1"]).astype(int) + (df_fobs["FCT_ifs"]  >= df_clim["t2"]).astype(int)

indices = fc_ind * 3 + ob_ind
seeps_all = np.array([ seeps_mtx[jj,idx] for jj,idx in enumerate(indices)])
seeps = np.nanmean(seeps_all,axis=0)
