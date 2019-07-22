# File di testing per le funzioni di texpy

import latex as mz
import numpy as np

def test_notazione_scientifica():
    print(mz.ns_tex(123), "$1.23 \\times 10^{2}$")
    print(mz.ns_tex(12.3), "$1.23 \\times 10^{1}$")
    print(mz.ns_tex(382387e-13), "$3.82 \\times 10^{-8}$")
    print(mz.ns_tex(382387e-13, 1e-13), "$382387 \\times 10^{-13}$")
    print(mz.ns_tex(382387e-13, 1e4), "$0.000000000004 \\times 10^{4}$")
    print(mz.ns_tex(123, 1, 1), "$123$")
    print(mz.ns_tex(123, 10, 1), "$12.3 \\times 10^{1}$")
    print(mz.ns_tex(382387e-13, nult=1e-9), "$3.8 \\times 10^{-8}$")
    print(mz.ns_tex(382387e14, nult=1e24), "$4 \\times 10^{19}$")
    print(mz.ns_tex(382387e14, nult=1e4), "$3.823870000000000 \\times 10^{19}$")
    print(mz.ns_tex(382387e14, 1e20), "$0.4 \\times 10^{20}$")
    print("TEST FUNZIONE NOTAZIONE SCIENTIFICA PASSATI")

def test_numero_errore():
    print(mz.ne_tex(1, 0.2), "$(1.0 \\pm 0.2)$")
    print(mz.ne_tex(1, 20), "$<2 \\times 10^{1}$")
    print(mz.ne_tex(1.987987, 0.2), "$2.0 \\pm 0.2$")
    print(mz.ne_tex(123, 2, unit="F"), "$(123 \\pm 2)$F")
    print(mz.ne_tex(123e-1, 2, "F"), "$(12 \\pm 2)$F")
    print(mz.ne_tex(123e-2, 2, "F"), "$<2$F")
    print(mz.ne_tex(123e-2, 2e-5, "F"), "$(1.23000 \\pm 0.00002)$F")
    print(mz.ne_tex(123e-3, 2e-5, "F"), "$(123.00 \\pm 0.02)$mF")
    #print(mz.ne_tex(0, 0, unit="F"), "$(0 \\pm 0)$F")
    print("\tTEST FUNZIONE NUMERO ERRORE PASSATI")

def test_nes():
    args = [12e-9, 65, 98e9, 64543]
    output = ["$1.20 \\times 10^{-8}$", "$6.50 \\times 10^{1}$", "$9.80 \\times 10^{10}$", "$6.45 \\times 10^{4}$"]
    for i in range(len(args)):
        print(mz.nes_tex(args[i]), output[i])
    
    args = [[12.675765e-9, 1e-6], [65.82736, 10], [98.827368e9, 1e1]]
    output = [[0, '$1 \\times 10^{-6}$'],
        ["$7 \\times 10^{1}$", "$1 \\times 10^{1}$"], 
        ["$9.882736800 \\times 10^{10}$", "$0.000000001 \\times 10^{10}$"]]
    for i in range(len(args)):
        temp = mz.nes_tex(*args[i])
        for j in range(len(temp)):
            print(temp[j], output[i][j])
    
    args = [[12.675765e-9, 1e-6, "F"], [65.82736, None, "F"], [98.827368e9, 1e1, "F"]]
    output = [(np.array([0]), np.array(["$1$\\mu F"])),
        np.array(["$65.8$F"]),
        (np.array(['$98.82736800$GF']), np.array(['$0.00000001$GF']))]
    for i in range(len(args)):
        print(mz.nes_tex(*args[i]), output[i])
    print("\tTEST FUNZIONE NES PASSATI")

# Per la funzione matrice latex non ho scritto un codice di testing
# perchè restituisce un output molto lungo


test_notazione_scientifica()
test_numero_errore()
test_nes()