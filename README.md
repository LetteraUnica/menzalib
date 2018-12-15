# Come installare:

Aprire terminale e inserire `pip install menzalib`


### FUNZIONI PER ERRORI DI MISURA

`dRdig(R)` Computa l'errore sulla misura di resistenza del multimetro digitale
supponendo di utilizzare la scala appropriata per la misura

`dVdig(V)` Computa l'errore sulla misura di ddp del multimetro digitale
supponendo di utilizzare la scala appropriata per la misura

`dVosc(V)` Computa l'errore sulla misura di voltaggio dell'oscilloscopio
supponendo di utilizzare la scala "coarse" appropriata per la misura

`dtosc(t)` Computa l'errore sulla misura del tempo dell'oscilloscoppio
supponendo di utilizzare la scala "coarse" appropriata per la misura

`dCdic(C,unit='nanofarad')` Calcola l'errore sulla misura della capacità del
multimetro digitale. Il parametro opzionale "unit" se cambiato porta la scala
da nanoFarad a Farad


### FUNZIONI PROPAGAZIONE ERRORI

`drapp(x, dx, y, dy)` Propaga l'errore su x/y
```python
# Es: Calcolo dell'errore su (1 +- 0.1) / (2 +- 0.3)
>>> import menzalib as mz
>>> mz.drapp(1, 0.1, 2, 0.3)
array(0.09013878)
>>> mz.drapp([1,2,3], [0.1, 0.2, 0.3], 10, 0.5)
array([0.01118034, 0.02236068, 0.03354102])
```

`dprod(x, dx, y, dy)` Propaga l'errore su x*y

```python
# Es: Calcolo dell'errore su (1 +- 0.1) * (2 +- 0.3)
>>> import menzalib as mz
>>> mz.dprod(1, 0.1, 2, 0.3)
array(0.36055513)
>>> mz.prod([1,2,3], [0.1, 0.2, 0.3], 10, 0.5)
array([1.11803399, 2.23606798, 3.35410197])
```


`dpoli(x, dx, a, da=0)` Propaga l'errore su x^a, di default l'errore sull'esponente è nullo
```python
# Es: Calcolo dell'errore su (1 +- 0.1)^2
>>> import menzalib as mz
>>> mz.dpoli(1, 0.1, 2)
array(0.2)
>>> mz.poli([1,2,3], [0.1, 0.2, 0.3], 4)
array([ 0.4,  6.4, 32.4])

# Es: Calcolo dell'errore su 2^(3+-0.2)
>>> mz.dpoli(2, 0, 3, 0.2)
1.1090354888959124
```

`dlog(x, dx, base="e")` Propaga l'errore sul logaritmo naturale di x

```python
# Es: Calcolo dell'errore su log(1 +- 0.1)
>>> import menzalib as mz
>>> mz.dlog(1, 0.1)
0.1
>>> mz.dlog([1,2,3], [0.1, 0.2, 0.3])
array([0.1, 0.1, 0.1])

# Es: Errore su f(x) = log_10(1 +- 0.2) (base 10)
>>> mz.dlog(1, 0.2, 10)
0.08685889638065036
```



`int_rette(popt1,popt2,pcov1,pcov2)`  
Calcola l'intersezione di due rette y=mx+q con errore sulla x del punto di intersezione  
popt1,popt2: Parametri ottimali della retta dove popt[0]=q e popt[1]=m  
pcov1,pcov2: Matrice di covarianza dei parametri della retta

### FUNZIONI DI FIT

`curve_fitdx(f, x, y, dx=None, dy=None, df=None, p0=None, nit=None, absolute_sigma=None)`  
Esegue il curve fit considerando anche gli errori sulla x, sintassi molto simile alla funzione `curve_fit` di scipy.  
Restituisce parametri ottimali di fit e matrice di covarianza  
In ordine i parametri sono:
- f : Funzione di fit nella forma f(x, popt)
- x : Variabile indipendente dove i dati sono misurati
- y : I dati dipendenti y=f(x, ...)
- dx: Opzionale, errori sulla x dei punti sperimentali, default=None
- dy: Opzionale, errori sulla y dei punti sperimentali, default=None
- df: Opzionale, derivata della funzione di fit, deve essere nella forma df(x, popt) default: derivata approssimata numericamente
- p0: Opzionale, parametri iniziali per la routine di curve_fit, default=None
- nit: Opzionale, numero massimo di cicli per propagare le incertezze efficaci, default=10
- absolute_sigma: Opzionale, per una spiegazione dettagliata vedere la pagina sulla
    funzione curve fit di scipy, default=False
- chi2pval: Opzionale, se chi2pval=True la funzione restituisce anche, in ordine:
    errore sui parametri ottimali, chi quadro, pvalue, default=False


`chi2_pval(f, x, y, dy, popt, dx=None, df=None)`  
Calcola il chi2 e il pvalue di un fit di una funzione f con parametri ottimali popt, i parametri sono:
- f : Funzione di fit nella forma f(x, popt)
- x : Variabile indipendente dove i dati sono misurati
- y : I dati dipendenti y=f(x, ...)
- dy: Opzionale, errori sulla y dei punti sperimentali, default=None
- dx: Opzionale, errori sulla x dei punti sperimentali, default=None
- popt: Array con i parametri ottimali di fit
- dx: Opzionale, errori sulla x dei punti sperimentali, default=None
- df: Opzionale, derivata della funzione di fit, deve essere nella forma df(x, popt) default: derivata approssimata numericamente
- default: derivata approssimata numericamente

### FUNZIONI LATEX

`ns_tex(n,nrif)`  
Funzione della notazione scientifica di un singolo numero con un numero di riferimento nrif.
Ad esempio se nrif=500 e n=4896 stampa n con l'ordine di grandezza di nrif, cioè ritorna
48.96 X 10^2
	
`ne_tex(x,dx)` Torna una stringa latex bellina con il valore x e l'errore

`mat_tex(Matrice,titolo=None,file=None)`
Stampa su terminale una matrice fatta di stringhe per latex
- Matrice: matrice fatta di stringhe contenente tutti i valori
- titolo: Opzionale, il titolo della tabella
- file: Opzionale, file in cui la matrice viene stampata (ATTENZIONE SOVRASCRIVE IL FILE!)
