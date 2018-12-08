from numpy import sqrt, vectorize, absolute, log, ones, zeros, array, sum, diag
from numpy.linalg import multi_dot
from scipy.optimize import curve_fit
from scipy.misc import derivative
from scipy.stats import chi2


# Author: Lorenzo Cavuoti
def errore_rapporto(x, dx, y, dy):
	return 1/y**2 * sqrt((y*dx)**2 + (x*dy)**2)
drapp=vectorize(errore_rapporto)


def errore_prodotto(x, dx, y, dy):
	return sqrt((y*dx)**2 + (x*dy)**2)
dprod=vectorize(errore_prodotto)


def errore_polinomiale(x, dx, a):
	return absolute(a*x**(a-1)*dx)
dpoli=vectorize(errore_polinomiale)


def errore_logaritmo(x, dx):
	return dx/x
dlog=vectorize(errore_logaritmo)


def errore_logaritmo10(x, dx):
	return dx/(x*log(10))
dlog10=vectorize(errore_logaritmo10)


"""funzione che calcola l'intersezione ed errore tra due rette indipendenti
	con equazioni y=x*m1+q1 e y=x*m2+q2"""
#Authonr: Francesco Sacco
def int_rette(popt1,popt2,pcov1,pcov2):
	q1,q2=popt1[0],popt2[0]
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


# Esegue il curve fit considerando anche gli errori sulla x
# Author: Lorenzo Cavuoti
def curve_fitdx(f, x, y, dx=None, dy=None, df=None, p0=None, nit=10, abs_sigma=False, chi2pval=False):

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
        popt, pcov = curve_fit(f, x, y, p0, sigma_eff, absolute_sigma=abs_sigma)
        sigma_eff = sqrt(dy**2 + (df(x, *popt)*dx)**2)

    if (chi2pval==False):
		return popt, pcov
    else:
		dpopt = sqrt(diag(pcov))
		chi = sum(((f(x,*popt)-y)/dy)**2)
		pvalue=chi2.cdf(chi,len(x))
		return popt, pcov, dpopt, chi, pvalue




"""funzione che gli dai la funzione con punti sperimentali con errore 
	e ti ritorna il chi2"""
#Author: Francesco Sacco, Lorenzo Cavuoti
def chi2_pval(f,x,y,dy,popt,dx=None,df=None):
	if (df is None) and (dx is not None):
		df=lambda x, *popt: derivative(f, x, dx=1e-4, order=5, args=popt)
	if dx is not None: dy=sqrt(dy**2 + (df(x, *popt)*dx)**2)
	chi = sum(((f(x,*popt)-y)/dy)**2)
	pvalue=chi2.cdf(chi,len(x))
	return chi, pvalue
