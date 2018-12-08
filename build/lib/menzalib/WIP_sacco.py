from numpy import empty
from numpy.linalg import multi_dot

'''la derivata parziale richiede una funzione f,
una variabile x_i rispetto al quale fare la derivata
e un punto in cui calcolare la derivata
'''
def derviata_parziale(f,x_i,punto,dx=1e-4):
	argomenti=punto
	def f_ridotta(x):
		argomenti[x_i]=x_i	#questo serve per rendere f(*argomenti) dipendente da x
		return f(*argomenti)
	return derivative(f_ridotta,punto[x_i],dx=dx)

def gradiente(f,punto,dx=1e-4):
	grad=empty(len(punto))
	for i in range(len(punto)):
		grad[i]=derviata_parziale(f,i,punto,dx=dx)
	return grad

#assicurati che J è orientata bene
def jacobiana(f,punto,dx=1e-4):
	J=empty([len(punto),len(f(punto))])
	for riga in range(len(J)):
		def f_ridotta(f,punto):
			return f(punto)[riga]
		J[riga]=gradiente(f_ridotta,punto,dx=dx)
	return J

def prop_err(f,punto,covarianza,dx=1e-4,J=jacobiana(f,punto,dx=dx))
	return multi_dot(J,covarianza,transpose(J))