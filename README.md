# Menzalib

## Descrizione della libreria
Questa libreria e' stata creata da studenti del corso di Laboratorio 3 dell'universita' di Pisa per velocizzare la stesura delle relazioni, contiene funzioni che potrebbero risultare utili pure a corsi come Laboratorio 1 e 2  

Si possono trovare funzioni che calcolano l'errore associato alle misure con multimetro digitale e oscilloscopio, [**funzioni per errori di misura**](https://github.com/LetteraUnica/menzalib/wiki/Errori-di-Misura). 

Funzioni che propagano l'errore delle operazioni matematiche piu' comuni come prodotto, logaritmo ecc... [**funzioni propagazione errori**](https://github.com/LetteraUnica/menzalib/wiki/Propagazione-errori).  

Una funzione che esegue il `curve_fit` considerando anche gli errori sulla x e un'altra funzione che calcola chi2 e p\_value [**funzioni di fit**](https://github.com/LetteraUnica/menzalib/wiki/Funzioni-di-fit).  

Infine funzioni che permettono stampare una tabella in LaTeX senza dover riscrivere tutti i dati tra $ ed & [**Funzioni LaTeX**](https://github.com/LetteraUnica/menzalib/wiki/Funzioni-per-latex).

Per imparare come funziona la libreria andare sulla [**Wiki**](https://github.com/LetteraUnica/menzalib/wiki)

## Dimostrazione
Calcolo dell'errore di $y=f(x)=x^2 + 1/\sin(x)$ con $x=2 \pm 0.1$
```python
def f(x):
   return x**2 + 1/np.sin(x)
y = f(2)
dy = mz.dy(f, x=2, dx=0.1)
print(f"{y} +- {dy}")
```
Output:
```python
5.099750170294616 +- 0.4503309
```

## Installazione
scrivere su terminale `pip install menzalib`

