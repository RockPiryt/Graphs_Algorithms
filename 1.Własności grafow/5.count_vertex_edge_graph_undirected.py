'''Zadanie 7 (0.2 pkt)

Napisz program, który od użytkownika wczyta macierz sąsiedztwa reprezentująca graf, a następnie wypisze ilość wierzchołków oraz krawędzi/łuków w grafie.

Jeżeli istnieje krawędź o wadze większej niż jeden, to zakładamy że jest to jedna krawędź.

Poniżej znajduje się przykładowe wyjście programu:

Ilość wierzchołków: 8
Ilość krawędzi: 15
Sample Input:

0 0 1 1 1 0 0 0
0 0 1 0 1 1 0 1
1 1 0 1 0 1 1 1
1 0 1 0 1 0 1 1
1 1 0 1 0 1 0 0
0 1 1 0 1 0 0 0
0 0 1 1 0 0 0 0
0 1 1 1 0 0 0 0
Sample Output:

Ilość wierzchołków: 8
Ilość krawędzi: 15'''

def count_vertices_and_edges(adj_matrix):
    """Liczy liczbę wierzchołków oraz krawędzi w grafie."""
    # Ilość wierzchołków to po prostu długość macierzy
    num_vertices = len(adj_matrix)
    
    num_edges = 0
    # Iteruj przez górną część macierzy sąsiedztwa
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):  # Sprawdzamy tylko górną część macierzy
            if adj_matrix[i][j] > 0:  # Krawędź istnieje
                num_edges += 1  # Zliczamy krawędź jako 1
    
    return num_vertices, num_edges

def read_adjacency_matrix():
    """Wczytuje macierz sąsiedztwa od użytkownika."""
    adj_matrix = []
    #print("Podaj macierz sąsiedztwa, każda linia to wiersz macierzy (oddzielone spacją):")
    
    # Wczytaj dane wejściowe aż do końca
    while True:
        try:
            line = input()
            if not line:  # Jeśli pusta linia, zakończ wczytywanie
                break
            # Dodaj wiersz do macierzy, przekształcając go na listę liczb całkowitych
            adj_matrix.append([int(x) for x in line.split()])
        except EOFError:
            break  # Zakończ wczytywanie, gdy nie ma więcej danych
    
    return adj_matrix

# Wczytaj macierz sąsiedztwa
adj_matrix = read_adjacency_matrix()

# Policz liczbę wierzchołków i krawędzi
num_vertices, num_edges = count_vertices_and_edges(adj_matrix)

# Wyświetl wyniki
print(f"Ilość wierzchołków: {num_vertices}")
print(f"Ilość krawędzi: {num_edges}")

'''
Zliczanie krawędzi w górnej części macierzy:

Użycie pętli for j in range(i + 1, num_vertices) zapewnia, że nie będziemy zliczać krawędzi w obie strony,
 co jest istotne dla grafu nieskierowanego.
Zliczamy tylko te krawędzie, które istnieją, czyli te, które mają wartość większą niż 0.
Krawędzie o wadze większej niż jeden:

Nie musimy już dzielić przez 2, ponieważ każda krawędź, niezależnie od jej wagi, jest liczona tylko raz.'''

''''''