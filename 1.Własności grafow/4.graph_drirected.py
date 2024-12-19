'''Zadanie 6 (0.1 pkt)

Napisz program, który utworzy graf skierowany dla ciągów liczb 
S i A o następującej definicji:

Zbiorem wierzchołków grafu będą liczby, które należą do ciągu A
Istnieje łuk 
(x,y), jeśli x≠y oraz  y−x∈S.
Graf przedstaw w postaci macierzy sąsiedztwa.

Pierwszy wiersz na wejściu jest to ciąg A, natomiast drugi wiersz reprezentuje ciąg S.

Uwaga. Ciągi ze zbioru A mogą być nie posortowane. 
Nie zmieniajmy kolejności występowania wierzchołków. 
Czyli traktujemy jako pierwszy wierzchołek, ten który występuje pierwszy w ciągu liczb A

Sample Input:

0 1 2 3 4
-2 1 2 4
Sample Output:

0 1 1 0 1
0 0 1 1 0
1 0 0 1 1
0 1 0 0 1
0 0 1 0 0'''

def is_in_set(value, S):
    """Sprawdza, czy dana wartość znajduje się w zbiorze S."""
    return value in S

def create_adjacency_matrix(A, S):
    """Tworzy macierz sąsiedztwa dla grafu skierowanego na podstawie zbiorów A i S."""
    # A=[0 1 2 3 4]
    # S=[-2 1 2 4]
    n = len(A)
    
    # Inicjalizuj pustą macierz sąsiedztwa zerami
    adj_matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(0)  
        adj_matrix.append(row)  

    # Wypełnij macierz sąsiedztwa
    for i in range(n):
        for j in range(n):
            # Unikaj pętli własnych
            if i != j:
                # Oblicz różnicę y - x
                diff = A[j] - A[i]
                
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

# Wejście: lista liczb A (pierwszy wiersz) oraz lista liczb S (drugi wiersz)
print("Podaj elementy zbioru A (oddzielone spacją): ")
A = [int(x) for x in input().split()]
print("Podaj elementy zbioru S (oddzielone spacją): ")
S = [int(x) for x in input().split()]

# Utwórz macierz sąsiedztwa
adj_matrix = create_adjacency_matrix(A, S)

# Wyświetl macierz sąsiedztwa
#print("Macierz sąsiedztwa:")
display_adjacency_matrix(adj_matrix)
