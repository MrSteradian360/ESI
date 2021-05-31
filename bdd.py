import pandas as pd
import itertools
import numpy as np


def LiczenieEntropii(etykieta, tabela, x):
    n1_plus = tabela.sum(axis=1)[x]  # liczebnosc atrybutu
    lista_n1_plus = [0, 0, 0, 0]

    for i in range(len(tabela.columns)):
        try:
            if tabela.iloc[-4][i] == 1 and tabela.loc[etykieta][i] == 1:
                lista_n1_plus[0] += 1
        except KeyError:
            continue
        try:
            if tabela.iloc[-3][i] == 1 and tabela.loc[etykieta][i] == 1:
                lista_n1_plus[1] += 1
        except KeyError:
            continue
        try:
            if tabela.iloc[-2][i] == 1 and tabela.loc[etykieta][i] == 1:
                lista_n1_plus[2] += 1
        except KeyError:
            continue
        try:
            if tabela.iloc[-1][i] == 1 and tabela.loc[etykieta][i] == 1:
                lista_n1_plus[3] += 1
        except KeyError:
            continue

    logarytmy_plus = [0, 0, 0, 0]

    for i in range(len(lista_n1_plus)):
        if lista_n1_plus[i] != 0 and n1_plus != 0:
            logarytmy_plus[i] = np.log2(lista_n1_plus[i] / n1_plus)
        else:
            logarytmy_plus[i] = 0

    if n1_plus != 0:
        entropia_1plus = -(lista_n1_plus[0] / n1_plus) * logarytmy_plus[0] - (lista_n1_plus[1] / n1_plus) * \
                         logarytmy_plus[
                             1] - (lista_n1_plus[2] / n1_plus) * logarytmy_plus[2] - (lista_n1_plus[3] / n1_plus) * \
                         logarytmy_plus[3]
    else:
        entropia_1plus = 0

    n1_minus = n - n1_plus

    lista_n1_minus = [0, 0, 0, 0]
    logarytmy_minus = [0, 0, 0, 0]

    for i in range(len(tabela.columns)):
        try:
            if tabela.iloc[-4][i] == 1 and tabela.loc[etykieta][i] == 1:
                lista_n1_minus[0] += 1
        except KeyError:
            continue
        try:
            if tabela.iloc[-3][i] == 1 and tabela.loc[etykieta][i] == 1:
                lista_n1_minus[1] += 1
        except KeyError:
            continue
        try:
            if tabela.iloc[-2][i] == 1 and tabela.loc[etykieta][i] == 1:
                lista_n1_minus[2] += 1
        except KeyError:
            continue
        try:
            if tabela.iloc[-1][i] == 1 and tabela.loc[etykieta][i] == 1:
                lista_n1_minus[3] += 1
        except KeyError:
            continue

    for i in range(len(lista_n1_minus)):
        if lista_n1_minus[i] != 0 and n1_minus != 0:
            logarytmy_minus[i] = np.log2(lista_n1_minus[i] / n1_minus)
        else:
            logarytmy_minus[i] = 0

    if n1_minus != 0:
        entropia_1minus = -(lista_n1_minus[0] / n1_minus) * logarytmy_minus[0] - (lista_n1_minus[1] / n1_minus) * \
                          logarytmy_minus[1] - (lista_n1_minus[2] / n1_minus) * logarytmy_minus[2] - (
                                  lista_n1_minus[3] / n1_minus) * logarytmy_minus[3]
    else:
        entropia_1minus = 0

    e1 = (n1_plus / n) * entropia_1plus + (n1_minus / n) * entropia_1minus
    return e1


def drzewo_binarne(tabela, przes, decyzja, level):
    gatunki = list(tabela.index[-4:-1])
    gatunki.append(tabela.index[-1])
    # gatunki = ['Horror', 'Komedia', 'Romans', 'Akcja']
    pozostale = 0
    for k in tabela.index:
        if k in gatunki:
            pozostale += 1
    minimum = 9999
    indeks = 0
    for j in range(-pozostale, 0):
        if len(np.unique(tabela.iloc[j])) == 1:
            if tabela.iloc[j][0] == 1:
                print("   " * level + "|---" + tabela.index[j])
                return 0
    for i in range(len(tabela.index[:len(tabela.index) - len(gatunki)])):  # znajduje atrybut z najmniejszą entropią
        if LiczenieEntropii(tabela.index[i], tabela, i) < minimum:
            minimum = LiczenieEntropii(tabela.index[i], tabela, i)
            indeks = i
    kryteria = (tabela.iloc[indeks] == decyzja)
    tabela2 = tabela[kryteria.index[kryteria]]

    if decyzja == 1:
        print("   " * level + "|---" + tabela2.index[indeks] + " TAK")
    else:
        print("   " * level + "|---" + tabela2.index[indeks] + " NIE")
    level += 1
    for kategoria in przes:
        if tabela2.index[indeks] in kategoria:
            for atrybut in kategoria:
                if atrybut != tabela2.index[indeks]:
                    try:
                        if len(np.unique(tabela2.loc[atrybut])) == 1:
                            tabela2 = tabela2.drop(index=atrybut)
                    except KeyError:
                        continue

    tabela2 = tabela2.drop(tabela2.index[indeks])  # usuwam rząd z najniższą entropią
    tabela2.columns = np.arange(len(tabela2.columns))

    x = drzewo_binarne(tabela2, przes, 1, level)
    if x != 0:
        drzewo_binarne(tabela2, przes, 0, level)


wiek = ["5-12", "13-25", "26-49", "50+"]
plec = ["M", "K"]
z_kim = ["Sam", "Z rodziną", "Ze znajomymi"]
pora_dnia = ["Rano", "Popołudnie", "Wieczór"]
gdzie = ["Telewizor", "Telefon", "Kino"]
przeslanki = [wiek, plec, z_kim, pora_dnia, gdzie]

"""
MOŻNA GENEROWAĆ TABELE I PRZESŁANKI W PROGRAMIE JEŚLI JEST TAKA POTRZEBA
il_kartezjanski = itertools.product(wiek, plec, z_kim, pora_dnia, gdzie)
lista_kartezjanska = list(il_kartezjanski)
# print(lista_kartezjanska)

wiek_kolumna = []
plec_kolumna = []
z_kim_kolumna = []
pora_dnia_kolumna = []
gdzie_kolumna = []

for z in lista_kartezjanska:
    wiek_osoby = []
    for w in wiek:
        if z[0] == w:
            wiek_osoby.append(1)
        else:
            wiek_osoby.append(0)
    wiek_kolumna.append(wiek_osoby)

for z in lista_kartezjanska:
    plec_osoby = []
    for w in plec:
        if z[1] == w:
            plec_osoby.append(1)
        else:
            plec_osoby.append(0)
    plec_kolumna.append(plec_osoby)

for z in lista_kartezjanska:
    z_kim_osoby = []
    for w in z_kim:
        if z[2] == w:
            z_kim_osoby.append(1)
        else:
            z_kim_osoby.append(0)
    z_kim_kolumna.append(z_kim_osoby)

for z in lista_kartezjanska:
    pora_dnia_osoby = []
    for w in pora_dnia:
        if z[3] == w:
            pora_dnia_osoby.append(1)
        else:
            pora_dnia_osoby.append(0)
    pora_dnia_kolumna.append(pora_dnia_osoby)

for z in lista_kartezjanska:
    gdzie_osoby = []
    for w in gdzie:
        if z[4] == w:
            gdzie_osoby.append(1)
        else:
            gdzie_osoby.append(0)
    gdzie_kolumna.append(gdzie_osoby)

tabela0 = pd.DataFrame(wiek_kolumna).T
tabela0 = tabela0.rename(index={0: "5-12", 1: "13-25", 2: "26-49", 3: "50+"})

tabela_plec = pd.DataFrame(plec_kolumna).T
tabela_plec = tabela_plec.rename(index={0: "M", 1: "K"})
tabela0 = tabela0.append(tabela_plec)

tabela_z_kim = pd.DataFrame(z_kim_kolumna).T
tabela_z_kim = tabela_z_kim.rename(index={0: "Sam", 1: "Z rodziną", 2: "Ze znajomymi"})
tabela0 = tabela0.append(tabela_z_kim)

tabela_pora_dnia = pd.DataFrame(pora_dnia_kolumna).T
tabela_pora_dnia = tabela_pora_dnia.rename(index={0: "Rano", 1: "Popołudnie", 2: "Wieczór"})
tabela0 = tabela0.append(tabela_pora_dnia)

tabela_gdzie = pd.DataFrame(gdzie_kolumna).T
tabela_gdzie = tabela_gdzie.rename(index={0: "Telewizor", 1: "Telefon", 2: "Kino"})
tabela0 = tabela0.append(tabela_gdzie)

horror_film = []
komedia_film = []
romans_film = []
akcja_film = []
for z in range(217):
    if z in range(1, 30):
        komedia_film.append(1)
        horror_film.append(0)
        romans_film.append(0)
        akcja_film.append(0)
    elif z in range(30, 90):
        komedia_film.append(0)
        horror_film.append(1)
        romans_film.append(0)
        akcja_film.append(0)
    elif z in range(90, 150):
        komedia_film.append(0)
        horror_film.append(0)
        romans_film.append(0)
        akcja_film.append(1)
    elif z in range(150, 217):
        komedia_film.append(0)
        horror_film.append(0)
        romans_film.append(1)
        akcja_film.append(0)

konkluzja_horror = pd.DataFrame(horror_film).T.rename(index={0: "Horror"})
konkluzja_komedia = pd.DataFrame(komedia_film).T.rename(index={0: "Komedia"})
konkluzja_akcja = pd.DataFrame(akcja_film).T.rename(index={0: "Akcja"})
konkluzja_romans = pd.DataFrame(romans_film).T.rename(index={0: "Romans"})
print(konkluzja_horror)

tabela0 = tabela0.append(konkluzja_horror)
tabela0 = tabela0.append(konkluzja_komedia)
tabela0 = tabela0.append(konkluzja_akcja)
tabela0 = tabela0.append(konkluzja_romans)

"""
tabela0 = pd.read_excel("konkluzje.xlsx", index_col=0)
n1 = tabela0.sum(axis=1)[-4]
n2 = tabela0.sum(axis=1)[-3]
n3 = tabela0.sum(axis=1)[-2]
n4 = tabela0.sum(axis=1)[-1]
# tabela0.to_excel("konkluzje.xlsx")
n = tabela0.shape[1]
entropia = (-n1 / n) * np.log2(n1 / n) - (n2 / n) * np.log2(n2 / n) - (n3 / n) * np.log2(n3 / n) - (n4 / n) * np.log2(
    n4 / n)
poziom = 0
drzewo_binarne(tabela0, przeslanki, 1, poziom)
drzewo_binarne(tabela0, przeslanki, 0, poziom)
input()
