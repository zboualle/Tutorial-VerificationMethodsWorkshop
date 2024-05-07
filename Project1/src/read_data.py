
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


filepath = '../data/merged_step_24hrs.txt'
df = pd.read_csv(filepath)

ecmwf_cols = [ df.columns[ii][0:6] == "ECMWF_" for ii in range(len(df.columns))]
df_ecmwf = df[df.columns[ecmwf_cols]]

ukmet_cols = [ df.columns[ii][0:6] == "UKMet_" for ii in range(len(df.columns))]
df_ukmet = df[df.columns[ukmet_cols]]

bias_ecmwf = [ df[col] - df["OBS"]  for col in  df.columns[ecmwf_cols] ]
print("Bias ECMWF members",np.mean(bias_ecmwf,axis=1))

bias_ukmet = [ df[col] - df["OBS"]  for col in  df.columns[ukmet_cols] ]
print("Bias ECMWF members",np.mean(bias_ukmet,axis=1))
