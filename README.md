Come installare:

Aprire terminale e inserire pip install menzalib

Funzioni:

#########################	FUNZIONI PER ERRORI DI MISURA 	################
dRdig(R) computa l'errore sulla misura di resistenza del multimetro digitale
supponendo di utilizzare la scala appropriata per la misura

dVdig(R) computa l'errore sulla misura di ddp del multimetro digitale
supponendo di utilizzare la scala appropriata per la misura

dVosc(V) computa l'errore sulla misura di voltaggio dell'oscilloscopio

dtosc(t) computa l'errore sulla misura del tempo dell'oscilloscoppio

dCdic(C,unit='nanofarad') calcola l'errore sulla misura della capacità del
multimetro digitale. il parametro opzionale "unit" se cambiato porta la scala
da nanoFarad a Farad


######################	FUNZIONI PROPAGAZIONE ERRORI 	##################
drapp(x, dx, y, dy) propaga l'errore su x/y
dprod(x, dx, y, dy) propaga l'errore su x*y
dpoli(x, dx, a) propaga l'errore su x^a
dlog(x, dx) propaga l'errore sul logaritmo naturale di x
dlog10(x, dx) propaga l'errore sul logaritmo in base 10 di x

int_rette(popt1,popt2,pcov1,pcov2)
Calcola l'intersezione di due rette y=mx+q con errore sulla x
popt1,popt2: Parametri ottimali della retta dove popt[0]=q e popt[1]=m
pcov1,pcov2: Matrice di covarianza dei parametri della retta

############################	FUNZIONI DI FIT 	#####################
curve_fitdx(f, x, y, dx=None, dy=None, df=None, p0=None, nit=None, absolute\_sigma=None)
f: Funzione di fit
x: Variabile dove la y è misurata
y: Variabile dipendente dalla x f(x, ...)
dx: Opzionale, errori sulla x, default=0
dy: Opzionale, errori sulla y, default=None
df: Opzionale, derivata della funzione di fit, se vengono dati errori sulla x senza specificare la derivata quest'ultima viene fatta numericamente
p0: Opzionale, parametri iniziali di fit, default=None
nit: Opzionale, numero di iterazioni del ciclo for per propagare le incertezze efficaci, default=10
absolute_sigma: Opzionale, default=False



chi2_pval(f, x, y, dy, popt, dx=None, df=None)
calcola il chi2 e il pvalue di un fit di una funzione f con parametri ottimali popt

f: Funzione di fit
x: Variabile dove la y è misurata
y: Variabile dipendente dalla x f(x, ...)
dy: Errori sulla y
popt: Parametri ottimali del fit
dx: Opzionale, errori sulla x, default=0
df: Opzionale, derivata della funzione di fit, se vengono dati errori sulla x senza specificare la derivata quest'ultima viene fatta numericamente

############################# FUNZIONI LATEX 	##########################
ns_tex(n,nrif)
funzione della notazione scientifica di un singolo numero con un numero di riferimento nrif
	ad esempio se nrif=500 e n=4896 stampa n con l'ordine di grandezza di nrif, cioè ritorna
	48.96 X 10^2
	
ne_tex(x,dx) torna una stringa latex bellina con il valore x e l'errore

mat_tex(Matrice,titolo=None,file=None)
stampa su terminale una matrice fatta di stringhe per latex
Matrice: matrice fatta di stringhe contenente tutti i valori
titolo: Opzionale, il titolo della tabella
file: Opzionale, file in cui la matrice viene stampata (ATTENZIONE SOVRASCRIVE IL FILE!)