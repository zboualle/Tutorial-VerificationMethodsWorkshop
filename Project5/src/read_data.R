
#read data
step = 24
datafile <- paste0('../data/Project5_fobs_jja2022_step',step,'_00.csv')
climfile <- paste0('../data/Project5_clim_jja2022_step',step,'_00.csv')

data <- read.csv(datafile, header = TRUE)
clim <- read.csv(climfile, header = TRUE)


#compute SEEPS
seeps_mtx = clim[6:14]

ob_ind <- (data["OBS"] > clim["t1"])*1 + (data["OBS"]  >= clim["t2"])*1
fc_ind <- (data["FCT_ifs"] > clim["t1"])*1 + (data["FCT_ifs"]  >= clim["t2"])*1

indices <- fc_ind * 3 + ob_ind + 1

seeps_all <- array(dim=c(length(indices)))
for ( jj in 1:length(indices) ){
    if (! is.na(indices[jj]) ) {
        seeps_all[jj] <- seeps_mtx[jj,indices[jj]]
    }
}
mean(seeps_all,na.rm=TRUE)
