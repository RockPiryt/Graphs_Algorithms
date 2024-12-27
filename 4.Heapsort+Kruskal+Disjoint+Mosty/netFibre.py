import sys

def parse_edges(input_lines, n, m):
    '''
    Parsuje wejściowe dane krawędzi, upewniając się, że każda krawędź jest poprawna.
    '''
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
        edges.append({'a': a, 'b': b, 'w': w})

    return edges

def create_adj_list(edges):
    '''
    Tworzy listę sąsiedztwa dla grafu nieskierowanego bez uwzględniania wag.

    :param edges: Lista słowników reprezentujących krawędzie z wagami.
                  Każdy słownik zawiera 'a' (początek), 'b' (koniec) i 'w' (waga).
    :return: Słownik reprezentujący listę sąsiedztwa (tylko sąsiedzi, bez wag).
    '''
    adjacency_list = {}

    for edge in edges:
        start = edge['a']
        end = edge['b']

        # Dodaj początkowy wierzchołek, jeśli nie istnieje
        if start not in adjacency_list:
            adjacency_list[start] = []
        if end not in adjacency_list:
            adjacency_list[end] = []

        # Dodaj sąsiedztwo w obu kierunkach
        adjacency_list[start].append(end)
        adjacency_list[end].append(start)

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

# #-----------------------------------------------------------------------------------Znajdowanie  komponentów za pomocą dfs
def dfs_iter(adj_list, start):
    visited = {node: False for node in adj_list}
    stack = [start]
    order = []

    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            order.append(node)

            for neighbor in adj_list[node]:
                if not visited[neighbor]:
                    stack.append(neighbor)

    return order, visited

# znajdowanie komponentów spójności w analizownym grafie
def find_components(adj_list):
    visited = {node: False for node in adj_list}
    components = []

    for node in adj_list:
        if not visited[node]:
            order, _ = dfs_iter(adj_list, node)
            components.append(order)
            for v in order:
                visited[v] = True

    return components

#tworzy listę sasiedztwa dla komponentów spójności
def create_component_adj_lists(adj_list):
    components = find_components(adj_list)

    # If there's only one component, return the original adjacency list
    if len(components) == 1:
        return [adj_list]

    # Create adjacency lists for each component
    component_adj_lists = []

    for component in components:
        component_adj_list = {node: [] for node in component}
        for node in component:
            component_adj_list[node] = [neighbor for neighbor in adj_list[node] if neighbor in component]
        component_adj_lists.append(component_adj_list)

    return component_adj_lists

# sprawdzanie cykliczności grafu na podstawie lsty sąsiedztwa
def get_degrees(graph):
    return [len(neighbors) for neighbors in graph.values()]

def is_cycle(component):
    vertex_count = len(component)
    print(f"ilosc vertexów {vertex_count}")

    # Zliczanie unikalnych krawędzi
    unique_edges = set()
    for vertex, neighbors in component.items():
        for neighbor in neighbors:
            edge = tuple(sorted((vertex, neighbor)))
            unique_edges.add(edge)
    
    edge_count = len(unique_edges)
    print(f"ilosc krawedzi {edge_count}")


    # Sprawdzanie, czy ilość krawędzi = ilość wierzchołków
    if vertex_count != edge_count:
        return False

    # Każdy wierzchołek musi mieć stopień 2
    degrees = get_degrees(component)
    print(f"stopnie w komponencie{degrees}")

    for degree in degrees:
        if degree != 2:
            return False

    return True

def find_bridges(graph):
    '''Funkcja znajdująca mosty w grafie przez usuwanie krawędzi'''
    bridges = []

    for node in graph:
        for neighbor in list(graph[node]):
            # Tworzymy nową listę krawędzi bez aktualnej
            modified_graph = {n: list(neigh) for n, neigh in graph.items()}
            if neighbor in modified_graph[node]:
                modified_graph[node].remove(neighbor)
            if node in modified_graph[neighbor]:
                modified_graph[neighbor].remove(node)

            # Sprawdzamy, czy graf pozostaje spójny
            original_component = dfs_iter(graph, node)[0]
            modified_component = dfs_iter(modified_graph, node)[0]

            if len(original_component) != len(modified_component):
                if (node, neighbor) not in bridges and (neighbor, node) not in bridges:
                    bridges.append((node, neighbor))

    return bridges

def remove_bridges_from_components(component_adj_lists):
    '''
    Usuwa mosty z każdego komponentu grafu.

    :param component_adj_lists: Lista list sąsiedztwa dla każdego komponentu.
    :return: Lista list sąsiedztwa po usunięciu mostów.
    '''
    updated_components = []

    for component in component_adj_lists:
        # Znajdź mosty w bieżącym komponencie
        bridges = find_bridges(component)
        # print(f"Mosty w komponencie: {bridges}")

        # Utwórz nową listę sąsiedztwa bez mostów
        updated_adj_list = {node: [] for node in component}
        for node, neighbors in component.items():
            for neighbor in neighbors:
                if (node, neighbor) not in bridges and (neighbor, node) not in bridges:
                    updated_adj_list[node].append(neighbor)

        updated_components.append(updated_adj_list)

    return updated_components

def format_components_after_removal(components):
    '''
    Formatuje listę komponentów spójności po usunięciu mostów.

    :param components: Lista list sąsiedztwa dla każdego komponentu.
    :return: Sformatowany string reprezentujący komponenty spójności.
    '''
    all_components = []

    for component in components:
        # Oddziel wierzchołki z pustą listą sąsiedztwa jako osobne komponenty
        single_nodes = [node for node, neighbors in component.items() if not neighbors]
        grouped_nodes = [node for node, neighbors in component.items() if neighbors]

        # Dodaj pojedyncze wierzchołki jako osobne komponenty
        for node in single_nodes:
            all_components.append([node])

        # Dodaj spójny komponent jako grupę
        if grouped_nodes:
            all_components.append(grouped_nodes)

    # Formatowanie wynikowego stringa
    formatted_components = f"{len(all_components)} KOMPONENTY: "
    formatted_components += ' '.join(
        f"[{' '.join(map(str, sorted(component)))}]" for component in all_components
    )
    return formatted_components



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

        edges = parse_edges(input_lines, n, m)  # Parsowanie krawędzi

        print(f"Krawędzie z wagami {edges}")

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

        #-----------------------------------------------------------Sprawdzanie spojnosci i cykliczności grafu 
        adj_list = create_adj_list(edges)
        print("lista sasiedztwa")
        print(adj_list)


        # Znajdowanie komponentów
        komponenty = find_components(adj_list)
        print(f"{len(komponenty)} składowe spójnościw grafie:", komponenty)

        component_adj_lists = create_component_adj_lists(adj_list)

        
        # Wyświetlenie wyników
        component_id = 1
        for comp_adj_list in component_adj_lists:
            print(f"Komponent w oryginalnym grafie {component_id}:", comp_adj_list)
            component_id += 1

        # -----------------------------------------------Znalezienie mostów w każdej składowej
        # component_id = 1
        # for comp_adj_list in component_adj_lists:
        #     bridges = find_bridges(comp_adj_list)
        #     print(f"Mosty w składowej {component_id}: {bridges}")
        #     component_id += 1

        # # Wyświetlanie mostów
        # print('\nMOSTY:')
        # if len(bridges) == 0:
        #     print('BRAK MOSTÓW')
        # else:
        #     for bridge in bridges:
        #         print(f"{bridge[0]} {bridge[1]}")  
            
        # Znalezienie i wypisanie mostów
        all_bridges = []
        for comp_adj_list in component_adj_lists:
            bridges = find_bridges(comp_adj_list)
            all_bridges.extend(bridges)  # Dodaj mosty z bieżącej składowej do wspólnej listy

        # Wyświetlenie mostów
        if all_bridges:
            print("MOSTY:")
            for bridge in sorted(all_bridges):
                print(f"{bridge[0]} {bridge[1]}")
        else:
            print("BRAK MOSTÓW")

        # # Sprawdzenie, czy graf jest cyklem
        # component_id = 1
        # for comp_adj_list in component_adj_lists:
        #     is_cycle_graph = is_cycle(comp_adj_list)
        #     print(f"Składowa {component_id} jest cyklem: {is_cycle_graph}")
        #     component_id += 1

        #----------------------------------------------------szukanie komponentów po usunieciu mostów 
        updated_components = remove_bridges_from_components(component_adj_lists)
        # print("Komponenty po usunięciu mostów:")
        # for i, comp in enumerate(updated_components, start=1):
        #     print(f"Komponent {i}: {comp}")

        print('\nKOMPONENTY:')
        formatted = format_components_after_removal(updated_components)
        print(formatted)


        # # Znajdowanie mostów
        # mosty = find_bridges(adj_list)
        # print("MOSTY:", mosty)


        # # Wyszukiwanie mostów
        # bridges = find_Bridges(adj_list)

        # # Sortowanie mostów
        # # heapSort(bridges, compare_numbers)

        # # Wyświetlanie mostów
        # print('\nMOSTY:')
        # if len(bridges) == 0:
        #     print('BRAK MOSTÓW')
        # else:
        #     for bridge in bridges:
        #         print(f"{bridge[0]} {bridge[1]}")  
        # # # --------------------------------------------------------Szukanie komponentów

        # # # Usuwanie mostów
        # # nodes = set()
        # # for edge in edges:
        # #     nodes.add(edge['a'])
        #     nodes.add(edge['b'])

        # edges_without_bridges = removeBridges(edges, bridges, nodes)

        # components = findComponents(edges_without_bridges)
        # #print(f"Komponenty przed sortowaniem: {components}")

        # heapSort(components, compare_numbers)

        # #print(f"Komponenty po sortowaniu: {components}")

        # # Wyświetlanie komponentów
        # print('\nKOMPONENTY:')
        # components_str = ' '.join(['[' + ' '.join(map(str, comp)) + ']' for comp in components])
        # print(f"{len(components)} KOMPONENTY: {components_str}")



    # except Exception:
    #     print('BŁĄD')



