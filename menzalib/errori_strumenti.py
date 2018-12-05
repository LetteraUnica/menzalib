from numpy import sqrt, vectorize, sort


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
			return i*0.04+t*5e-5+0.6e-9
	print('Tempo troppo lungo, fai prima a misurarlo a mano')
	return
dtosc=vectorize(errore_osc_tempo)


