from numpy import sqrt, vectorize, absolute, log, ones, zeros, array, sum, diag
from scipy.optimize import curve_fit
from scipy.misc import derivative
from scipy.stats import chi2

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
    if df is None:
        if dx is not None:
            df=lambda x, *popt: derivative(f, x, dx=10**-4, order=5, args=popt)
        else:
            df=zeros(len(x))

    if dx is None:
        dx=zeros(len(x))

    # Eseguo il fit
    sigma_eff = dy
    for i in range(nit):
        popt, pcov = curve_fit(f, x, y, p0, sigma_eff, absolute_sigma=absolute_sigma)
        sigma_eff = sqrt(dy**2 + (df(x, *popt)*dx)**2)

    if (chi2pval==False):
        return popt, pcov
    else:
        dpopt = sqrt(diag(pcov))
        chi = sum(((f(x,*popt)-y)/sigma_eff)**2)
        pvalue = chi2.cdf(chi,len(x))
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
        df=lambda x, *popt: derivative(f, x, dx=1e-4, order=5, args=popt)
    if dx is not None: dy=sqrt(dy**2 + (df(x, *popt)*dx)**2)
    chi = sum(((f(x,*popt)-y)/dy)**2)
    pvalue=chi2.cdf(chi,len(x))
    return chi, pvalue