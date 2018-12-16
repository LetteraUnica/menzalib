from numpy import floor,log10,absolute,round,vectorize,transpose
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

#funzione della notazione scientifica di un singolo numero con un numero di riferimento nrif
"""ad esempio se nrif=500 e n=4896 stampa n con l'ordine di grandezza di nrif, cioè ritorna
	48.96 X 10^2"""
#Author: Francesco Sacco
def notazione_scientifica_latex(n,nrif):
	if n==0: return "$0$"
	if nrif==0: 
		print('non puoi usare come numero di riferimento zero')
		return notazione_scientifica_latex(n,n)
	exp=int(floor(log10(absolute(nrif))))#guardo l'ordine di grandezza di nrif
	if absolute(exp)==1: exp=0 #nel caso l'esponente è uno o meno uno non uso la n.s.
	n=n/10**exp #porto n nell'ordine di grandezza di nrif
	n=round(n,2)#arrotondo alla seconda cifra dopo la virgola
	if exp==0: return "$"+str(n)+"$"
	return "$"+str(n)+"\\times 10^{"+str(exp)+"}$" #ritorna la stringa in latex
#vettorizzo
ns_tex=vectorize(notazione_scientifica_latex)



#funzione della notazione scientifica di un valore x con errore
#stampa una stringa contenente i due valori stampati per bene in latex
#questa funzione potrebbe avere errori se una delle due variabili è uguale a zero
#Author: Francesco Sacco
def numero_con_errore_latex(x,dx):
	if dx==0.0 and x==0.0: return "$0\\pm 0"
	if x==0.0: return "$0\\pm "+notazione_scientifica_latex(dx,dx)[1:]
	if dx==0.0: return notazione_scientifica_latex(x,x)[:-1]+"\\pm 0$"
	exp=int(floor(log10(absolute(x))))#guardo l'ordine di grandezza di x
	if absolute(exp)==1: exp=0 #nel caso l'esponente è uno o meno uno non uso la n.s.
	x=x/10**exp     #porto la virgola dopo la prima cifra
	dx=dx/10**exp   #porto la virgola dove si trova quella della x
	cifr=int(floor(log10(absolute(dx))))  #guardo l'ordine di grandezza di dx
	#taglio le di x con un ordine di grandezza inferiore a dx
	x=round(x,absolute(cifr))       
	dx=round(dx,absolute(cifr)) #taglio le cifre significative di dx dopo la prima
	#ritorno la stringa in latex
	if exp==0:
		return  "$"+str(x)+"\\pm"+stringhizza(dx)+"$" 
	return  "$("+str(x)+"\\pm"+stringhizza(dx)+")\\times 10^{"+str(exp)+"}$"
#vettorizzo la funzione
ne_tex=vectorize(numero_con_errore_latex)



#Funzione che stampa una matrice fatta di stringhe in un formato comodo per latex
#l'argomento "titolo" deve essere una stringa che contiene il titolo in latex della tabella
#l'argomento "file" deve contenere il percorso al file sul quale stampare la matrice
#ATTENZIONE! il file in cui la funzione stampa la matrice viene completamente sovrascritto
#Author: Francesco Sacco
def mat_tex(Matrice,titolo=None,file=None):
	tipo_tabella='{'+(len(Matrice)*'c')+'}'
	Matrice=transpose(Matrice)
	if file==None:
		print('\n\nCopia tutto quello che c\'è tra le linee')
		print('--------------------------')
		f=stdout
	else: f=open(file,'w')
	print('\\begin{tabular}'+tipo_tabella+'\n\\hline',file=f)
	if titolo is None:
		print('\t% qua ci va il titolo della tabella (ricorda di mettere \\\\ alla fine) %\n \\hline',file=f)
	else: print('\t'+titolo+'\\\\ \n\\hline',file=f)
	for colonna in Matrice:
		stringa='\t'
		for numero in colonna:
			stringa=stringa+numero+' & '
		print(stringa[:-2]+'\\\\',file=f)
	print('\\hline\n\\end{tabular}',file=f)
	if file==stdout: print('--------------------------\n\n')
   




   