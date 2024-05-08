
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

datapath = '../data/Proj4_t2m-{centre}-JJA-1959-2001.txt'
cols = ["year", "observation"]+ list( ["mem%s"%i for i in range(0,9)])

df_ecmwf = pd.read_table(datapath.format(centre="ecmwf"),header=None,sep=" ",names=cols)
df_mf = pd.read_table(datapath.format(centre="mf"),header=None,sep=" ",names=cols)
df_ukmo = pd.read_table(datapath.format(centre="ukmo"),header=None,sep=" ",names=cols)
