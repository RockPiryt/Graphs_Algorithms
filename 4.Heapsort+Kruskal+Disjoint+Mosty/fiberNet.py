import sys

# --------------------------------------------Tworzenie grafu jako listy sąsiedztwa
def create_adjacency_list(edges):
    """
    Tworzy listę sąsiedztwa w postaci słownika  dla nieskierowanego grafu, uwzględniając wierzchołki bez sąsiadów (możliwość grafu niespójnego).
    edges to Lista krawędzi, gdzie każda krawędź jest słownikiem {'a': początek, 'b': koniec, 'w': waga}.
    """
    adjacency_list = {}

    # Dodaj wszystkie wierzchołki do listy sąsiedztwa z pustymi listami (w przypadku grafu niespójnego)
    for edge in edges:
        a, b = edge['a'], edge['b']
        if a not in adjacency_list:
            adjacency_list[a] = []
        if b not in adjacency_list:
            adjacency_list[b] = []

    # Dodaj krawędzie do listy sąsiedztwa
    for edge in edges:
        a, b, w = edge['a'], edge['b'], edge['w']
        
        # Dodanie krawędzi (a -> b)
        adjacency_list[a].append((b, w))
        
        # Dodanie krawędzi (b -> a)
        adjacency_list[b].append((a, w))
    
    return adjacency_list

# --------------------------------------------Sortowanie lity za pomocą heapSort
def compare_edges(edge1, edge2):
    # Pierwszeństwo mają krawędzie o mniejszej wadze
    if edge1['w'] != edge2['w']:
        return edge1['w'] - edge2['w']  
    # Przy równych wagach decyduje mniejszy numer pierwszego wierzchołka
    if edge1['a'] != edge2['a']:
        return edge1['a'] - edge2['a'] 
    # Przy równych pierwszych wierzchołkach decyduje mniejszy numer drugiego wierzchołka
    if edge1['b'] != edge2['b']:
        return edge1['b'] - edge2['b']  
    return 0  # Są równe

def max_heapify_iter(Array, n, i):
    # Wykonywana dopóki własność kopca nie zostanie przywrócona. Przerywana, gdy largest == i, co oznacza, że rodzic jest większy lub równy swoim dzieciom.
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        # Porównanie największego dotychczasowego elementu z lewym dzieckiem
        # if left < n and Array[left] > Array[largest] :
        if left < n and compare_edges(Array[left], Array[largest]) > 0:
            largest = left

        # Porównanie największego dotychczasowego elementu z prawym dzieckiem
        # if right < n and Array[right] > Array[largest]:
        if right < n and compare_edges(Array[right], Array[largest]) > 0:
            largest = right

        # Jeśli największy element to nie rodzic, wykonaj zamianę
        if largest != i:
            Array[i], Array[largest] = Array[largest], Array[i]
            # Przesuwamy się do dziecka i kontynuujemy przywracanie własności kopca
            i = largest
        else:
            # Własność kopca została przywrócona
            break

def heapSort(Array):
    n=len(Array)

    # Build Heap Max
    lpn = n//2 - 1 #last parent node
    end = -1 #aby objeło także index 0 
    step = -1 # cofanie się o krok ndeksy odwiedzane przez pętlę: lpn =2, lpn-1=1 lpn-2=0(root)
    for i in range(lpn, end, step):
        max_heapify_iter(Array, n, i)

     # Sortowanie kopcowe
    lastElement = n - 1 
    step = -1 # cofanie
    for i in range (lastElement, 0, step):# i to  aktualna ilość elementów do sortowania, najpierw są wszystkie elementy, potem o 1 mniej itd.  6,5,4,3,2,1
        #Zmiana największego elementu z Max heap (root) z ostatnim elementem
        Array[i], Array[0] =  Array[0], Array[i]

          # Przywracanie własności kopca dla zmniejszonej tablicy
        max_heapify_iter(Array, i , 0)

# ----------------------------------------DisjointSet
class DisjointSet:
    def __init__(self, n):
        # zestaw zbiorów 1 elementowych, gdzie każdy wierzchołek jest swoim rodzicem
        self.parent = list(range(n + 1))  # Indeksy od 1 do n
        self.rank = [0] * (n + 1)        
    def Find_parent(self, x):
        # jeśli jest sam dla siebie rodzicem
        if x == self.parent[x]:
            return x
        # w przeciwnym wypadku szukaj rodzica subset
        else:
            #rekurencyjne wywołanie
            self.parent[x] = self.Find_parent(self.parent[x])
            return self.parent[x]

    def union(self, x, y):
        xRoot = self.Find_parent(x)
        yRoot = self.Find_parent(y)

        if xRoot == yRoot: # x and y are already in the same set
            print("Cyclic Grpah")
            return  

        #Uczycie rank jest szybsze (nlogn)
        # Union by rank: attach smaller rank tree under the root of the higher rank tree ( dołączenie rzadszego drzewa pod gęstsze drzewo)
        if self.rank[xRoot] < self.rank[yRoot]:
            self.parent[xRoot] = yRoot
        elif self.rank[xRoot] > self.rank[yRoot]:
            self.parent[yRoot] = xRoot
        else:
            # If ranks are the same, make one root and increment its rank
            self.parent[yRoot] = xRoot
            self.rank[xRoot] += 1

# # Implementacja algorytmu Kruskala - do szukania minialnego drzewa spinajacego
def kruskal(edges, n):
    # Inicjalizacja zbiorów rozłącznych
    ds = DisjointSet(n)
    
    # Sortowanie krawędzi na podstawie wagi
    heapSort(edges)
    
    # Inicjalizacja listy krawędzi w MST (Minimalnym Drzewie Rozpinającym)
    mst = []
    total_weight = 0

    # Przetwarzanie każdej krawędzi w kolejności rosnącej wag
    for edge in edges:
        u = edge['a']
        v = edge['b']
        weight = edge['w']
        
        # Sprawdzenie, czy wierzchołki `u` i `v` są w tym samym zbiorze
        if ds.Find_parent(u) != ds.Find_parent(v):
            # Dodanie krawędzi do MST
            mst.append(edge)
            total_weight += weight
            
            # Połączenie zbiorów
            ds.union(u, v)
    
    return mst, total_weight

#-----------------------------------------------------------------------------------Znajdowanie mostów za pomocą dfs
def dfs_iter(graph, start, excluded_edge):
    """
    :param excluded_edge: Krawędź, którą chcemy pominąć (w formacie (v, u)).
    :return: Lista odwiedzonych wierzchołków.
    """
    n = len(graph)  # Liczba wierzchołków
    visited = [False] * n  
    stack = [start - 1]  # Stos zaczyna się od wierzchołka startowego (0-based)
    
    while stack:
        node = stack.pop()
        node_neighbors = graph[node][1:]  # Pobieramy sąsiadów wierzchołka (pomijamy indeks)
        
        if not visited[node]:  
            visited[node] = True  

            # Dodaj sąsiadów do stosu, omijając excluded_edge
            for neighbor, _ in node_neighbors:
                #Graf jest nieskierowany, więc krawędź (node, neighbor) jest taka sama jak (neighbor, node). Chcemy upewnić się, że żadna z tych dwóch wersji krawędzi nie jest tą, którą wykluczamy.
                if not visited[neighbor - 1] and (node + 1, neighbor) != excluded_edge and (neighbor, node + 1) != excluded_edge:
                    stack.append(neighbor - 1)  # Dodajemy 0-based index

    return visited

def isConnected(graph, n, start, excluded_edge):
    """
    Sprawdza, czy graf pozostaje spójny po usunięciu krawędzi.

    :param graph: Lista sąsiedztwa reprezentująca graf (wierzchołek, sąsiad, waga).
    :param n: Liczba wierzchołków.
    :param start: Wierzchołek początkowy (1-based).
    :param excluded_edge: Krawędź, którą ma zostać usunięta z grafu (w formacie (v, u)).
    :return: True, jeśli graf pozostaje spójny, w przeciwnym razie False.
    """
    visited = [False] * n

    # Używamy funkcji dfs_iter, sprawdzając spójność po usunięciu krawędzi
    visited = dfs_iter(graph, start, excluded_edge)

    return all(visited)

def findBridges(graph, n):

    bridges = []

    # Iterujemy po każdej krawędzi w grafie
    for v in range(n):
        for u, _ in graph[v]:  # Ignorujemy wagę krawędzi
            if v < u:  # Sprawdzamy każdą krawędź tylko raz
                if not isConnected(graph, n, v + 1, (v + 1, u + 1)):  # Sprawdzamy, czy usunięcie krawędzi powoduje rozdzielenie
                    bridges.append((v + 1, u + 1))
    #Lista mostów w postaci krotek (v, u).
    return bridges




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

        print(f"Krawędzie z wagami {edges}")

        minSpinalTree, total_weight = kruskal(edges, n)

        # Wyświetlenie minimalnego drzewa spinającego
        print('MINIMALNE DRZEWO SPINAJĄCE:')
        total_cost = 0
        for edge in minSpinalTree:
            print(f"{edge['a']} {edge['b']} {edge['w']}")
            total_cost += edge['w']
        print(f'Łączny koszt: {total_cost}')

        #-----------------------------------------------------------Szukanie mostów    
        # Budowanie grafu oryginalnego jako lista sąsiedztwa 
        graph_adj_list = create_adjacency_list(edges)
        # Wyświetlenie listy sąsiedztwa
        for node, neighbors in graph_adj_list.items():
            print(f"{node}: {neighbors}")

        # Znajdowanie mostów
        bridges = findBridges(graph_adj_list, n)

        # Wyświetlenie mostów
        print("Mosty w grafie:", bridges)

        # Znajdowanie mostów
#         bridges = find_bridges(graph_adj_list, n)
            

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
    
# def isConnected(graph, n, start, excluded_edge):
# visited = [False] * n

# def dfs(v):
#     visited[v] = True
#     for u in graph[v]:
#         if not visited[u] and (v, u) != excluded_edge and (u, v) != excluded_edge:
#             dfs(u)

# dfs(start)
# return all(visited)

# def findBridges(graph, n):
#     bridges = []

#     for v in range(n):
#         for u in graph[v]:
#             if v < u: # Sprawdź każdą krawędź tylko raz
#                 if not isConnected(graph, n, v, (v, u)):
#                     bridges.append((v, u))

#     return bridges