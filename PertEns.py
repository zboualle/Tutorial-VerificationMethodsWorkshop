import random
import numpy as np
import copy
from PertEns import *

def truncnorm_rvs_fast(loc,shape,clip_a,max_iterations=100,random_state=np.random):
    jiter = 1
    #loc[loc<clip_a] = clip_a
    rd_field = random_state.normal(loc, shape)
    mask = rd_field < clip_a
    while mask.any():
        if jiter>max_iterations:
            rd_field[mask] =0.
            break
            raise ValueError("Maximum number of iterations exceeded.")
        rd_field[mask] = random_state.normal(loc[mask], shape[mask])
        mask = rd_field < clip_a
        jiter += 1
    return rd_field

def perturb_10FF(eo,sigma):
        e = copy.deepcopy(eo)
        for j in range(e.shape[1]):
           f0 = e[:,j]
           f0 [ np.where( eo[:,j] < 0. ) ]= 0.
           f0 [ np.where( np.isfinite(eo[:,j]) == False ) ]= 0.

           clip_a,clip_b = 0,1000
           loc = sigma[0] + sigma[1] * f0
           loc[loc<clip_a] = clip_a
           shape  =  abs(sigma[2] + sigma[3] * f0**sigma[4])

           rdField = truncnorm_rvs_fast(loc, shape, clip_a)

           rdField [np.where( rdField < 0 )]=0
           e[:,j] = eo[:,j]*0 + rdField

        return e

def perturb_2T(eo,sigma):
        e = copy.deepcopy(eo)
        for j in range(e.shape[1]):
           e[:,j] += np.random.normal(0, sigma, size=len(e[:,j]))
        return e


def perturb_TP(eo,sigma):
        e = copy.deepcopy(eo)
        for j in range(e.shape[1]):
           f0 = e[:,j]
           f0 [ np.where( eo[:,j] < 0. ) ]= 0.

           mu     = sigma[0] + sigma[1] * f0
           sig_sq = sigma[2] + sigma[3] * f0**0.5

           shape  = (mu**2)/(sig_sq**2)
           scale  = sig_sq**2/mu

           shape [np.where( sig_sq == 0. )]= 0.
           scale [np.where( mu     == 0. )]= 0.

           rdField = np.random.gamma(shape,scale) - sigma[4]
           rdField [np.where( rdField < 0 )]=0.
           e[:,j] = eo[:,j]*0. + rdField
        return e



def sigma_2T(deltax) :
        beta0 = min(0.02*deltax,2.)
        beta1 = max(0.35 -0.002*deltax,0.15)
        powtr = 0.25
        sigma = [ beta0, beta1, powtr ]

        return sigma

def sigma_10FF(deltax) :
        alpha0 = deltax * -0.02
        alpha1 = 1. + deltax *  0.002
        beta0  = 0.00001
        beta1  = 0. + deltax * - 0.04 + deltax**0.75 * 0.17
        powtr  = 0.5

        sigma  = [ alpha0, alpha1, beta0, beta1, powtr]
        return sigma

def sigma_TP(deltax,period=24) :
        if period == 24:
            alpha0 = 0.005*deltax**0.5
            alpha1 = 1.
            beta0  = 0.0005*deltax
            beta1  = -0.02* deltax + 0.55 *deltax**0.5
            delta  = 0.005*deltax**0.5
        elif  period == 12:
            alpha0 = 0.115
            alpha1 = 1.
            beta0  = 0.002
            beta1  = 0.055 -0.02* deltax + 0.44 *deltax**0.5
            delta  = 0.5 + 0.002*deltax
        elif  period == 6:
            alpha0 = 0.15
            alpha1 = 1.
            beta0  = 0.001*deltax
            beta1  = -0.015* deltax + 0.4 *deltax**0.5
            delta  = 0.4
        else:
            print("  *** Observation uncertainty parameters unknown for that accumulation period ***")
            Stop

        sigma  = [alpha0, alpha1, beta0, beta1,delta]
        return sigma

def orographyCorrection(e,morog,oorog):
    for j in range(e.shape[1]):
        e[:,j] += (morog-oorog)*0.0065
    return e

def orographyCorrectionEnsemble(e,morog,oorog,sigma):
    sigmaO = sigma[0] + sigma[1]*abs(morog-oorog)**sigma[2]
    for j in range(e.shape[1]):
        e[:,j] += np.random.normal(0, sigmaO, size=len(morog))
    return e
