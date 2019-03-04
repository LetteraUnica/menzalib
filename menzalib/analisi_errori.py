from numpy import sqrt, absolute, log, ones, zeros, empty, array, sum, diag, reshape, identity, zeros_like, diagflat, transpose, dot
from numpy.linalg import multi_dot
from scipy.optimize import curve_fit
from scipy.stats import chi2
from numdifftools.nd_algopy import Gradient, Derivative
from inspect import signature

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

#Author Lorenzo Cavuoti
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

#Author Lorenzo Cavuoti
def dpoli(x, dx, a, da=0):
    """
    Esegue l'errore sulla funzione f(x)=x^a
    In ordine i parametri sono:
    x, errore_x, a, errore_a (Opzionale, default=0).
    La funzione accetta tuple, array, array di numpy e restituisce un array di numpy

    Es: Calcolo dell'errore su (1 +- 0.1)^2

    >>> import menzalib afrom numdifftools.nd_algopy import Gradient, Derivative mz
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

#Author Lorenzo Cavuoti
def dlog(x, dx, base="e"):
    """
    Esegue l'errore sulla funzione f(x)=log(x)
    In ordine i parametri sono:
    x, errore_x, base(Opzionale, default="e").
    La funzione accetta tuple, array, array di numpy e restituisce un array di numpy

    Es: Calcolo dell'errore su log(1 +- 0.1)

    >>> import menzalib as mz
    >>> mz.dlog(1, 0.1)        'inspect'
    0.1
    >>> mz.dlog([1,2,3], [0.1, 0.2, 0.3])
    array([0.1, 0.1, 0.1])

    Errore su f(x) = log_10(1 +- 0.2)
    >>> mz.dlog(1, 0.2, 10)np.linalg
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

#Author Lorenzo Cavuoti
def d_dB(x, dx):
    """
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

#Author Francesco Sacco, Lorenzo Cavuoti
def jacobiana(f,x):
    x=array(x, dtype=float)
    if x.ndim!=0 and len(signature(f).parameters) == len(x):
        def g(x): return f(*x)
        return jacobiana(g,x)
        
    y=array(f(x), dtype=float) #per far diventare tutto un array di numpy
    if (y.ndim==0) and (x.ndim==0): return Derivative(f)(x) #se f:R->R
    if (y.ndim==0): return Gradient(f)(x)#se f:Rn->R
    if (x.ndim==0): J=empty(len(y))  #se f:R->Rn    
    else: J=empty([len(y),len(x)])   #se f:Rn->Rm inizializzo la jacobiana
    
    for riga in range(len(y)):
        def f_ridotta(x): #restringo f in una sua componente f_ridotta=f[riga]
            return f(x)[riga]
        J[riga]=Gradient(f_ridotta)(x) #metto il grandiente nella riga
    return J

#Author Lorenzo Cavuoti, Francesco Sacco
def dy(f, x, pcov,jac=None):
    x, pcov = array(x, dtype=float), array(pcov, dtype=float) #per far diventare tutto un array di numpy
    if jac==None: J = jacobiana(f,x) #se la giacobiana non è stata fornita me la calcolo
    else: # Vedo quanti argomenti ha jac e li immetto come vettore x
        if x.ndim!=0 and len(signature(jac).parameters) == len(x):
            def g(x): return jac(*x)
            return dy(f, x, pcov, g)
        J=jac(x) #prendo la giacobiana calcolata in x

    if pcov.ndim==0: return pcov*J
    if pcov.ndim==1: pcov=diagflat(pcov) # Creo una matrice diagonale con gli errori
    if x.ndim!=0 and len(signature(f).parameters) == len(x): # Vedo quanti argomenti ha f e li immetto come vettore x
        def g(x): return f(*x)
        return dy(g, x, pcov, jac)

    return sqrt(multi_dot([J,pcov,transpose(J)])) # Ritorno la matrice di covarianza



