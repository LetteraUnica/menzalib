import numpy as np
from numpy import sqrt, vectorize, absolute, log, array
from scipy.optimize import curve_fit
from scipy.stats import chi2
from numdifftools.nd_algopy import Derivative

# Author: Lorenzo Cavuoti
def curve_fitdx(f, x, y, dx=None, dy=None, p0=None, df=None, nit=10, absolute_sigma=False, chi2pval=False):
    """
    Esegue il curve fit considerando anche gli errori sulla x
    Restituisce parametri ottimali di fit e matrice di covarianza
    In ordine i parametri sono:
    f : Funzione di fit nella forma f(x, popt)
    x : Variabile indipendente dove i dati sono misurati
    y : I dati dipendenti y=f(x, ...)
    dx: Opzionale, errori sulla x dei punti sperimentali, default=None
    dy: Opzionale, errori sulla y dei punti sperimentali, default=None
    df: Opzionale, derivata della funzione di fit, deve essere nella forma df(x, popt)
        default: derivata approssimata numericamente
    p0: Opzionale, parametri iniziali per la routine di curve_fit, default=None
    nit: Opzionale, numero massimo di cicli per propagare le incertezze efficaci, default=10
    absolute_sigma: Opzionale, per una spiegazione dettagliata vedere la pagina sulla
        funzione curve fit di scipy, default=False
    chi2pval: Opzionale, se chi2pval=True la funzione restituisce anche, in ordine:
        errore sui parametri ottimali, chi quadro, pvalue, default=False
    """

    # Inizializzazione variabili, se la derivata
    # non è data esplicitamente la approssimo con scipy
    if dy is None :
        dy = np.ones(len(y))

    if dx is None:
        popt, pcov = curve_fit(f, x, y, p0, dy, absolute_sigma=absolute_sigma)
        chi = np.sum(((f(x,*popt)-y)/dy)**2)
    
    else:
        if df is None:
            df=Derivative(f)
        
        # Eseguo il fit
        sigma_eff = dy
        chi, chi_old = 1., -1.
        i=0
        while (i<10 and abs(chi-chi_old)/chi > 1e-6):
            popt, pcov = curve_fit(f, x, y, p0, sigma_eff, absolute_sigma=absolute_sigma)
            sigma_eff = sqrt(dy**2 + (df(x, *popt)*dx)**2)
            chi_old = chi
            chi = np.sum(((f(x,*popt)-y)/sigma_eff)**2)
            i += 1

    if (chi2pval==False):
        return popt, pcov
    else:
        dpopt = sqrt(np.diag(pcov))
        pvalue = chi2.cdf(chi,len(x)-len(popt))
        return popt, pcov, dpopt, chi, pvalue


#Author: Francesco Sacco, Lorenzo Cavuoti
def chi2_pval(f,x,y,dy,popt,dx=None,df=None):
    """
    Calcola il chi2 e pvalue, i parametri sono:
    f : Funzione di fit nella forma f(x, popt)
    x : Variabile indipendente dove i dati sono misurati
    y : I dati dipendenti y=f(x, ...)
    dy: Opzionale, errori sulla y dei punti sperimentali, default=None
        dx: Opzionale, errori sulla x dei punti sperimentali, default=None
    popt: Array con i parametri ottimali di fit
    dx: Opzionale, errori sulla x dei punti sperimentali, default=None
    df: Opzionale, derivata della funzione di fit, deve essere nella forma df(x, popt)
        default: derivata approssimata numericamente
    """
    if (df is None) and (dx is not None):
        df=Derivative(f)
    if dx is not None: dy=sqrt(dy**2 + (df(x, *popt)*dx)**2)
    chi = np.sum(((f(x,*popt)-y)/dy)**2)
    pvalue=chi2.cdf(chi,len(x)-len(popt))
    return chi, pvalue