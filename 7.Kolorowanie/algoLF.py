# Napisz program, który dla grafu podanego jako lista sąsiedztwa, wypisze kolorowanie wierzchołków przeprowadzone za pomocą algorytmu LF (largest first). Ponadto program ma wypisać liczbę chromatyczną otrzymaną w wyniku tego pokolorowania.

# Zakładamy, że wybieramy niepokolorowany wierzchołek o najwyższym stopniu i najwyższym labelu. Oznacza to, że jeśli wierzchołek 2 ma stopień 4 oraz wierzchołek 3 ma stopień 4 to wybieramy najpierw wierzchołek 3.

# Natomiast podczas przeszukiwania sąsiadów zaczynamy zawsze od sąsiada z najmniejszym labelem.
import heapq

def read_adjacency_list():
    # print("Wprowadź graf jako listę sąsiedztwa")
    adjacency_list = {}

    try:
        while True:
            line = input()
            data = list(map(int, line.split()))
            if len(data) > 1:
                adjacency_list[data[0]] = data[1:]
    except EOFError:
        pass

    return adjacency_list

# Funkcja uporządkowuje wierzchołki grafu nierosnąco według stopni.
def sort_vertices_by_degree2(adjacency_list):
    # Utwórz kopiec jako listę krotek (stopień, wierzchołek)
    heap = [(len(neighbors), vertex) for vertex, neighbors in adjacency_list.items()]

    # Przekształć listę w kopiec
    heapq.heapify(heap)

    # Wyciągnij wierzchołki z kopca w kolejności rosnącej i odwróć
    sorted_vertices = []
    while heap:
        degree, vertex = heapq.heappop(heap)
        sorted_vertices.append((degree, vertex))

    # Odwróć kolejność, aby uzyskać malejący porządek stopni
    sorted_vertices.reverse()

    # Zwróć tylko wierzchołki
    return [vertex for _, vertex in sorted_vertices]


def sort_vertices_by_degree(adjacency_list):
    # Utwórz kopiec jako listę krotek (stopień, wierzchołek)
    heap = [(len(neighbors), vertex) for vertex, neighbors in adjacency_list.items()]

    # Przekształć listę w kopiec
    heapq.heapify(heap)

    # Wyciągnij wierzchołki z kopca w kolejności rosnącej i odwróć
    sorted_vertices = []
    while heap:
        degree, vertex = heapq.heappop(heap)
        sorted_vertices.append((vertex, degree))

    # Odwróć kolejność, aby uzyskać malejący porządek stopni
    sorted_vertices.reverse()

    # Zwróć słownik w formacie {wierzchołek: stopień}
    return {vertex: degree for vertex, degree in sorted_vertices}

# Iteracyjne przeszukiwanie grafu w głąb (DFS)
def dfs_iter(adj_list, start):

    visited = {node: False for node in adj_list}  
    stack = [start] 
    order = [] 

    while stack:
        node = stack.pop()  
        if not visited[node]:
            visited[node] = True  
            order.append(node) 

            # Dodaj sąsiadów na stos w kolejności odwrotnej, aby odwiedzać je w porządku rosnącym
            for neighbor in sorted(adj_list[node], reverse=True):
                if not visited[neighbor]:
                    stack.append(neighbor)

    return order, visited

# Zliczanie kolorów potrzebnych do pokolorowania wierzchołków. return: Słownik z kolorowaniem wierzchołków i liczba chromatyczna.
def largest_first_coloring(adjacency_list, sorted_vertices):
    coloring = {}

    # Pokolorowanie wierzchołków zaczynjąc od  wierzchołka o najwyższym stopniu i najwyższym labelu na podstawie listy sorted_vertices.
    for vertex in sorted_vertices:
        # print(f"Przetwarzanie wierzchołka: {vertex}")
        # Zebranie kolory sąsiadów 
        neighbor_colors = set()

        # podczas przeszukiwania sąsiadów zaczynamy zawsze od sąsiada z najmniejszym labelem.
        start_vertex = min(adjacency_list.keys())
        # print(f"Startowy wierzchołek dla DFS: {start_vertex}")
        neighbors_dfs_order, _ = dfs_iter(adjacency_list, start_vertex)
        for neighbor in neighbors_dfs_order:
            if neighbor in adjacency_list[vertex] and neighbor in coloring:
                neighbor_colors.add(coloring[neighbor])
        
        # print(f"Kolory sąsiadów dla wierzchołka {vertex}: {neighbor_colors}")

        # Znajdź najmniejszy dostępny kolor zaczynając od 1
        color = 1
        while color in neighbor_colors:
            color += 1

        coloring[vertex] = color
        print(f"Przypisany kolor dla wierzchołka {vertex}: {color}")
    
    # Posortuj wyniki kolorowania według wierzchołków rosnąco (metoda dla początkujących)
    sorted_coloring = {}
    for vertex in sorted(coloring.keys()):
        sorted_coloring[vertex] = coloring[vertex]
    
    # Liczba chromatyczna to maksymalny użyty kolor
    chromatic_number = max(coloring.values()) if coloring else 0

    return sorted_coloring, chromatic_number



if __name__ == "__main__":
    adjacency_list = read_adjacency_list()
    print("Lista sąsiedztwa grafu:", adjacency_list)

    sorted_vertices = sort_vertices_by_degree(adjacency_list)
    print("Wierzchołki posortowane według stopnia:", sorted_vertices)

    start_vertex=1
    # Wykonaj DFS od tego wierzchołka
    dfs_order, _ = dfs_iter(adjacency_list, start_vertex)
    print(f"Kolejność DFS: {dfs_order}")
    
    
    coloring, chromatic_number = largest_first_coloring(adjacency_list, sorted_vertices)
    print("Kolorowanie wierzchołków jako słownik:", coloring)
    print("Pokolorowanie wierzchołków:", " ".join(map(str, coloring.values())))
    print(f"Liczba chromatyczna == {chromatic_number}")
