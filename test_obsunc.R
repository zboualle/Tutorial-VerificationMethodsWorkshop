library(dplyr)
source("PertEns.R")

# Reading data
filepath <- '../Project1/data/merged_step_24hrs.txt'
df <- read.csv(filepath)

# Calculating ECMWF and UKMet mean squared errors

ens <- as.matrix(df %>% select(contains('ECMWF')))

#perturb the ensemble
delta_x <- 18 # grid-resolution in km
sigma <- sigma_TP(delta_x)
ens_new <- perturb_TP(ens,sigma)

ens_sd = mean(apply(ens,1,sd))
ens_new_sd = mean(apply(ens_new,1,sd))
