from numpy import sqrt, sort, vectorize

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

def errore_capacita(C):
	ep=C*0.04 #questo è l'errore percentuale
	for i in range(-9,-5):
	    if C<2*10**i: return sqrt(ep**2+9*10**(i*2-6))
	print("Tollerati valori minori di 50 micro farad")
	return

dCdig=vectorize(errore_capacita)

def errore_osc_volt(V):
	scala=sort([2e-3,2e-2,2e-1,2,5e-3,5e-2,5e-1,5,1e-2,1e-1,1])
	for i in range(0,len(scala)):
		if V<scala[i]*8:
			return sqrt((V*0.04)**2+(scala[i]/10)**2)
	print("Tollerati valori minori di 40V")
	return
	
dVosc=vectorize(errore_osc_volt)
