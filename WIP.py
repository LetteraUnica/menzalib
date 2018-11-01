from scipy.stats import chi2  

#NON TESTATA, POTREBBE CONTENERE ERRORI
#funzione che gli dai i dati e la funzione fittata e ti ritorna chi2 e pval
#Aut
def chi2_pval(f,x,y,dy,popt,dx=None,df=None):
	if (df is None) and dx:
    	df=lambda x, *popt: derivative(f, x, dx=1e-4, order=5, args=popt)
	if df and dx: dy=sqrt(dy**2 + (df(x, *popt)*dx)**2)
	chi2=0
	for i in range (len(x)):
		chi2=chi2+(f(x[i],*popt)-dy[i])**2/dy[i]
	pvalue=chi2.cdf(chi2,len(x))
	return chi2, pvalue