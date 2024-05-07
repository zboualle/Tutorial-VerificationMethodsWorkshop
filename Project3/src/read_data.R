# Reading data
path <- '../data/'
files <- list.files(path, pattern = '*.txt', full.names = TRUE)
df <- read.csv(files[[1]])

# Computing mean squared error
err_harmonie <- df$HARMONIE - df$WSP_OBS
err_hirlam <- df$HIRLAM5 - df$WSP_OBS
mean(sqrt(err_harmonie^2), na.rm = TRUE)
mean(sqrt(err_hirlam^2), na.rm = TRUE)
