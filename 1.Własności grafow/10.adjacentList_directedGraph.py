"""Zadanie 6 (0.1 pkt)

Napisz program, który wczytuje graf skierowany podany jako lista sąsiedztwa i 
wypisuje stopnie wychodzące oraz wchodzące każdego wierzchołka.

Sample Input:

1 2
2 1
Sample Output:

Stopnie wejściowe: 1 1
Stopnie wyjściowe: 1 1"""

def read_graph():
    graph = []
    
    # Wczytuj dane aż do końca wejścia (EOF)
    try:
        while True:
            line = input().strip()
            if line:
                split_line = line.split() 
                u = int(split_line[0])  # Pierwszy element to numer wierzchołka
                while len(graph) <= u:
                    graph.append([])  # Dodajemy brakujące wierzchołki
                neighbors = []
                for x in split_line[1:]:
                    neighbors.append(int(x))
                graph[u] = neighbors  # Przypisujemy listę sąsiadów
            else:
                graph.append([])  
    except EOFError:
        pass
    
    return graph

def calculate_degrees(graph):
    n = len(graph) - 1  # Liczba wierzchołków (ignorujemy indeks 0)
    in_degree = [0] * (n + 1)
    out_degree = [0] * (n + 1)
    
    for u in range(1, n + 1):
        out_degree[u] = len(graph[u])  # Stopień wychodzący = liczba sąsiadów
        for v in graph[u]:
            in_degree[v] += 1  # Dodajemy do stopnia wchodzącego wierzchołka v

    print("Stopnie wejściowe:", " ".join(map(str, in_degree[1:])))
    print("Stopnie wyjściowe:", " ".join(map(str, out_degree[1:])))

graph = read_graph()
calculate_degrees(graph)