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

    print(f"posortowane krawędzie {edges}")
    
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
# Sprawdza, czy wierzchołek `end` jest osiągalny z wierzchołka `start`  po usunięciu krawędzi `excluded_edge`.
def isConnected(graph, start, end, excluded_edge):
    """
    :param excluded_edge: Krawędź do pominięcia (w formacie (v, u)).
    :return: True, jeśli `end` jest osiągalny z `start`, w przeciwnym razie False.
    """
    visited = {v: False for v in graph}
    stack = [start]

    while stack:
        node = stack.pop()
        if node == end:
            return True  # Znaleziono połączenie między start a end
        if not visited[node]:
            visited[node] = True
            for neighbor, _ in graph[node]:
                if (node, neighbor) != excluded_edge and (neighbor, node) != excluded_edge:
                    stack.append(neighbor)

    return False  # Nie znaleziono połączenia


def removeBridges(graph, bridges):

    # Usuwanie mostów z listy sąsiedztwa
    for bridge in bridges:
        v, u = bridge
        
        # Usuwamy krawędź v -> u i u -> v
        graph[v] = [(neighbor, weight) for neighbor, weight in graph[v] if neighbor != u]
        graph[u] = [(neighbor, weight) for neighbor, weight in graph[u] if neighbor != v]
    
    #Zaktualizowana lista sąsiedztwa po usunięciu mostów.
    return graph
#---------------------------------------------------------------Szukanie komponentów
#nowe do wspólnego dfs
def dfs(graph, start, visited, component=None, excluded_edge=None):
    """
    :param component: Lista do zapisywania wierzchołków aktualnego komponentu (opcjonalnie).
    :param excluded_edge: Krawędź do pominięcia w formacie (v, u) (opcjonalnie).
    """
    stack = [start]
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            if component is not None:
                component.append(node)
            for neighbor, _ in graph[node]:
                if excluded_edge is None or (node, neighbor) != excluded_edge and (neighbor, node) != excluded_edge:
                    if not visited[neighbor]:
                        stack.append(neighbor)

def findBridges(graph):
    """
    Znajduje mosty w grafie.

    :param graph: Lista sąsiedztwa jako słownik {wierzchołek: [(sąsiad, waga)]}.
    :return: Lista mostów w formacie [(v, u)].
    """
    bridges = []

    for v in graph:
        for u, _ in graph[v]:
            if v < u:  # Rozważamy każdą krawędź tylko raz
                # Sprawdzamy, czy usunięcie krawędzi (v, u) powoduje rozdzielenie grafu
                visited = {node: False for node in graph}
                dfs(graph, v, visited, excluded_edge=(v, u))
                if not visited[u]:  # Jeśli u nie zostało odwiedzone, to (v, u) jest mostem
                    bridges.append((v, u))

    return bridges

def findComponents(graph):
    """
    Znajduje komponenty spójności w grafie.
    """
    visited = {v: False for v in graph}
    components = []
    for node in graph:
        if not visited[node]:
            component = []
            dfs(graph, node, visited, component)
            components.append(component)
    heapSort(components)
    return components

if __name__ == '__main__':
    try:
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
        print("lista sąsiedztwa")
        for node, neighbors in graph_adj_list.items():
            print(f"{node}: {neighbors}")

        # Znajdowanie mostów
        bridges = findBridges(graph_adj_list)

        # Wyświetlanie mostów
        print('\nMOSTY:')
        if len(bridges) == 0:
            print('BRAK MOSTÓW')
        else:
            for bridge in bridges:
                print(f"{bridge[0]} {bridge[1]}")  

        # ------------------------------------------------szukanie komponentów

        # Usuwanie mostów z grafu
        graph_adj_list = removeBridges(graph_adj_list, bridges)

        # Wyświetlanie zaktualizowanej listy sąsiedztwa po usunięciu mostów
        print("\nZaktualizowana lista sąsiedztwa po usunięciu mostów:")
        for node, neighbors in graph_adj_list.items():
            print(f"{node}: {neighbors}")
        
        # Znalezienie komponentów spójności
        components = findComponents(graph_adj_list)

        # Wyświetlanie komponentów
        print('\nKOMPONENTY:')
        components_str = ' '.join(['[' + ' '.join(map(str, comp)) + ']' for comp in components])
        print(f"{len(components)} KOMPONENTY: {components_str}")

    except Exception:
        print('BŁĄD')


