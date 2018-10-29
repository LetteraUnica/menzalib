Come installare:

Aprire terminale e inserire pip install menzalib

Funzioni:
dRdig(R) computa l'errore sulla misura di resistenza del multimetro digitale
supponendo di utilizzare la scala appropriata per la misura

dVdig(R) computa l'errore sulla misura di ddp del multimetro digitale
supponendo di utilizzare la scala appropriata per la misura

dVosc(V) computa l'errore sulla misura di voltaggio dell'oscilloscopio

dTosc(t) computa l'errore sulla misura del tempo dell'oscilloscoppio (WIP)

drapp(x, dx, y, dy) propaga l'errore su x/y
dprod(x, dx, y, dy) propaga l'errore su x*y
dpoli(x, dx, a) propaga l'errore su x^a
dlog(x, dx) propaga l'errore sul logaritmo naturale di x
dlog10(x, dx) propaga l'errore sul logaritmo in base 10 di x


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
