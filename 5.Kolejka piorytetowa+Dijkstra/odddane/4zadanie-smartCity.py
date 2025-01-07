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
        # Upewnienie się, że a ≤ b
        if a > b:
            a, b = b, a
        edges.append({'a': a, 'b': b, 'w': w})

    return edges

def get_data():

    input_lines = sys.stdin.read().strip().split('\n')

    if len(input_lines) < 2:
        raise ValueError("BŁĄD")

    try:
        # Parsowanie liczby wierzchołków (n) i krawędzi (m)
        n, m = map(int, input_lines[0].split())
    except ValueError:
        raise ValueError("BŁĄD")

    # Weryfikacja zakresu dla n i m
    if n < 2 or n > 100 or m < n - 1 or m > (n * (n - 1)) // 2:
        raise ValueError("BŁĄD.")

    # Wywołanie `parse_edges` do przetworzenia krawędzi
    edges = parse_edges(input_lines, n, m)

    return n, m, edges

#Tworzy listę sąsiedztwa dla grafu nieskierowanego bez uwzględniania wag.
def create_adj_list(edges):

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

#Tworzy listę sąsiedztwa dla grafu nieskierowanego z wagami.
def create_adjacency_list_with_weights(n, edges):
    '''
    Tworzy listę sąsiedztwa z wagami na podstawie listy krawędzi.
    '''
    adjacency_list = {}
    for edge in edges:
        a, b, w = edge['a'], edge['b'], edge['w']
        if a not in adjacency_list:
            adjacency_list[a] = []
        if b not in adjacency_list:
            adjacency_list[b] = []
        adjacency_list[a].append((b, w))
        adjacency_list[b].append((a, w))  # Ponieważ graf jest nieskierowany

    return adjacency_list
# #############################################################Szukanie MST za pomoca heapsort, Disjonint set oraz kruskala
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

########################################################################Dijkstra z piority queue bo potrzebne do średnicy oraz peryferium 
#lista kolejkowa w oparciu o min heap
class PiorityQueue:
    def __init__(self, capacity):
        self.storage = [None] * capacity
        self.capacity = capacity
        self.size = 0

    def getParentIndex(self, index):
        return (index - 1) // 2

    def getLeftChildIndex(self, index):
        return 2 * index + 1

    def getRightChildIndex(self, index):
        return 2 * index + 2

    def hasParent(self, index):
        return self.getParentIndex(index) >= 0

    def hasLeftChild(self, index):
        return self.getLeftChildIndex(index) < self.size

    def hasRightChild(self, index):
        return self.getRightChildIndex(index) < self.size

    def swap(self, index1, index2):
        self.storage[index1], self.storage[index2] = self.storage[index2], self.storage[index1]

    def resize(self):
        """Podwaja pojemność kopca."""
        self.capacity *= 2
        self.storage.extend([None] * (self.capacity - len(self.storage)))

    def insertHeap(self, element):
        if self.size == self.capacity:
            self.resize()  # Zwiększenie rozmiaru kopca
        self.storage[self.size] = element
        self.size += 1
        self.heapifyUp()

    def heapifyUp(self):
        index = self.size - 1
        while self.hasParent(index):
            parent_index = self.getParentIndex(index)
            if self.storage[parent_index][0] <= self.storage[index][0]:
                break
            self.swap(parent_index, index)
            index = parent_index

    def removeFromHeap(self):
        if self.size == 0:
            raise Exception("Kopiec pusty")
        removed_element = self.storage[0]
        self.storage[0] = self.storage[self.size - 1]
        self.size -= 1
        self.heapifyDown()
        return removed_element

    def heapifyDown(self):
        index = 0
        while self.hasLeftChild(index):
            smaller_child_index = self.getLeftChildIndex(index)
            if self.hasRightChild(index) and self.storage[self.getRightChildIndex(index)][0] < self.storage[smaller_child_index][0]:
                smaller_child_index = self.getRightChildIndex(index)
            if self.storage[index][0] <= self.storage[smaller_child_index][0]:
                break
            self.swap(index, smaller_child_index)
            index = smaller_child_index

    def printHeap(self):
        print("Kopiec:", self.storage[:self.size])

#-------------------------------------------------------------Dijkstra z piority queue
def dijkstra(graph, start):
    # Determine the number of vertices in the graph
    num_vertex = len(graph)

    # Initialize previous, visited, and distances dictionaries
    previous = {v: None for v in range(1, num_vertex + 1)}
    visited = {v: False for v in range(1, num_vertex + 1)}
    distances = {v: float("inf") for v in range(1, num_vertex + 1)}
    distances[start] = 0

    # Initialize PriorityQueue with a capacity of the number of vertices
    min_heap = PiorityQueue(num_vertex)

    # Insert the start vertex with a distance of 0 into the heap
    min_heap.insertHeap((distances[start], start))

    while min_heap.size > 0:
        removed_distance, removed_vertex = min_heap.removeFromHeap()
        visited[removed_vertex] = True

        # Explore all neighbors of the current vertex
        for neighbor, weight in graph[removed_vertex]:
            # If the vertex has been visited, skip it
            if visited[neighbor]:
                continue

            if weight > 0:  
                new_distance = removed_distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = removed_vertex

                    # Add the neighbor to the heap with the updated distance
                    min_heap.insertHeap((new_distance, neighbor))

    return distances

# ------------------------------------------------------------Główne parametry grafu - średnica, promien, peryferium, centrum
# Oblicza średnicę grafu wykorzystując algorytm Dijkstry.
def graph_diameter_with_dijkstra(graph):
    max_distances = []

    for start_vertex in graph.keys():  # Iterujemy po kluczach listy sąsiedztwa
        distances = dijkstra(graph, start_vertex)
        # Maksymalna odległość z danego wierzchołka
        max_distance = max(distances.values())
        max_distances.append(max_distance)

    # Średnica grafu to największa odległość
    return max(max_distances)

# Znajduje peryferium grafu, czyli wierzchołki, dla których maksymalna odległość do innego wierzchołka równa się średnicy grafu.
def find_periphery(graph, diameter):
    periphery = []

    for start_vertex in graph.keys():
        distances = dijkstra(graph, start_vertex)
        max_distance = max(distances.values())

        # Jeśli maksymalna odległość równa średnicy, dodaj wierzchołek do peryferium
        if max_distance == diameter:
            periphery.append(start_vertex)  # Konwersja na 1-based index

    return sorted(periphery)  

def graph_radius(graph):
    eccentricities = {}

    for start_vertex in graph.keys():
        distances = dijkstra(graph, start_vertex)
        max_distance = max(distances.values())
        #peryferium = max odleglość
        eccentricities[start_vertex] = max_distance

    # Promień grafu to najmniejsza wartość z eccentricity
    radius = min(eccentricities.values())

    return radius

def graph_center(graph):
    eccentricities = {}

    for start_vertex in graph.keys():
        distances = dijkstra(graph, start_vertex)
        max_distance = max(distances.values())
        eccentricities[start_vertex] = max_distance

    # Promień grafu to najmniejsza wartość z eccentricity
    radius = min(eccentricities.values())

    # Centrum grafu to wierzchołki o eccentricity równym promieniowi
    center = []
    for vertex in eccentricities:
        if eccentricities[vertex] == radius:
            center.append(vertex)


    return center

#-------------------------------------------------------------------szukanie pkt artykulacyjnych
def find_articulation_points(graph, num_components_original_graph):
    articulation_points = []
    

    for vertex in list(graph.keys()):
        # Usunięcie wierzchołka z grafu
        temp_neighbors = graph.pop(vertex, [])
        for neighbor in temp_neighbors:
            graph[neighbor].remove(vertex)

        # Zliczenie komponentów po usunięciu wierzchołka
        current_components = find_components(graph)
        num_current_components = len(current_components)
        # print(f"ilość komponentów po usunięciu {vertex} wynosi {num_current_components}, a są to komponeny {current_components}")

        # Jeśli liczba komponentów wzrosła, wierzchołek jest punktem artykulacyjnym
        if num_current_components > num_components_original_graph:
            articulation_points.append(vertex)

        # Przywrócenie wierzchołka do grafu
        graph[vertex] = temp_neighbors
        for neighbor in temp_neighbors:
            graph[neighbor].append(vertex)

    return articulation_points


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
            components.append(sorted(order))  # Sortowanie wierzchołków w komponencie
            for v in order:
                visited[v] = True

    return components


#tworzy listę sasiedztwa dla komponentów spójności
def create_component_adj_lists(adj_list):
    '''
    Tworzy listę sąsiedztwa dla każdego komponentu spójności i sortuje wierzchołki oraz ich sąsiadów.

    :param adj_list: Słownik reprezentujący listę sąsiedztwa grafu.
    :return: Lista posortowanych list sąsiedztwa dla każdego komponentu.
    '''
    components = find_components(adj_list)

    # Jeśli jest tylko jeden komponent, zwróć posortowaną listę sąsiedztwa
    if len(components) == 1:
        sorted_adj_list = {node: sorted(adj_list[node]) for node in sorted(adj_list)}
        return [sorted_adj_list]

    # Tworzenie list sąsiedztwa dla każdego komponentu
    component_adj_lists = []
    for component in components:
        component_adj_list = {node: [] for node in component}
        for node in component:
            component_adj_list[node] = sorted([neighbor for neighbor in adj_list[node] if neighbor in component])
        
        # Sortowanie wierzchołków
        sorted_component_adj_list = {node: component_adj_list[node] for node in sorted(component_adj_list)}
        component_adj_lists.append(sorted_component_adj_list)

    return component_adj_lists

# -------------------------------------------------------------szukanie mostów w komponentach

#Funkcja znajdująca mosty w grafie przez usuwanie krawędzi
def find_bridges(graph):
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

# Usuwa mosty z każdego komponentu grafu (jako lista sąsiedztwa).
def remove_bridges_from_components(component_adj_lists):
    '''
    Usuwa mosty z każdego komponentu grafu i tworzy nowe komponenty.

    :param component_adj_lists: Lista list sąsiedztwa dla każdego komponentu.
    :return: Lista list sąsiedztwa po usunięciu mostów.
    '''
    updated_components = []

    for component in component_adj_lists:
        # Znajdź mosty w bieżącym komponencie
        bridges = find_bridges(component)

        # Utwórz nową listę sąsiedztwa bez mostów
        modified_component = {node: [] for node in component}
        for node, neighbors in component.items():
            for neighbor in neighbors:
                if (node, neighbor) not in bridges and (neighbor, node) not in bridges:
                    modified_component[node].append(neighbor)

        # Znajdź komponenty spójności w zmodyfikowanym komponencie
        new_components = create_component_adj_lists(modified_component)
        updated_components.extend(new_components)

    return updated_components


#Formatuje listę komponentów spójności po usunięciu mostów.
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
            # Wierzchołki w komponencie muszą być unikalne i posortowane
            all_components.append(sorted(grouped_nodes))

    # Posortuj komponenty po pierwszym elemencie w każdej grupie
    all_components = sorted(all_components, key=lambda x: x[0])

    # Formatowanie wynikowego stringa
    formatted_components = f"{len(all_components)} KOMPONENTY: "
    formatted_components += ' '.join(
        f"[{' '.join(map(str, component))}]" for component in all_components
    )
    return formatted_components

#Oblicza macierz najkrótszych czasów dojazdów w grafie, korzystając z algorytmu Dijkstry.
def shortest_paths_matrix(adjacency_list_weights):

    vertices = sorted(adjacency_list_weights.keys())
    # print("\nWierzchołki (posortowane rosnąco):", vertices)
    num_vertices = len(vertices)

    # Macierz wynikowa, wypełniona początkowo nieskończonościami
    shortest_paths = [["INF"] * num_vertices for _ in range(num_vertices)]

    # Uruchom Dijkstrę dla każdego wierzchołka jako punktu startowego
    for i in range(num_vertices):
        start_vertex = vertices[i]
        distances = dijkstra(adjacency_list_weights, start_vertex)

        # Wypełnij wiersz `i` w macierzy wynikowej
        for j in range(num_vertices):
            end_vertex = vertices[j]
            if distances[end_vertex] < float("inf"):
                shortest_paths[i][j] = distances[end_vertex]

    return shortest_paths



if __name__ == "__main__":
    
    n, m, edges = get_data()
    # print(f"liczba dzielnic/węzłów komunikacyjnychi (ilość vertex){n}")
    # print(f"liczba bezpośrednich połączeń (ilość krawędzi) {m}")
    # print(f"Krawędzie z wagami {edges}")

    #-----------------------------------------------------------------------------wyznaczanie MST
    heapSort(edges, compare_edges)
    # print(f"posortowane krawędzie {edges}")

    minSpinalTree, total_weight = kruskal(edges, n)

    # Wyświetlenie minimalnego drzewa spinającego
    print("SIEĆ PODSTAWOWA (MST):")
    total_cost = 0
    for edge in minSpinalTree:
        print(f"{edge['a']}-{edge['b']}: {edge['w']}")
        total_cost += edge['w']
    print(f"Łączny czas: {total_cost}")

    #-----------------------------------------------------tworznenie listy sąsiedztwa z wagami (dijsktra)
    adjacency_list_weights = create_adjacency_list_with_weights(n, edges)
    # print("Lista sąsiedztwa z wagami:")
    # print(adjacency_list_weights)
    # --------------------------------------------------------wyznaczanie: średnicy, promienia, peryferium i centrum
    print("\nPARAMETRY SIECI:")
    diameter = graph_diameter_with_dijkstra(adjacency_list_weights)
    print("Średnica:", diameter)
    
    radius = graph_radius(adjacency_list_weights)
    print("Promień:", radius)

    center = graph_center(adjacency_list_weights)
    print("Centrum:", center)

    periphery = find_periphery(adjacency_list_weights, diameter)
    print("Peryferium:", periphery)

    #-----------------------------------------------------tworznie macierzy najkrtoszych czasów (korzystam z dijkstra z wagami)
    result_matrix = shortest_paths_matrix(adjacency_list_weights)

    print("\nCZASY PRZEJAZDÓW:")
    for row in result_matrix:
        print(" ".join(map(str, row)))

     #-----------------------------------------------------tworznenie listy sąsiedztwa bez wag (articulation points)
    adj_list = create_adj_list(edges)
    # print("lista sasiedztwa")
    # print(adj_list)

    # Znajdowanie komponentów w oryginalnym grafie
    komponenty = find_components(adj_list)
    num_components_original_graph = len(komponenty)
    # print("liczba kompoentów w oryinalnym grafie :", num_components_original_graph)

    # tylko grafy spójne, wiec ilość komponentów=1
    if num_components_original_graph > 1:
        print("BŁĄD")

    #znajdowanie pkt artykulacji
    articulation_points = find_articulation_points(adj_list, num_components_original_graph)
    print("\nPUNKTY KRYTYCZNE:")
    if articulation_points:
        print(" ".join(map(str, articulation_points)))
    else:
        print("BRAK")
    