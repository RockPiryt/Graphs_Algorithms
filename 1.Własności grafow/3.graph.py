'''Zadanie 5 (0.1 pkt)

Napisz program, który dla danego ciągu liczb 
S, utworzy graf, którego wierzchołkami będą liczby ze zbioru S, natomiast krawędziami zbiór par 
(u,v) takich że ∣u−v∣∈S. Wyświetl macierz sąsiedztwa tego grafu.

Uwaga. Ciągi ze zbioru S mogą być nie posortowane. 
Nie zmieniajmy kolejności występowania wierzchołków. 
Czyli traktujemy jako pierwszy wierzchołek, ten który występuje pierwszy w ciągu liczb S.

Sample Input:

2 3 4 7 11 13
Sample Output:

0 0 1 0 0 1
0 0 0 1 0 0
1 0 0 1 1 0
0 1 1 0 1 0
0 0 1 1 0 1
1 0 0 0 1 0'''

# put your python code here
def is_in_set(value, S):
    """Sprawdza, czy dana wartość znajduje się w zbiorze S."""
    return value in S

def create_adjacency_matrix(S):
    """Tworzy macierz sąsiedztwa na podstawie zbioru S."""
    #n=2 3 4 7 11 13 - lista inputów od usera
    n = len(S)
    
    # Inicjalizuj pustą macierz sąsiedztwa zerami 
    adj_matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(0)  # Dodaj 0 do wiersza
        adj_matrix.append(row)  # Dodaj wiersz do macierzy

    # Wypełnij macierz sąsiedztwa
    for i in range(n):
        for j in range(n):
            # Unikaj pętli własnych
            if i != j:
                # Oblicz wartość bezwzględną różnicy
                diff = abs(S[i] - S[j])
                
                # Jeśli różnica znajduje się w zbiorze S, oznacz jako krawędź
                if is_in_set(diff, S):
                    adj_matrix[i][j] = 1

    return adj_matrix

def display_adjacency_matrix(adj_matrix):
    """Wyświetla macierz sąsiedztwa."""
    n = len(adj_matrix)
    # Wyświetl macierz wiersz po wierszu
    for i in range(n):
        for j in range(n):
            if j == n - 1:
                # Jeśli to ostatni element w wierszu, nie dodawaj spacji
                print(adj_matrix[i][j], end="")
            else:
                # Dodaj spację po każdym elemencie oprócz ostatniego
                print(adj_matrix[i][j], end=" ")
        # Przejdź do nowego wiersza po zakończeniu wiersza
        print()

# Wejście: lista liczb S
#S = input("Podaj elementy zbioru S (oddzielone spacją): ")  
S = input()  
S = S.split() 
S = list(map(int, S))  # mapowanie każdego elementu ze stringa na int

# S = [int(x) for x in input("Podaj elementy zbioru S (oddzielone spacją): ").split()]


# Utwórz macierz sąsiedztwa
adj_matrix = create_adjacency_matrix(S)

# Wyświetl macierz sąsiedztwa
#print("Macierz sąsiedztwa:")
display_adjacency_matrix(adj_matrix)




