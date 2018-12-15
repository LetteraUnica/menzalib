from numpy import sqrt, vectorize, absolute, log, ones, zeros, array, sum, diag
from numpy.linalg import multi_dot
from scipy.optimize import curve_fit
from scipy.misc import derivative
from scipy.stats import chi2


# Author: Lorenzo Cavuoti
def drapp(x, dx, y, dy):
    """
    Esegue l'errore sul rapporto di due numeri.
    In ordine i parametri sono:
    numeratore, errore_numeratore, denominatore, errore_denominatore.
    La funzione accetta tuple, array, array di numpy e restituisce un array di numpy

    Es: Calcolo dell'errore su (1 +- 0.1) / (2 +- 0.3)

    >>> import menzalib as mz
    >>> mz.drapp(1, 0.1, 2, 0.3)
    array(0.09013878)
    >>> mz.drapp([1,2,3], [0.1, 0.2, 0.3], 10, 0.5)
    array([0.01118034, 0.02236068, 0.03354102])
    """

    x, dx = array(x), array(dx)
    y, dy = array(y), array(dy)
    return 1/y**2 * sqrt((y*dx)**2 + (x*dy)**2)


def dprod(x, dx, y, dy):
    """
    Esegue l'errore sul prodotto di due numeri x*y.
    In ordine i parametri sono:
    x, errore_x, y, errore_y.
    La funzione accetta tuple, array, array di numpy e restituisce un array di numpy

    Es: Calcolo dell'errore su (1 +- 0.1) * (2 +- 0.3)

    >>> import menzalib as mz
    >>> mz.dprod(1, 0.1, 2, 0.3)
    array(0.36055513)
    >>> mz.prod([1,2,3], [0.1, 0.2, 0.3], 10, 0.5)
    array([1.11803399, 2.23606798, 3.35410197])
    """
    x, dx = array(x), array(dx)
    y, dy = array(y), array(dy)
    return sqrt((y*dx)**2 + (x*dy)**2)


def dpoli(x, dx, a, da=0):
    """
    Esegue l'errore sulla funzione f(x)=x^a
    In ordine i parametri sono:
    x, errore_x, a, errore_a (Opzionale, default=0).
    La funzione accetta tuple, array, array di numpy e restituisce un array di numpy

    Es: Calcolo dell'errore su (1 +- 0.1)^2

    >>> import menzalib as mz
    >>> mz.dpoli(1, 0.1, 2)
    array(0.2)
    >>> mz.poli([1,2,3], [0.1, 0.2, 0.3], 4)
    array([ 0.4,  6.4, 32.4])
    >>> mz.dpoli(1, 0, 2, 0.3)
    array(0.4158883083359672)
    """
    x, dx = array(x), array(dx)
    a, da = array(a), array(da)
    return absolute(a*x**(a-1)*dx) + absolute(log(x)*x**a*da)

print(dpoli(2,0,3,0.2))

def dlog(x, dx, base="e"):
    """
    Esegue l'errore sulla funzione f(x)=log(x)
    In ordine i parametri sono:
    x, errore_x, base(Opzionale, default="e").
    La funzione accetta tuple, array, array di numpy e restituisce un array di numpy

    Es: Calcolo dell'errore su log(1 +- 0.1)

    >>> import menzalib as mz
    >>> mz.dlog(1, 0.1)
    0.1
    >>> mz.dlog([1,2,3], [0.1, 0.2, 0.3])
    array([0.1, 0.1, 0.1])

    Errore su f(x) = log_10(1 +- 0.2)
    >>> mz.dlog(1, 0.2, 10)
    0.08685889638065036
    """

    x, dx = array(x), array(dx)
    if (base=="e"):
        return dx/x
    else:
        base = array(base)
        if (all(base<=0)):
            print("Errore: Base del logaritmo negativa!")
            return
        return absolute(dx/(x*log(base)))

#Author: Francesco Sacco
def int_rette(popt1,popt2,pcov1,pcov2):
    """
    Calcola l'intersezione ed errore tra due rette indipendenti
	con equazioni y=x*m1+q1 e y=x*m2+q2
    In ordine i parametri sono:
    popt1 : Parametri ottimali della prima retta
    popt2 : Parametri ottimali della seconda retta
    pcov1 : Matrice di covarianza della prima retta
    pcov2 : Matrice di covarianza della seconda retta
    """
    q1,q2=popt1[0],popt2[0]     # Forse bisogna invertire 1 con 0?
    m1,m2=popt1[1],popt2[1]
    pcov=zeros((4,4))
    pcov[:2,:2]=pcov1
    pcov[2:,2:]=pcov2
    gradientex=([1/(m1-m2),-(q1-q2)/(m1-m2)**2,
                -1/(m1-m2),(q1-q2)/(m1-m2)**2])
    x=(q2-q1)/(m1-m2)
    y=(q2*m1-q1*m2)/(m1-m2)
    dx=sqrt(multi_dot([gradientex,pcov,gradientex]))
    return x,y,dx


# Author: Lorenzo Cavuoti
def curve_fitdx(f, x, y, dx=None, dy=None, df=None, p0=None, nit=10, absolute_sigma=False, chi2pval=False):
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
