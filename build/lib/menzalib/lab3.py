from numpy import sqrt, sort, vectorize, absolute, log, ones, zeros, array,round,floor,log10
from scipy.optimize import curve_fit
from scipy.misc import derivative

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
# Author: Francesco Sacco
def errore_capacita(C):
	ep=C*0.04 #questo è l'errore percentuale
	for i in range(-9,-5):
	    if C<2*10**i: return sqrt(ep**2+9*10**(i*2-6))
	print("Tollerati valori minori di 50 micro farad")
	return

dCdig=vectorize(errore_capacita)

# Errore della misura di voltagio dell'oscilloscopio
# supponendo che si sia scelta la scala coarse corretta
# i.e. quella dove il segnale si vede meglio senza che questo esca dallo schermo
# Author: Francesco Sacco
def errore_osc_volt(V):
	scala=sort([2e-3,2e-2,2e-1,2,5e-3,5e-2,5e-1,5,1e-2,1e-1,1])
	for i in range(0,len(scala)):
		if V<scala[i]*8:
			return sqrt((V*0.04)**2+(scala[i]/10)**2)
	print("Tollerati valori minori di 40V")
	return
	
dVosc=vectorize(errore_osc_volt)

# Propagazione di incertezze in alcune funzioni utili
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
def curve_fitdx(f, x, y, dx=None, dy=None, df=None, p0=None, nit=None, absolute_sigma=None):

    # Inizializzazione variabili, se la derivata
    # non è data esplicitamente la approssimo con scipy
    if df is None:
        if dx:
            df=lambda x, *popt: derivative(f, x, dx=10**-4, order=5, args=popt)
        else:
            df=zeros(len(x))
    
    if dx is None:
        dx=zeros(len(x))
    
    if nit is None: 
        nit=10
    
    if absolute_sigma is None:
        abs_sigma=False

    # Eseguo il fit
    sigma_eff = dy
    for i in range(nit):
        popt, pcov = curve_fit(f, x, y, p0, sigma_eff, absolute_sigma=abs_sigma)
        sigma_eff = sqrt(dy**2 + (df(x, *popt)*dx)**2)

    return popt, pcov


#funzione della notazione scientifica di un singolo numero con un numero di riferimento nrif
"""ad esempio se nrif=500 e n=4896 stampa n con l'ordine di grandezza di nrif, cioè ritorna
    48.96 X 10^2"""
#Author: Francesco Sacco
def notazione_scientifica_latex(n,nrif):
    exp=int(floor(log10(nrif)))#guardo l'ordine di grandezza di nrif
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
    exp=int(floor(log10(x)))#guardo l'ordine di grandezza di x
    x=x/10**exp     #porto la virgola dopo la prima cifra
    dx=dx/10**exp   #porto la virgola dove si trova quella della x
    cifr=int(floor(log10(dx)))  #guardo l'ordine di grandezza di dx
    #taglio le di x con un ordine di grandezza inferiore a dx
    x=round(x,absolute(cifr))       
    dx=round(dx,absolute(cifr)) #taglio le cifre significative di dx dopo la prima
    #ritorno la stringa in latex
    if exp==0:
        return  "$"+str(x)+"\\pm"+str(dx)+"$" 
    return  "$("+str(x)+"\\pm"+str(dx)+")\\times 10^{"+str(exp)+"}$"
#vettorizzo la funzione
ne_tex=vectorize(numero_con_errore_latex)










