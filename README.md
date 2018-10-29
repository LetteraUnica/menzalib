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
