from scipy.stats import chi2
from scipy.misc import derivative
from numpy import sqrt, sum

#NON TESTATA, POTREBBE CONTENERE ERRORI
#funzione che gli dai i dati e la funzione fittata e ti ritorna chi2 e pval
#Aut
def chi2_pval(f,x,y,dy,popt,dx=None,df=None):
	if (df is None) and (dx is not None):
		df=lambda x, *popt: derivative(f, x, dx=1e-4, order=5, args=popt)
	if (df is not None) and (dx is not None): dy=sqrt(dy**2 + (df(x, *popt)*dx)**2)
	
	chi = sum(((f(x,*popt)-y)/dy)**2)
	#chi=0
	#for i in range (len(x)):
	#	chi=chi+(f(x[i],*popt)-dy[i])**2/dy[i]
	pvalue=chi2.cdf(chi,len(x))
	return chi, pvalue