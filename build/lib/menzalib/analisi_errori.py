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
        return absolute(dx/x)
    else:
        base = array(base)
        if (all(base<=0)):
            print("Errore: Base del logaritmo negativa!")
            return
        return absolute(dx/(x*log(base)))

def d_dB(x, dx):
    """
    d_dB(x, dx)
    Esegue l'errore sulla funzione f(x)=20*log_10(x), utile per fare l'errore sui decibel
    In ordine i parametri sono:
    x, errore_x
    La funzione accetta tuple, array, array di numpy e restituisce un array di numpy

    Es: Calcolo dell'errore su 20*log(1+-0.1) (Errore sulla conversione di 1 +- 0.1 in decibel)

    >>> import menzalib as mz
    >>> mz.d_dB(1, 0.1)
    0.8685889638065035
    >>> mz.d_dB([1,2,3], [0.1, 0.2, 0.3])
    [0.86858896 0.86858896 0.86858896]
    """

    x, dx = array(x), array(dx)
    return absolute(20 * dx/(x*log(10)))

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