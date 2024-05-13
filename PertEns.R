#import random
#import numpy as np
#import copy

truncnorm_rvs <- function(loc,shape,clip_a,max_iterations=100,random_state=np.random){
    jiter <- 1
    rd_field <- rnorm(length(loc),mean=loc, sd=shape)
    mask <- rd_field < clip_a
    while ( sum(mask)>1){
        if ( jiter>max_iterations) {
            rd_field[mask] <-0.
            break
            #("Maximum number of iterations exceeded.")
        }
        rd_field[mask] <- rnorm(sum(mask), mean = loc[mask], sd = shape[mask])
        mask <- rd_field < clip_a
        jiter <- jiter +1
    }
    return( rd_field )
}

perturb_10FF <- function(eo,sigma){
    if( is.null(dim(e))){
        e <- array(e, dim=c(length(e),1))
    }
    for (j in 1:dim(e)[2]){
        f0 <- e[,j]
        f0 [ eo[,j] < 0. ]<- 0.
        f0 [ is.finite(eo[,j]) == False ] <- 0.

        clip_a <- 0
        clip_b <- 1000
        loc <- sigma[1] + sigma[2] * f0
        loc[loc<clip_a] <- clip_a
        shape  <-  abs(sigma[3] + sigma[4] * f0**sigma[4])

        rdField <- truncnorm_rvs(loc, shape, clip_a)

        rdField [ rdField < 0 ]=0
        e[,j] <- e[,j]*0 + rdField
    }
    return(e)
}

perturb_2T <- function(e,sigma){
        if( is.null(dim(e))){
            e <- array(e, dim=c(length(e),1))
        }
        for (j in 1:dim(e)[2]){
           e[,j] = e[,j] + rnorm( dim(e)[1], mean=0, sd = sigma)
        }
        return(e)
}

perturb_TP <- function(e,sigma){
    if( is.null(dim(e))){
        e <- array(e, dim=c(length(e),1))
    }
    nmem <- dim(e)[2]

    for (j in 1:nmem){
           f0 <- e[,j]
           f0 [ e[,j] < 0. ] <- 0.

           mu     <- sigma[1] + sigma[2] * f0
           sig_sq <- sigma[3] + sigma[4] * f0**0.5

           shape  <- (mu**2)/(sig_sq**2)
           scale  <- sig_sq**2/mu

           shape [ sig_sq == 0. ] <- 0.
           scale [ mu     == 0. ] <- 0.

           rdField <- rgamma(dim(e)[1], shape, scale=scale) - sigma[4]
           rdField [ rdField < 0 ] <- 0.
           e[,j] <- e[,j]*0. + rdField
    }
    return(e)
}


sigma_2T <- function(deltax){
        beta0 <- min(0.02*deltax,2.)
        beta1 <- max(0.35 -0.002*deltax,0.15)
        powtr <- 0.25
        sigma <- c(beta0, beta1, powtr)
        return(sigma)
}

sigma_10FF <- function(deltax){
        alpha0 <- deltax * -0.02
        alpha1 <- 1. + deltax *  0.002
        beta0  <- 0.00001
        beta1  <- 0. + deltax * - 0.04 + deltax**0.75 * 0.17
        powtr  <- 0.5
        sigma  <- c(alpha0, alpha1, beta0, beta1, powtr)
        return(sigma)
}

sigma_TP <- function(deltax,period=24){
        if (period == 24){
            alpha0 <- 0.005*deltax**0.5
            alpha1 <- 1.
            beta0  <- 0.0005*deltax
            beta1  <- -0.02* deltax + 0.55 *deltax**0.5
            delta  <- 0.005*deltax**0.5
        } else if( period == 12){
            alpha0 <- 0.115
            alpha1 <- 1.
            beta0  <- 0.002
            beta1  <- 0.055 -0.02* deltax + 0.44 *deltax**0.5
            delta  <- 0.5 + 0.002*deltax
        } else if(period == 6){
            alpha0 <- 0.15
            alpha1 <- 1.
            beta0  <- 0.001*deltax
            beta1  <- -0.015* deltax + 0.4 *deltax**0.5
            delta  <- 0.4
        }else {
            print("  *** Observation uncertainty parameters unknown for that accumulation period ***")
            Stop
        }
        sigma  <- c(alpha0, alpha1, beta0, beta1,delta)
        return(sigma)
}

orographyCorrection <- function(e,morog,oorog){
    if( is.null(dim(e)) ){
        e <- array(e, dim=c(length(e),1))
    }
    nmem <- dim(e)[2]
    for (j in 1:nmem){
        e[,j] = e[,j] + (morog-oorog)*0.0065
    }
    return(e)
}

orographyCorrectionEnsemble <- function(e,morog,oorog,sigma){
    sigmaO <- sigma[1] + sigma[2]*abs(morog-oorog)**sigma[3]
    if( is.null(dim(e))){
        e <- array(e, dim=c(length(e),1))
    }
    nmem <- dim(e)[2]
    for (j in 1:nmem){
        e[,j] = e[,j] + rnorm(length(morog), mean = 0, sd = sigmaO)
    }
    return(e)
}
