from numpy import floor,log10,absolute,round,vectorize,transpose
from sys import stdout

#funzione della notazione scientifica di un singolo numero con un numero di riferimento nrif
"""ad esempio se nrif=500 e n=4896 stampa n con l'ordine di grandezza di nrif, cioè ritorna
	48.96 X 10^2"""
#Author: Francesco Sacco
def notazione_scientifica_latex(n,nrif):
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
	if dx==0 and x==0: return "$0\\pm 0"
	if x==0: return "$0\\pm "+notazione_scientifica_latex(dx,dx)[1:]
	if dx==0: return notazione_scientifica_latex(x,x)[:-1]+"\\pm 0"
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
		return  "$"+str(x)+"\\pm"+str(dx)+"$" 
	return  "$("+str(x)+"\\pm"+str(dx)+")\\times 10^{"+str(exp)+"}$"
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
   




   