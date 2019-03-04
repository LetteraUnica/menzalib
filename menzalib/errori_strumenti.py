from numpy import sqrt, vectorize, sort


# Author: Francesco Sacco
def errore_ddp_digitale(V):
    """
    Calcola l'errore della misura di ddp del multimetro digitale
    supponendo che si sia scelta la scala corretta.
    La ddp deve essere data in Volt
    """
    if V<0.2: return sqrt(V**2*25e-6+1e-8)
    if V<2:   return sqrt(V**2*25e-6+1e-6)
    if V<20:  return sqrt(V**2*25e-6+1e-4)
    if V<200: return sqrt(V**2*25e-6+1e-2)
    print("Tollerati valori minori di 200V")
    return
dVdig=vectorize(errore_ddp_digitale)

# Author: Francesco Sacco
def errore_res_digitale(R):
    """
    Calcola l'errore della misura di resistenza del multimetro digitale
    supponendo che si sia scelta la scala corretta.
    La resistenza deve essere data in Ohm
    """
    if R<200: return sqrt(R**2*64e-6+9e-2)
    if R<2e3: return sqrt(R**2*64e-6+1)
    if R<2e4: return sqrt(R**2*64e-6+1e2)
    if R<2e5: return sqrt(R**2*64e-6+1e4)
    if R<2e6: return sqrt(R**2*64e-6+1e6)
    if R<2e7: return sqrt(R**2*1e-4+1e8)
    print("Tollerati valori minori di 2*10^7 ohm")
    return
dRdig=vectorize(errore_res_digitale)


# Author: Francesco Sacco
def errore_osc_volt(V,scala=None):
    """
    Calcola l'errore della misura di ddp dell'oscilloscopio
    supponendo che si sia scelta la scala coarse corretta
    i.e. quella dove il segnale si vede meglio senza che questo esca dallo schermo
    La ddp deve essere data in volt
    """
    if scala!=None: return sqrt((V*0.04)**2+(scala/10)**2)
    scala=sort([2e-3,2e-2,2e-1,2,5e-3,5e-2,5e-1,5,1e-2,1e-1,1])
    for i in scala:
        if V<i*8:
            return sqrt((V*0.04)**2+(i/10)**2)
    print("Tollerati valori minori di 40V")
    return	
dVosc=vectorize(errore_osc_volt)


#Author:Francesco Sacco
def errore_osc_tempo(t,scala=None):
    """
    Calcola l'errore della misura di tempo dell'oscilloscopio
    supponendo che si sia scelta la scala corretta.
    i.e. quella dove il segnale si vede meglio senza che questo esca dallo schermo
    Il tempo deve essere dato in secondi
    """
	## da 5ns a 50s comprendente 1,2.5,5 *10^i
    if scala!=None: return scala*0.04+t*5e-5+5e-10
    scala=[5e-9]
    for i in range (-8,2):
        scala.append(5*10**(i))
        scala.append(2.5*10**(i))
        scala.append(10**(i))
    scala=sort(scala)
    for i in scala:
        if t<10*i:  
            return i*0.04+t*5e-5+5e-9
    print('Tempo troppo lungo, fai prima a misurarlo a mano')
    return
dtosc=vectorize(errore_osc_tempo)


def errore_osc_frequenza(f, scala=None, misura="cursore"):
    """
    Calcola l'errore della misura di frequenza dell'oscilloscopio
    supponendo che si sia scelta la scala corretta.
    i.e. quella dove il segnale si vede meglio senza che questo esca dallo schermo
    La frequenza deve essere data in Hertz.
    Il parametro opzionale scala serve per scegliere la scala se questa è diversa da
    quella assunta dalla funzione
    Se il parametro opzionale misura è diverso da "cursore" l'errore in frequenza
    viene dato dal trigger dell'oscilloscopio (molto preciso ma meno robusto)
    """
    if misura != "cursore" :
        return f*52*10**-6
    dt = errore_osc_tempo(1/f, scala=scala)
    return f**2 * dt
dfosc = vectorize(errore_osc_frequenza)


# Author: Francesco Sacco
def errore_capacita(C,unit='nanofarad'):
    """
    Calcola l'errore della misura di capacità del multimetro digitale
    supponendo che si sia scelta la scala corretta.
    La capacità deve essere data in nanoFarad
    Se unit ha un valore diverso sarà in Farad
    """
    ep=C*0.04 #questo è l'errore percentuale
    if unit=='nanofarad': scala=range(0,5) # Non raggiunge 10^5 ma si ferma a 10^4
    else: scala=range(-9,-5)
    for i in scala:
        if C<2*10**i: return sqrt(ep**2+9*10**(i*2-6))
    print("Tollerati valori minori di 20 micro farad")
    return
dCdig=vectorize(errore_capacita)

