# Title     : Data ingestion
# Created by: Gabriel Perez
# Created on: 20/05/2021
library(dplyr)

path <- '../data/Project_2_data_'
files <- list.files(path, pattern = '*.txt', full.names = TRUE)
projections <- c(24, 48, 72, 96, 120)
df_list <- list()
i <- 1
for (projection in projections){
  df <- read.table(paste(path, projection, 'h.txt', sep=''), header = TRUE )
  df$projection <- projection
  df_list[[i]] <- df
  i <- i + 1
}
df <- bind_rows(df_list)
