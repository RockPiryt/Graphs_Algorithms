def wczytaj():
    wejscie =[]
    try:
        while True:
            wiersz = input()
            if wiersz.strip() != "":
                lista = list(map(int, wiersz.split()))
                wejscie.append(lista)
       
    except EOFError:
        pass
    return wejscie
   
def bledy_wejscia(wejscie):
    znacznik = True
    elementy = len(wejscie)
    if len(wejscie[0]) != 3:
        znacznik = False
    if wejscie[0][0] < 2 or wejscie[0][0] > 30:
        znacznik = False
    if wejscie[0][1] < 1 or wejscie[0][1] > 5:
        znacznik = False
    if wejscie[0][2] < 1 or wejscie[0][2] > 3:
        znacznik = False
    if wejscie[0][0] != len(wejscie) - 3:
        znacznik = False
    if wejscie[0][1] != len(wejscie[elementy-2]):
        znacznik = False
    if wejscie[0][2] != len(wejscie[elementy-1]):
        znacznik = False
    for i in range(1, len(wejscie) - 2):
        for j in range(len(wejscie[i])):
            if wejscie[i][j] > 1 or wejscie[i][j] < 0:
                znacznik = False
                break
    for i in range(len(wejscie[elementy-2])):
        if wejscie[elementy-2][i] > wejscie[0][0]:
            znacznik = False
            break
    for i in range(len(wejscie[elementy-1])):
        if wejscie[elementy-1][i] > wejscie[0][0]:
            znacznik = False
            break       
    return znacznik

def zrob_liste_sasiedztwa(wejscie):
    lista = []
    for i in range(len(wejscie)):
        wiersz =[]
        wiersz.append(i+1)
        for j in range(0, len(wejscie[i])):
            if wejscie[i][j] >= 1:
                wiersz.append(j+1)
        lista.append(wiersz)
    return lista


def podzial(tablica, poczatek, koniec):
    srodek = (poczatek + koniec) // 2
    tablica[srodek], tablica[koniec] = tablica[koniec], tablica[srodek]
    pivot = tablica[koniec]
    i = poczatek - 1
    for j in range(poczatek, koniec):
        if tablica[j] <= pivot:
            i += 1
            tablica[i], tablica[j] = tablica[j], tablica[i]
    tablica[i + 1], tablica[koniec] = tablica[koniec], tablica[i + 1]
    return i + 1  # index q

def quicksort(tablica, poczatek, koniec):
    if poczatek < koniec:
        q = podzial(tablica, poczatek, koniec)
        quicksort(tablica, poczatek, q - 1)
        quicksort(tablica, q + 1, koniec)

def sortowanie(tablica):
    quicksort(tablica, 0, len(tablica) - 1)
    return tablica
   
def czy_odwiedzony(wierzcholek, odwiedzone):
    if wierzcholek in odwiedzone:
        return True
    else:
        return False
         
def czy_pusty_stos(stos):
    if len(stos) != 0:
        return False
    else:
        return True

def dfs(lista_sasiedztwa, wierzcholek, wyjscia, opcja):
    stos = []
    odwiedzone = []
    znacznik = True
    sasiad = wierzcholek
    czy_sciezka_ew = False
    while znacznik:               
        if sasiad != None:
            wierzcholek = sasiad
            stos.append(wierzcholek)
            if czy_odwiedzony(wierzcholek, odwiedzone) == False:
                odwiedzone.append(wierzcholek)
            if opcja == "S":
                if wierzcholek in wyjscia:
                    znacznik = False
                    czy_sciezka_ew = True
                    break
            sasiad = None
            for i in range(1, len(lista_sasiedztwa[wierzcholek-1])):           
                if czy_odwiedzony(lista_sasiedztwa[wierzcholek-1][i], odwiedzone) == False:
                        sasiad = lista_sasiedztwa[wierzcholek-1][i]
                        break
        else:
            if czy_pusty_stos(stos) == False:
                stos.pop(len(stos) -1)
                if czy_pusty_stos(stos) == False:
                    wierzcholek = stos[len(stos) -1]
                    for i in range(1, len(lista_sasiedztwa[wierzcholek-1])):
                        if czy_odwiedzony(lista_sasiedztwa[wierzcholek-1][i], odwiedzone) == False:
                            sasiad = lista_sasiedztwa[wierzcholek-1][i]
                            break
                else:
                    znacznik = False
            else:
                znacznik = False
               
    if opcja == "S":
        if czy_sciezka_ew == False:
            odwiedzone = []
    return odwiedzone
   
                         
def main():
    wejscie = wczytaj()
    if bledy_wejscia(wejscie) == True:
        liczba_pomieszczen = wejscie[0][0]
        liczba_wyjsc = wejscie[0][1]
        liczba_zagrozen = wejscie[0][2]
        przejscia = zrob_liste_sasiedztwa(wejscie[1:len(wejscie)-2])              
        wyjscia = wejscie[len(wejscie)-2]
        zagrozenia = wejscie[len(wejscie)-1]
        sciezki_ewakuacyjne = []
       
        wyjscia = sortowanie(wyjscia)
        zagrozenia = sortowanie(zagrozenia)
       
        for i in range(len(zagrozenia)):
            sciezka = dfs(przejscia, zagrozenia[i], wyjscia, "S")
            if len(sciezka) > 0:
                sciezki_ewakuacyjne.append(sciezka)
           
        przejscie = dfs(przejscia, zagrozenia[0], wyjscia, "P")
                               
        if len(zagrozenia) == len(sciezki_ewakuacyjne):
            print("BEZPIECZNY")
            for i in range(len(sciezki_ewakuacyjne)):
                print(' '.join(map(str, sciezki_ewakuacyjne[i])))
            print(' '.join(map(str, przejscie)))
        else:
            print("NIEBEZPIECZNY")
            for i in range(len(sciezki_ewakuacyjne)):
                print(' '.join(map(str, sciezki_ewakuacyjne[i])))
            lista_pomocnicza = []
            for i in range(len(sciezki_ewakuacyjne)):
                lista_pomocnicza.append(sciezki_ewakuacyjne[i][0])
            for i in range(len(zagrozenia)):
                if zagrozenia[i] not in lista_pomocnicza:
                    print("BRAK DROGI Z POMIESZCZENIA", zagrozenia[i])    

    else:
        print("BŁĄD")
   
   
if __name__ == "__main__":
    main()