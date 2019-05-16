import numpy as np
from numpy import floor,log10,absolute,round,vectorize,transpose,array
from sys import stdout

"""
visto che la funzione str(x) ti ritorna la stringa "1e-5" se x=1e-5 ho creato questa
funzione che ti ritorna 0.00005, funziona solo per gli esponenti negativi,
prima o poi includerò quelli positivi.
Forse.
"""
#Author:Francesco Sacco
def stringhizza(x):
	s=str(x)
	e=s.find("e")#trovo quella e di merda
	if e==-1:#se non c'è è tutto bello così
		return s
	exp=int(s[e+2:])#altrimenti prendo l'esponente
	dot=s.find(".")#e vedo dov'è il punto
	if dot!=-1:#se c'è il punto
		s=s[:dot]+s[dot+1:]#lo levo dalla stringa
		return "0."+"0"*(exp-dot)+s[:e]# e ritorno il numero per bene
	return "0."+"0"*(exp-1)+s[:e]#altrimenti torno questo

#Author:Francesco Sacco
def principale(n,nrif=None,nult=None):
	if n==0: return ["0",0]
	if nrif==None:nrif=n
	if nult==None:
		if absolute(nrif)==absolute(n): nult=n/100 #ns_tex(456,456)=4.56 x 10^2
		if absolute(nrif)>absolute(n): nult=n    #ns_tex(6,572)=0.06 x 10^2
		if absolute(nrif)<absolute(n): nult=nrif #ns_tex(572,6)=572
	if nrif==0.0 or nult==0.0: 
		print('non puoi usare come numero di riferimento o numero dell\'ultima cifra lo zero')
		return principale(n)
	#se il numero di riferimento è più piccolo di quello dell'ultima cifra,
	#allora bisogna usare nrif come numero per l'ultima cifra
	if nult>nrif: nult=nrif 
	er=int(floor(log10(absolute(nrif))))#guardo l'ordine di grandezza di nrif
	#porto n nell'ordine di grandezza di nrif nel caso in cui l'esponente è 1 o -1 non uso la n.s.
	n,nult=n/10**er,nult/10**er 
	eu=int(floor(log10(absolute(nult))))#guardo l'ordine di grandezza di nult
	n=round(n,-eu)#arrotondo all'ordine di grandezza di eu
	if eu>=0: n=int(n)# se non mi interessa quello che c'è dopo la virgola (es 690\pm20)
	num=stringhizza(n)
	num=num+"0"*(-eu-len(num)+num.find(".")+1)# aggiungo gli zeri che mancano
	return [num,er] #ritorna la stringa del numero e l'esponente (x=num*10^er)

#funzione della notazione scientifica di un singolo numero con un numero di riferimento nrif
"""ad esempio se nrif=500 e n=4896 stampa n con l'ordine di grandezza di nrif, cioè ritorna
	48.96 X 10^2"""
#Author: Francesco Sacco
def notazione_scientifica_latex(n,nrif=None,nult=None):
	n,exp=principale(n,nrif,nult)
	if exp==0: return "$"+n+"$"
	return "$"+n+" \\times 10^{"+str(exp)+"}$"
#vettorizzo
ns_tex=vectorize(notazione_scientifica_latex)


#ritorna due stringe, una col valore e l'altro con l'errore fatte in modo che abbiano
#lo stesso ordine di grandezza
#Author:Francesco Sacco
def nes_tex(x,dx=None):
	if dx==None: return ns_tex(x)    
	return ns_tex(x,nult=dx), ns_tex(dx,x)


#funzione della notazione scientifica di un valore x con errore
#stampa una stringa contenente i due valori stampati per bene in latex
#questa funzione potrebbe avere errori se una delle due variabili è uguale a zero
#Author: Francesco Sacco
def numero_con_errore_latex(x,dx):
	rif=x
	if absolute(x)<1000:rif=1
	n,er=principale(x,rif,dx)
	dn=principale(dx,rif)[0]
	if er==0: return "$"+n+" \\pm "+dn+"$"
	return "$("+n+" \\pm "+dn+") \\times 10^{"+str(er)+"}$"
#vettorizzo la funzione
ne_tex=vectorize(numero_con_errore_latex)


#Funzione che stampa una matrice fatta di stringhe in un formato comodo per latex
#l'argomento "file" deve contenere il percorso al file sul quale stampare la matrice
#ATTENZIONE! il file in cui la funzione stampa la matrice viene completamente sovrascritto
#Author: Francesco Sacco, Lorenzo Cavuoti
def mat_tex(Matrice,file=None):
	Matrice = array(Matrice, dtype=np.unicode, ndmin=2)
	tipo_matrice=len(Matrice)*'c'
	Matrice=transpose(Matrice)
	if file is None:
		print('\n\nCopia tutto quello che c\'è tra le linee')
		print('--------------------------')
		print('\\begin{tabular}{'+tipo_matrice+'}\n\\hline')
		f=stdout
	else: f=open(file,'w')
	for colonna in Matrice:
		stringa='\t'
		for numero in colonna:
			stringa=stringa+numero+' & '
		print(stringa[:-2]+'\\\\',file=f)
	if file==None:
		print('\t\\hline\n\\end{tabular}')
		print('--------------------------\n\n')



   