import sys
def create_adjacency_list_no_weights(edges):
    """
    Tworzy listę sąsiedztwa dla grafu skierowanego bez uwzględniania wag.

    :param edges: Lista słowników reprezentujących krawędzie z wagami.
                  Każdy słownik zawiera 'a' (początek), 'b' (koniec) i 'w' (waga).
    :return: Słownik reprezentujący listę sąsiedztwa (tylko sąsiedzi, bez wag).
    """
    adjacency_list = {}
    
    for edge in edges:
        start = edge['a']
        end = edge['b']
        
        # Dodajemy wierzchołek początkowy, jeśli jeszcze nie istnieje
        if start not in adjacency_list:
            adjacency_list[start] = []
        
        # Dodajemy sąsiada
        adjacency_list[start].append(end)
        
        # Upewniamy się, że wierzchołek końcowy istnieje w grafie
        if end not in adjacency_list:
            adjacency_list[end] = []
    
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

def compare_numbers(num1, num2):
    if isinstance(num1, list) and isinstance(num2, list):
        return num1[0] - num2[0]  
    return num1 - num2 



# Funkcja max_heapify dla iteracyjnego przywracania własności kopca
def max_heapify_iter(Array, n, i, compare):
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        # Porównanie największego dotychczasowego elementu z lewym dzieckiem
        if left < n and compare(Array[left], Array[largest]) > 0:
            largest = left

        # Porównanie największego dotychczasowego elementu z prawym dzieckiem
        if right < n and compare(Array[right], Array[largest]) > 0:
            largest = right

        # Jeśli największy element to nie rodzic, wykonaj zamianę
        if largest != i:
            Array[i], Array[largest] = Array[largest], Array[i]
            i = largest
        else:
            break

# Funkcja heapsort, sortująca listę przy użyciu kopca
def heapSort(Array, compare):
    n = len(Array)

    # Budowanie kopca max
    lpn = n // 2 - 1  # ostatni węzeł rodzica
    end = -1  # aby obejmowało także index 0 
    step = -1  # cofanie się o krok
    for i in range(lpn, end, step):
        max_heapify_iter(Array, n, i, compare)

    # Sortowanie kopcowe
    lastElement = n - 1
    step = -1  # cofanie
    for i in range(lastElement, 0, step):  # i to aktualna ilość elementów do sortowania
        # Zmiana największego elementu z Max heap (root) z ostatnim elementem
        Array[i], Array[0] = Array[0], Array[i]

        # Przywracanie własności kopca dla zmniejszonej tablicy
        max_heapify_iter(Array, i, 0, compare)


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
def dfs(edges, start, visited, component=None, excluded_edge=None):
    """
    Przeszukiwanie grafu w głąb.
    :param excluded_edge: Krawędź do pominięcia w formacie (v, u).
    """
    stack = [start]  # Stos do śledzenia wierzchołków do odwiedzenia
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            if component is not None:
                component.append(node)  # Dodajemy wierzchołek do komponentu
            print(f"Odczytano wierzchołek: {node}")  # Debugowanie

            # Znajdź sąsiadów wierzchołka, z pominięciem excluded_edge
            neighbors = []
            for edge in edges:
                if edge['a'] == node and (excluded_edge is None or (node, edge['b']) != excluded_edge):
                    neighbors.append(edge['b'])
                elif edge['b'] == node and (excluded_edge is None or (node, edge['a']) != excluded_edge):
                    neighbors.append(edge['a'])
           
            print(f"Sąsiedzi {node}: {neighbors}")  # Debugowanie

            # Dodaj sąsiadów do stosu
            for neighbor in neighbors:
                if not visited[neighbor]:
                    stack.append(neighbor)


#Sprawdza każdą krawędź, wykluczając ją z grafu, i wykonuje DFS. Jeśli wierzchołek końcowy tej krawędzi jest nieosiągalny, to jest to most.
def findBridges(edges):
    """
    Znajduje mosty w grafie reprezentowanym jako lista krawędzi.

    :param edges: Lista krawędzi w formacie [{'a': początkowy node, 'b': końcowy node, 'w': waga}].
    :return: Lista mostów w formacie [(v, u)].
    """
    bridges = []

    # Zbierz wszystkie wierzchołki w grafie
    nodes = set()
    for edge in edges:
        nodes.add(edge['a'])
        nodes.add(edge['b'])

    # Sprawdzamy każdą krawędź, czy jest mostem
    for edge in edges:
        v, u = edge['a'], edge['b']

        # Lista odwiedzonych wierzcholkow
        visited = {node: False for node in nodes}

        # Wykonaj DFS z wykluczeniem tej krawędzi
        dfs(edges, v, visited, excluded_edge=(v, u))

        # Jeśli wierzchołek u nie został odwiedzony, to (v, u) jest mostem
        if not visited[u]:
            bridges.append((v, u))

    return bridges




#---------------------------------------------------------------Szukanie komponentów
def removeBridges(edges, bridges, nodes):
    """
    Usuwa mosty z listy krawędzi, ale zachowuje wszystkie wierzchołki.
    """
    new_edges = []
    
    # Dodajemy wszystkie krawędzie, które nie są mostami
    for edge in edges:
        if not any((edge['a'] == bridge[0] and edge['b'] == bridge[1]) or (edge['a'] == bridge[1] and edge['b'] == bridge[0]) for bridge in bridges):
            new_edges.append(edge)

    # Upewniamy się, że graf zawiera wszystkie wierzchołki (nawet izolowane)
    for node in nodes:
        # Dodajemy wierzchołki jako osobne krawędzie bezpośrednie (izolowane wierzchołki)
        if not any(edge['a'] == node or edge['b'] == node for edge in new_edges):
            new_edges.append({'a': node, 'b': node, 'w': 0})  # Krawędź do samego siebie

    # Teraz posortuj krawędzie przed dalszym przetwarzaniem
    heapSort(new_edges, compare_edges)  # Sortowanie krawędzi

    return new_edges





def findComponents(edges):
    """
    Znajduje komponenty spójności w grafie.
    """
    nodes = set()
    for edge in edges:
        nodes.add(edge['a'])
        nodes.add(edge['b'])
    
    visited = {node: False for node in nodes}
    components = []

    for node in visited.keys():
        if not visited[node]:
            component = []
            # Rozpoczynamy DFS od wierzchołka
            dfs(edges, node, visited, component)
            # Posortuj komponent przy użyciu heapSort
            heapSort(component, compare_numbers)  # Sortowanie elementów w komponencie
            components.append(component)

    # Sprawdzamy wierzchołki, które nie zostały odwiedzone (izolowane wierzchołki)
    isolated_nodes = [node for node in nodes if not visited[node]]
    for isolated_node in isolated_nodes:
        components.append([isolated_node])  # Dodajemy jako osobny komponent

    # Sortowanie komponentów
    heapSort(components, compare_numbers)  # Sortowanie komponentów według numerów wierzchołków

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

        adj_list = create_adjacency_list_no_weights(edges)

        print("{")
        for i, (node, neighbors) in enumerate(adj_list.items()):
            neighbors_str = ", ".join(map(str, neighbors))
            comma = "," if i < len(adj_list) - 1 else ""
            print(f"    {node}: [{neighbors_str}]{comma}")
        print("}")

        # Sortowanie krawędzi na podstawie wagi
        heapSort(edges, compare_edges)

        print(f"posortowane krawędzie {edges}")

        minSpinalTree, total_weight = kruskal(edges, n)

        # Wyświetlenie minimalnego drzewa spinającego
        print('MINIMALNE DRZEWO SPINAJĄCE:')
        total_cost = 0
        for edge in minSpinalTree:
            print(f"{edge['a']} {edge['b']} {edge['w']}")
            total_cost += edge['w']
        print(f'Łączny koszt: {total_cost}')

        #-----------------------------------------------------------Szukanie mostów    
        # Wyszukiwanie mostów
        bridges = findBridges(edges)

        # Sortowanie mostów
        heapSort(bridges, compare_numbers)

        # Wyświetlanie mostów
        print('\nMOSTY:')
        if len(bridges) == 0:
            print('BRAK MOSTÓW')
        else:
            for bridge in bridges:
                print(f"{bridge[0]} {bridge[1]}")  
        # --------------------------------------------------------Szukanie komponentów

        # Usuwanie mostów
        nodes = set()
        for edge in edges:
            nodes.add(edge['a'])
            nodes.add(edge['b'])

        edges_without_bridges = removeBridges(edges, bridges, nodes)

        components = findComponents(edges_without_bridges)
        #print(f"Komponenty przed sortowaniem: {components}")

        heapSort(components, compare_numbers)

        #print(f"Komponenty po sortowaniu: {components}")

        # Wyświetlanie komponentów
        print('\nKOMPONENTY:')
        components_str = ' '.join(['[' + ' '.join(map(str, comp)) + ']' for comp in components])
        print(f"{len(components)} KOMPONENTY: {components_str}")



    except Exception:
        print('BŁĄD')



