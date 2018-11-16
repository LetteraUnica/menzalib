import numpy as np
from numpy import linspace, sqrt, sort, vectorize, absolute, log, ones, zeros, array, round, floor, log10, transpose, sum
from numpy.linalg import multi_dot
from scipy.optimize import curve_fit
from scipy.misc import derivative
from scipy.stats import chi2
import pylab as pl

# Errore della misura di ddp del multimetro digitale
# supponendo che si sia scelta la scala corretta
# Author: Francesco Sacco
def errore_ddp_digitale(V):
	if V<0.2: return sqrt(V**2*25e-6+1e-8)
	if V<2:   return sqrt(V**2*25e-6+1e-6)
	if V<20:  return sqrt(V**2*25e-6+1e-4)
	if V<200: return sqrt(V**2*25e-6+1e-2)
	print("Tollerati valori minori di 200V")
	return
dVdig=vectorize(errore_ddp_digitale)

# Errore della misura di resistenza del multimetro digitale
# supponendo che si sia scelta la scala corretta
# Author: Francesco Sacco
def errore_res_digitale(R):
	if R<200: return sqrt(R**2*64e-6+9e-2)
	if R<2e3: return sqrt(R**2*64e-6+1)
	if R<2e4: return sqrt(R**2*64e-6+1e2)
	if R<2e5: return sqrt(R**2*64e-6+1e4)
	if R<2e6: return sqrt(R**2*64e-6+1e6)
	if R<2e7: return sqrt(R**2*1e-4+1e8)
	print("Tollerati valori minori di 2*10^7 ohm")
	return
dRdig=vectorize(errore_res_digitale)

# Errore della misura di capacità del multimetro digitale
# supponendo che si sia scelta la scala corretta
# La capacità deve essere data in nanoFarad
# Author: Francesco Sacco
def errore_capacita(C):
	ep=C*0.04 #questo è l'errore percentuale
	for i in range(0,5): # Non raggiunge 10^5 ma si ferma a 10^4
		if C<2*10**i: return sqrt(ep**2+9*10**(i*2-6))
	print("Tollerati valori minori di 20 micro farad")
	return
dCdig=vectorize(errore_capacita)

# Errore della misura di voltagio dell'oscilloscopio
# supponendo che si sia scelta la scala coarse corretta
# i.e. quella dove il segnale si vede meglio senza che questo esca dallo schermo
# Author: Francesco Sacco
def errore_osc_volt(V):
	scala=sort([2e-3,2e-2,2e-1,2,5e-3,5e-2,5e-1,5,1e-2,1e-1,1])
	for i in scala:
		if V<i*8:
			return sqrt((V*0.04)**2+(i/10)**2)
	print("Tollerati valori minori di 40V")
	return	
dVosc=vectorize(errore_osc_volt)


# Errore della misura del lempo dell'oscilloscopio
#Author:Francesco Sacco
def errore_osc_tempo(t):
	## da 5ns a 50s comprendente 1,2.5,5 *10^i
	scala=[5e-9]
	for i in range (-8,2):
		scala.append(5*10**(i))
		scala.append(2.5*10**(i))
		scala.append(10**(i))
	scala=sort(scala)
	for i in scala:
		if t<10*i:  
			return i*0.04
	print('Tempo troppo lungo')
	return
dtosc=vectorize(errore_osc_tempo)

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


# Esegue il curve fit considerando anche gli errori sulla x
# Author: Lorenzo Cavuoti
def curve_fitdx(f, x, y, dx=None, dy=None, df=None, p0=None, nit=None, abs_sigma=None):

    # Inizializzazione variabili, se la derivata
    # non è data esplicitamente la approssimo con scipy
    if df is None:
        if dx is not None:
            df=lambda x, *popt: derivative(f, x, dx=10**-4, order=5, args=popt)
        else:
            df=zeros(len(x))
    
    if dx is None:
        dx=zeros(len(x))
    
    if nit is None: 
        nit=10
    
    if abs_sigma is None:
        abs_sigma=False

    # Eseguo il fit
    sigma_eff = dy
    for i in range(nit):
        popt, pcov = curve_fit(f, x, y, p0, sigma_eff, absolute_sigma=abs_sigma)
        sigma_eff = sqrt(dy**2 + (df(x, *popt)*dx)**2)

    return popt, pcov


"""funzione che gli dai la funzione con punti sperimentali con errore 
	e lui ti ritorna il chi2"""
#Author: Francesco Sacco, Lorenzo Cavuoti
def chi2_pval(f,x,y,dy,popt,dx=None,df=None):
	if (df is None) and (dx is not None):
		df=lambda x, *popt: derivative(f, x, dx=1e-4, order=5, args=popt)
	if dx is not None: dy=sqrt(dy**2 + (df(x, *popt)*dx)**2)
	chi = sum(((f(x,*popt)-y)/dy)**2)
	pvalue=chi2.cdf(chi,len(x))
	return chi, pvalue


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
			   -1/(m1-m2), (q1-q2)/(m1-m2)**2])
	x=(q2-q1)/(m1-m2)
	y=(q2*m1-q1*m2)/(m1-m2)
	dx=sqrt(multi_dot([gradientex,pcov,gradientex]))
	return ([x,y,dx])


#funzione della notazione scientifica di un singolo numero con un numero di riferimento nrif
"""ad esempio se nrif=500 e n=4896 stampa n con l'ordine di grandezza di nrif, cioè ritorna
	48.96 X 10^2"""
#Author: Francesco Sacco
def notazione_scientifica_latex(n,nrif):
	exp=int(floor(log10(absolute(nrif))))#guardo l'ordine di grandezza di nrif
	if absolute(exp)==1: exp=0 #nel caso l'esponente è uno o meno uno non uso la n.s.
	n=n/10**exp #porto n nell'ordine di grandezza di nrif
	n=round(n,2)#arrotondo alla seconda cifra dopo la virgola
	if exp==0: return "$"+str(n)+"$"
	return "$"+str(n)+"\\times 10^{"+str(exp)+"}$" #ritorna la stringa in latex
#vettorizzo
ns_tex=vectorize(notazione_scientifica_latex)



#funzione della notazione scientifica di un valore x con errore
#stampa una stringa contenente i due valori stampati per bene in latex
#Author: Francesco Sacco
def numero_con_errore_latex(x,dx):
	exp=int(floor(log10(absolute(x))))#guardo l'ordine di grandezza di x
	if absolute(exp)==1: exp=0 #nel caso l'esponente è uno o meno uno non uso la n.s.
	x=x/10**exp     #porto la virgola dopo la prima cifra
	dx=dx/10**exp   #porto la virgola dove si trova quella della x
	cifr=int(floor(log10(absolute(dx))))  #guardo l'ordine di grandezza di dx
	#taglio le di x con un ordine di grandezza inferiore a dx
	x=round(x,absolute(cifr))       
	dx=round(dx,absolute(cifr)) #taglio le cifre significative di dx dopo la prima
	#ritorno la stringa in latex
	if exp==0:
		return  "$"+str(x)+"\\pm"+str(dx)+"$" 
	return  "$("+str(x)+"\\pm"+str(dx)+")\\times 10^{"+str(exp)+"}$"
#vettorizzo la funzione
ne_tex=vectorize(numero_con_errore_latex)


#Funzione che stampa una matrice fatta di stringhe in un formato comodo per latex
#Author: Francesco Sacco
def stampa_matrice_latex(M):
	tipo_tabella='{'+(len(M)*'c')+'}'
	M=transpose(M)
	print('\n\nCopia tutto quello che c\'è tra le linee')
	print('--------------------------')
	print('\\begin{tabular}'+tipo_tabella)
	print('\\hline\n % qua ci va il titolo della tabella (ricorda di mettere \\\\ alla fine) %\n \\hline')
	for colonna in M:
		stringa='\t'
		for numero in colonna:
			stringa=stringa+numero+' & '
		print(stringa[:-2]+'\\\\')
	print('\\end{tabular}\n--------------------------\n\n')
   