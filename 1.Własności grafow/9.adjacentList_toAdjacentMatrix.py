'''Zadanie 5 (0.1 pkt)

Napisz program, który wczytuje graf podany jako lista sąsiedztwa i wyświetla macierz sąsiedztwa danego grafu.

Sample Input 1:

1 2
2 1
Sample Output 1:

0 1
1 0
Sample Input 2:

1 2 4 5 6 9
2 1 3 4 8 10
3 2 5 6 8 10
4 1 2 5 7 8
5 1 3 4 6 9
6 1 3 5 7 9
7 4 6 8 9 10
8 2 3 4 7 10
9 1 5 6 7 10
10 2 3 7 8 9
Sample Output 2:

0 1 0 1 1 1 0 0 1 0
1 0 1 1 0 0 0 1 0 1
0 1 0 0 1 1 0 1 0 1
1 1 0 0 1 0 1 1 0 0
1 0 1 1 0 1 0 0 1 0
1 0 1 0 1 0 1 0 1 0
0 0 0 1 0 1 0 1 1 1
0 1 1 1 0 0 1 0 0 1
1 0 0 0 1 1 1 0 0 1
0 1 1 0 0 0 1 1 1 0'''

def read_graph():
    graph = []
    
    # Wczytuj dane aż do końca wejścia (EOF)
    try:
        while True:
            line = input().strip()
            if line:
                split_line = line.split()
                neighbors = []
                for x in split_line[1:]:  # Pomijamy pierwszy element (numer wierzchołka)
                    neighbors.append(int(x))
                graph.append(neighbors)
            else:
                graph.append([])  # Dodajemy pustą listę, jeśli nie ma sąsiadów
    except EOFError:
        pass
    
    return graph

def adjacency_matrix(graph):
    # Zidentyfikowanie liczby wierzchołków
    num_vertices = len(graph)
    
    # Tworzenie pustej macierzy 
    matrix = []
    for i in range(num_vertices):
        row = []
        for j in range(num_vertices):
            row.append(0)  
        matrix.append(row) 

    # Wypełnienie macierzy na podstawie listy sąsiedztwa
    for i in range(num_vertices):
        for neighbor in graph[i]:
            matrix[i][neighbor - 1] = 1  # Indeksy zmniejszone o 1 (wierzchołki zaczynają się od 1)
    return matrix

def display_adjacency_matrix(adj_matrix):
    """Wyświetla macierz sąsiedztwa."""
    n = len(adj_matrix)
    # Wyświetl macierz wiersz po wierszu
    for i in range(n):
        for j in range(n):
            if j == n - 1:
                print(adj_matrix[i][j], end="")
            else:
                print(adj_matrix[i][j], end=" ")
        print()

# Wczytaj graf w formie listy sąsiedztwa
graph = read_graph()
# Tworzenie macierzy sąsiedztwa
matrix = adjacency_matrix(graph)
# Wyświetlenie macierzy
display_adjacency_matrix(matrix)

