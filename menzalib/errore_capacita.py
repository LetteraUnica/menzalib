from numpy import vectorize,sqrt

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