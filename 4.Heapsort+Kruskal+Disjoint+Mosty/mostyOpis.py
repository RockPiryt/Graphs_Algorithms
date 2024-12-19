import sys


# # Implementacja algorytmu Kruskala
# def kruskal(edges, n):
#     # Sortowanie krawędzi za pomocą HeapSort
#     heap_sort(edges)

#     parent = [i for i in range(n + 1)]

#     minSpinalTree = []

#     for edge in edges:
#         if find(parent, edge['a']) != find(parent, edge['b']):
#             minSpinalTree.append(edge)
#             union(parent, edge['a'], edge['b'])
#         if len(minSpinalTree) == n - 1:
#             break

#     return minSpinalTree

# # Implementacja HeapSort
# def heap_sort(array):
#     n = len(array)

#     # Budowanie kopca (max-heap)
#     for i in range(n // 2 - 1, -1, -1):
#         heapify(array, n, i)

#     # Wyciąganie elementów z kopca
#     for i in range(n - 1, -1, -1):
#         array[0], array[i] = array[i], array[0]
#         heapify(array, i, 0)

#     # Odwrócenie tablicy, aby uzyskać sortowanie rosnące
#     array.reverse()

# # Funkcja heapify
# def heapify(array, n, i):
#     largest = i
#     l = 2 * i + 1
#     r = 2 * i + 2

#     if l < n and compare_edges(array[l], array[largest]) > 0:
#         largest = l

#     if r < n and compare_edges(array[r], array[largest]) > 0:
#         largest = r

#     if largest != i:
#         array[i], array[largest] = array[largest], array[i]
#         heapify(array, n, largest)

# # Funkcja porównująca krawędzie zgodnie z podanymi kryteriami
# def compare_edges(edge1, edge2):
#     if edge1['w'] != edge2['w']:
#         return edge2['w'] - edge1['w'] # Dla max-heap
#     if edge1['a'] != edge2['a']:
#         return edge2['a'] - edge1['a']
#     if edge1['b'] != edge2['b']:
#         return edge2['b'] - edge1['b']
#     return 0

# # Implementacja Union-Find z kompresją ścieżki
# def find(parent, i):
#     if parent[i] != i:
#         parent[i] = find(parent, parent[i])
#     return parent[i]

# def union(parent, x, y):
#     xroot = find(parent, x)
#     yroot = find(parent, y)
#     parent[yroot] = xroot

# # Budowanie grafu jako listy sąsiedztwa
# def build_graph(edges, n):
#     graph = {i: [] for i in range(1, n + 1)}
#     for edge in edges:
#         graph[edge['a']].append({'to': edge['b']})
#         graph[edge['b']].append({'to': edge['a']})
#     return graph

# # Znajdowanie mostów za pomocą algorytmu Tarjana
# time = 0 # Deklaracja zmiennej globalnej

# def find_bridges(graph, n):
#     global time
#     time = 0
#     visited = [False] * (n + 1)
#     disc = [0] * (n + 1)
#     low = [0] * (n + 1)
#     parent = [-1] * (n + 1)
#     bridges = []

#     for i in range(1, n + 1):
#         if not visited[i]:
#             bridge_util(i, visited, disc, low, parent, graph, bridges)

#     # Sortowanie mostów zgodnie z wymaganiami
#     bridges.sort(key=lambda x: (x['u'], x['v']))

#     return bridges

# def bridge_util(u, visited, disc, low, parent, graph, bridges):
#     global time
#     visited[u] = True
#     time += 1
#     disc[u] = low[u] = time

#     # Sortowanie sąsiadów, aby zawsze wybierać najmniejszy numer
#     neighbors = sorted(edge['to'] for edge in graph[u])

#     for v in neighbors:
#         if not visited[v]:
#             parent[v] = u
#             bridge_util(v, visited, disc, low, parent, graph, bridges)
#             low[u] = min(low[u], low[v])

#             if low[v] > disc[u]:
#                 bridges.append({'u': min(u, v), 'v': max(u, v)})
#         elif v != parent[u]:
#             low[u] = min(low[u], disc[v])

# # Usuwanie krawędzi z grafu
# def remove_edge(graph, u, v):
#     graph[u] = [edge for edge in graph[u] if edge['to'] != v]
#     graph[v] = [edge for edge in graph[v] if edge['to'] != u]

# # Znajdowanie komponentów spójności
# def find_components(graph, n):
#     visited = [False] * (n + 1)
#     components = []

#     for i in range(1, n + 1):
#         if not visited[i]:
#             component = []
#             dfs_components(graph, i, visited, component)
#             component.sort()
#             components.append(component)

#     # Sortowanie komponentów
#     components.sort(key=lambda x: x[0])

#     return components

# def dfs_components(graph, u, visited, component):
#     visited[u] = True
#     component.append(u)

#     neighbors = sorted(edge['to'] for edge in graph[u])

#     for v in neighbors:
#         if not visited[v]:
#             dfs_components(graph, v, visited, component)

if __name__ == '__main__':
    # try:
        input_lines = sys.stdin.read().strip().split('\n')

        # Sprawdzenie minimalnej liczby linii
        if len(input_lines) < 2:
            raise ValueError('BŁĄD')

        # Parsowanie pierwszej linii z n i m
        n_m = list(map(int, input_lines[0].split()))
        if len(n_m) != 2:
            raise ValueError('BŁĄD')
        n, m = n_m
        if n < 2 or n > 100 or m < n - 1 or m > (n * (n - 1)) // 2:
            raise ValueError('BŁĄD')
        
        print(f"Liczba  nodów: {n}")
        print(f"Liczba  możliwych połączeń: {m}")

        # Odczytanie krawędzi
        edges = []
        for i in range(1, m + 1):
            a_b_w = list(map(int, input_lines[i].split()))
            if len(a_b_w) != 3:
                raise ValueError('BŁĄD')
            a, b, w = a_b_w
            if (
                a < 1 or a > n or b < 1 or b > n or
                w < 1 or w > 1000000
            ):
                raise ValueError('BŁĄD')
            # Upewnienie się, że a ≤ b
            if a > b:
                a, b = b, a
            edges.append({'a': a, 'b': b, 'w': w})

        print(f"o to krawędzie z wagami {edges}")

#         # Wykonanie algorytmu Kruskala
#         minSpinalTree = kruskal(edges, n)

#         # Wyświetlenie minimalnego drzewa spinającego
#         print('MINIMALNE DRZEWO SPINAJĄCE:')
#         total_cost = 0
#         for edge in minSpinalTree:
#             print(f"{edge['a']} {edge['b']} {edge['w']}")
#             total_cost += edge['w']
#         print(f'Łączny koszt: {total_cost}')

#         # Budowanie grafu oryginalnego
#         graph = build_graph(edges, n)

#         # Znajdowanie mostów
#         bridges = find_bridges(graph, n)

#         # Wyświetlanie mostów
#         print('\nMOSTY:')
#         if len(bridges) == 0:
#             print('BRAK MOSTÓW')
#         else:
#             for bridge in bridges:
#                 print(f"{bridge['u']} {bridge['v']}")

#         # Usunięcie mostów z grafu
#         for bridge in bridges:
#             remove_edge(graph, bridge['u'], bridge['v'])

#         # Znajdowanie komponentów
#         components = find_components(graph, n)

#         # Wyświetlanie komponentów
#         print('\nKOMPONENTY:')
#         components_str = ' '.join(['[' + ' '.join(map(str, comp)) + ']' for comp in components])
#         print(f"{len(components)} KOMPONENTY: {components_str}")

#     except Exception:
#         print('BŁĄD')


# # Moje kawałki

# # Szukanie mostów - wykorzystanie DFS
# class Graph:
#     def __init__(self, adjacency_list):
#         """Inicjalizacja grafu na podstawie listy sąsiedztwa."""
#         self.adjacency_list = adjacency_list

    
#     def getNeighbours(self, vertex_index):
#         """Zwraca sąsiadów wybranego wierzchołka na podstawie numeru wprowadzonego przez użytkownika."""
#         try:
            
#             # Pobranie listy sąsiadów
#             neighbors = self.adjacency_list[vertex_index][1:]
            
#             # # Wyświetlenie sąsiadów (jeśli istnieją)
#             # if neighbors:
#             #     print(f"Sąsiedzi wierzchołka {vertex_index + 1} to    -----: {', '.join(map(str, neighbors))}")
#             # else:
#             #     print(f"Wierzchołek {vertex_index + 1} nie ma sąsiadów.")
            
#             return neighbors

#         except IndexError:
#             print("BŁĄD: Nie można znaleźć sąsiadów dla podanego wierzchołka.")
#             exit(1)

#     def vertex_count(self):
#         """Zwraca liczbę wierzchołków w grafie."""
#         return len(self.adjacency_list)
    
#     def count_edges(self):
#         """Zlicza liczbę krawędzi w grafie."""
#         edge_count = 0  
    
#         for neighbors in self.adjacency_list:
#             edge_count += len(neighbors) - 1  # Odejmujemy 1, aby pominąć numer wierzchołka
        
#         return edge_count // 2  
    
#     def get_degrees(self):
#         '''Funkcja zwracająca ciąg stopni wierzchołków'''
#         degrees = []
#         for neighbors in self.adjacency_list:
#             degrees.append(len(neighbors) - 1)  # Odejmujemy 1, aby pominąć numer wierzchołka
#         return degrees
    
#     def dfs_iter(self, start):
#         """Przeszukiwanie grafu w głąb (DFS) w iteracyjnej wersji."""

#         n = len(self.adjacency_list)
#         visited = [False] * n  # Wszystkie wierzchołki oznaczamy jako nieodwiedzone
#         stack = [start]  # Stos zaczyna się od wierzchołka startowego (0-based)
#         order = []  # Kolejność odwiedzania wierzchołków

#         while stack:
#             # Pobieramy wierzchołek ze stosu
#             node = stack.pop()
#             node_neighbors = self.getNeighbours(node)
#             if not visited[node]:  # Jeśli wierzchołek jeszcze nie został odwiedzony
#                 visited[node] = True  # Oznacz jako odwiedzony
#                 order.append(node + 1)  # Dodajemy do porządku, ale jako 1-based

#                 # Dodaj sąsiadów do stosu w odwrotnej kolejności
#                 reversed_neighbors = sorted(node_neighbors, reverse=True)
#                 updated_neighbors = [neighbor - 1 for neighbor in reversed_neighbors] #odjęcie od każdego 1, zeby indexy sie zgadzaly
#                 for neighbor in updated_neighbors:
#                     if not visited[neighbor]:
#                         stack.append(neighbor)

#         return order, visited