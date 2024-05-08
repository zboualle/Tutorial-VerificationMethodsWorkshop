# Reading data
path <- '../data/'
file_ecmwf <- list.files(path, pattern='*ecmwf-JJA-1959-2001.txt', full.names = TRUE)
file_ukmo <- list.files(path, pattern='*ukmo-JJA-1959-2001.txt', full.names = TRUE)
file_mf <- list.files(path, pattern='*mf-JJA-1959-2001.txt', full.names = TRUE)

df_ecmwf <- read.table(file_ecmwf)
df_ukmo <- read.table(file_ukmo)
df_mf <- read.table(file_mf)
