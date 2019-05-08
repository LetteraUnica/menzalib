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


def principale(n,nrif=None,nult=None):
    if n==0.0: return ["0",0]
    if nrif==None:nrif=n
    if nult==None:
        if nrif==n: nult=n/100 #ns_tex(456,456)=4.56 x 10^2
        if nrif>n: nult=n    #ns_tex(6,572)=0.06 x 10^2
        if nrif<n: nult=nrif #ns_tex(572,6)=572
    if nrif==0.0 or nult==0.0: 
        print('non puoi usare come numero di riferimento o numero dell\'ultima cifra lo zero')
        return principale(n)
    er=int(floor(log10(absolute(nrif))))#guardo l'ordine di grandezza di nrif
    #if absolute(er)==1: er=0 #nel caso l'esponente è uno o meno uno non uso la n.s.
    n,nult=n/10**er,nult/10**er #porto n nell'ordine di grandezza di nrif
    eu=int(floor(log10(absolute(nult))))#guardo l'ordine di grandezza di nult
    if eu>0:
        print('non puoi usare un numero per l\'ultima cifra maggiore di quello di riferimento')
        return principale(n)
    n=round(n,-eu)#arrotondo alla seconda cifra dopo la virgola
    return [str(n),er] #se 3.645*10^-23 si ha che str(n)="3.645" e er=-23


#funzione della notazione scientifica di un singolo numero con un numero di riferimento nrif
"""ad esempio se nrif=500 e n=4896 stampa n con l'ordine di grandezza di nrif, cioè ritorna
	48.96 X 10^2"""
#Author: Francesco Sacco
def notazione_scientifica_latex(n,nrif=None,nult=None):
    n,exp=principale(n,nrif,nult)
    if exp==0: return "$"+n+"$"
    return "$"+n+"\\times 10^{"+str(exp)+"}$"
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
    n,er=principale(x,nult=dx)
    dn=principale(dx,x)[0]
    if er==0: return "$"+n+"\\pm"+dn+"$"
    return "$("+n+"\\pm"+dn+")\\times 10^{"+str(er)+"}$"
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
    if file==None: print('--------------------------\n\n')


   