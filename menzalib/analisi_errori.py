import numpy as np
from numpy import sqrt, absolute, log, ones, zeros, array, transpose
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



def dsomm(dx,dy):
    dx,dy=array(dx),array(dy)
    return sqrt(dx**2+dy**2)


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
        if (np.all(base<=0)):
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
    """
    Calcola la jacobiana di una funzione f in un punto x.
    Ovvero la matrice delle derivate prime di f: R^n->R^m in x
    Parametri:
    f(x, y, ...): funzione multidimensionale di cui fare la jacobiana
    x: tupla, array o numpy array che indica il punto in cui calcolare la jacobiana

    Es: Calcolare la jacobiana di f(x)=exp(x) in x=2
    >>> import numpy as np
    >>> import menzalib as mz
    >>> def f(x):
    ...     return np.exp(np.sin(x)) 
    >>> mz.jacobiana(f,2)
    7.38905609893065

    Es: Calcolo della jacobiana di g(x,y)=[sin(x)*cos(y), y*exp(x)] in (x, y) = (1, 3)
    >>> def g(x,y):
    ...     return [np.sin(x)*np.cos(y), y*np.exp(x)]
    >>> mz.jacobiana(g, [1,3])
    array([[-0.53489523, -0.11874839],
        [ 8.15484549,  2.71828183]])
    
    Casi particolari:
    Indico con J(x) la jacobiana di f in x
    Se f: R->R ==> J(x)=f'(x)
    Se f: R^n->R ==> J(x)=gradiente(f)(x)
    """
    x=array(x, dtype=float)
    # Nel caso uno scriva f(x,y, ...) invece di f(x) con x vettore
    if x.ndim!=0 and len(signature(f).parameters) == len(x):
        def g(x): return f(*x)
        return jacobiana(g,x)
        
    y=array(f(x), dtype=float) #per far diventare tutto un array di numpy
    if (y.ndim==0) and (x.ndim==0): return Derivative(f)(x) #se f:R->R
    if (y.ndim==0): return Gradient(f)(x)#se f:Rn->R
    if (x.ndim==0): J=np.empty(len(y))  #se f:R->Rn    
    else: J=np.empty([len(y),len(x)])   #se f:Rn->Rm inizializzo la jacobiana
    
    for riga in range(len(y)):
        def f_ridotta(x): #restringo f in una sua componente f_ridotta=f[riga]
            return f(x)[riga]
        J[riga]=Gradient(f_ridotta)(x) #metto il grandiente nella riga
    return J

#Author Lorenzo Cavuoti, Francesco Sacco
def dy(f, x, pcov,jac=None):
    """
    Data una variabile aleatoria x, calcola matrice di covarianza della variabile aleatoria y=f(x).
    Parametri:
    f(x, y, ...): funzione R^n->R^m che restituisce y=f(x)
    x: tupla, array o numpy array che indica il punto in cui calcolare la matrice di covarianza
    pcov: Matrice di covarianza della variabile aleatoria x, se viene dato un vettore v
        la matrice di covarianza  diagonale con la diagonale uguale a v, diag(pcov)=v
    jac, Opzionale: funzione che restituisce la matrice jacobiana della funzione f in un punto x,
        se non data la jacobiana è approssimata numericamente

    Es: Calcolo dell'errore su y=f(x)=x/(1+x**2) in x=2 +- 0.1
    In questo caso la matrice di covarianza (cov) è uno scalare tale che cov==dx**2
    dove == indica una definizione e dx indica l'errore sulla x, quindi:
    >>> import menzalib as mz
    >>> def f(x):
            return x/(1+x**2)
    >>> mz.dy(f, 2, 0.1**2)
   	0.012000000000000004
   	
   	Calcolo dell'errore su 
    


    Casi particolari:
    Indico con J(x) la jacobiana di f in x
    Se f: R->R ==> J(x)=f'(x)
    Se f: R^n->R ==> J(x)=gradiente(f)(x)
    """
    x, pcov = array(x, dtype=float), array(pcov, dtype=float) #per far diventare tutto un array di numpy
    if jac==None: J = jacobiana(f,x) #se la jacobiana non è stata fornita me la calcolo
    else: # Vedo quanti argomenti ha jac e li immetto come vettore x
        if callable(jac)==False: J=array(jac,dtype=float)#nel caso la giacobiana è una matrice
        else:#nel caso in cui la giacobiana è una funzione
            if (callable(jac)==True and x.ndim!=0 and len(signature(jac).parameters) == len(x)):
                def g(x): return jac(*x)
                return dy(f, x, pcov, g)
            J=jac(x) #prendo la giacobiana calcolata in x
    if pcov.ndim==0: return pcov*J
    if pcov.ndim==1: 
        pcov=pcov**2 #passo da deviazione standar a varianza 
        pcov=np.diagflat(pcov) # Creo una matrice diagonale con gli errori

    if x.ndim!=0 and len(signature(f).parameters) == len(x): # Vedo quanti argomenti ha f e li immetto come vettore x
        def g(x): return f(*x)
        return dy(g, x, pcov, jac)

    return multi_dot([J,pcov,transpose(J)]) # Ritorno la matrice di covarianza
