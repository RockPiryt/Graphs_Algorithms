import sys
# #-----------------------------------------------------------------------------------wczytanie danych
def input_adjacency_matrix():

    print("Wklej macierz sąsiedztwa (wiersze oddzielone Enterem, zakończ Ctrl+Z):")
    adjacency_matrix = []
    
    try:
        while True:
            line = input().strip()  # Wczytaj wiersz i usuń nadmiarowe spacje
            if line:  # Jeśli wiersz nie jest pusty
                row = list(map(int, line.split()))
                if adjacency_matrix and len(row) != len(adjacency_matrix[0]):
                    raise ValueError("Wszystkie wiersze muszą mieć tę samą liczbę elementów.")
                adjacency_matrix.append(row)
    except EOFError:
        pass  # Koniec wprowadzania (Ctrl+Z)
    
    return adjacency_matrix

def adjacency_matrix_to_list(adjacency_matrix):
    adjacency_list = {}

    for i in range(len(adjacency_matrix)):
        adjacency_list[i + 1] = []  # Klucze wierzchołków są 1-indeksowane
        for j in range(len(adjacency_matrix[i])):
            if adjacency_matrix[i][j] == 1:
                adjacency_list[i + 1].append(j + 1)  # Dodaj sąsiadów (też 1-indeksowane)

    return adjacency_list
# #-----------------------------------------------------------------------------------Znajdowanie  komponentów za pomocą dfs
#Iteracyjny DFS, który odwiedza wierzchołki i zbiera krawędzie oraz ścieżkę Eulera.
def dfs_iter_with_edges_and_path(adj_list, start):

    visited = {node: False for node in adj_list}
    visited_edges = set()  
    stack = [(start, None)]  # Stos przechowuje wierzchołki i ich poprzedników
    euler_path = [] 

    while stack:
        node, parent = stack.pop()
        if not visited[node]:
            visited[node] = True
            euler_path.append(node)  # Dodaj wierzchołek do ścieżki
            for neighbor in adj_list[node]:
                edge = tuple(sorted((node, neighbor))) 
                if edge not in visited_edges:
                    visited_edges.add(edge)  
                    stack.append((neighbor, node))

    return visited_edges, euler_path

# dfs - order wierzcholków-dla szukania mostów i komponentów
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
            components.append(sorted(order))  
            for v in order:
                visited[v] = True

    return components

#tworzy listę sasiedztwa dla komponentów spójności
def create_component_adj_lists(adj_list):
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

#---------------------------------------------------------------------Stopnie wierzchołków
# Oblicza ciąg stopni wierzchołków na podstawie listy sąsiedztwa
def calculate_degree_sequence(adjacency_list):
    degree_sequence = []

    for vertex, neighbors in adjacency_list.items():
        degree = len(neighbors)  # Liczba sąsiadów to stopień wierzchołka
        degree_sequence.append(degree)

    # Sortowanie ciągu stopni malejąco
    degree_sequence.sort(reverse=True)

    return degree_sequence

# Sprawdza, czy wszystkie wierzchołki w grafie mają parzysty stopień
def all_vertices_even(degree_sequence):
    for degree in degree_sequence:
        if degree % 2 != 0: 
            return False
    return True
# Sprawdza, czy w ciągu stopni są dokładnie dwa wierzchołki o nieparzystym stopniu, a reszta wierzchołków ma stopień parzysty.
def has_exactly_two_odd_degrees(degree_sequence):
    odd_count = 0  

    for degree in degree_sequence:
        if degree % 2 != 0:  
            odd_count += 1

    return odd_count == 2

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
# ----------------------------------------------------------------------------------Półeuelrowski (ścieżka Eulera)
#sprawdzenie czy półeulorwski , czyli ze zawiera ścieżkę eulera
# -warunek ścieżki- każdy jego wierzchołek za wyjątkiem dwóch musi posiadać parzysty stopień.
# - warunek zaliczenia wszystkich krawędzi z grafu – zbior unikalnych krawędzi bez powtórek
# - graf musi być spojny – tylko 1 komponent spojnosci sprawdzany dfs


#Sprawdza czy jest ścieżka w grafie spójnym, który ma 2 wierzchołki nieparzyste a reszte parzyste
def is_semi_eulerian(adjacency_list):
    # Sprawdzenie unikalności krawędzi podczas DFS
    for vertex in adjacency_list:
        visited_edges, euler_path = dfs_iter_with_edges_and_path(adjacency_list, vertex)
        all_edges = set(tuple(sorted((u, v))) for u in adjacency_list for v in adjacency_list[u])
        if visited_edges == all_edges:
            print(f"Znaleziono unikalną ścieżkę zawierającą wszystkie krawędzie, zaczynając od wierzchołka {vertex}.")
            return True, euler_path

    print("Nie znaleziono unikalnej ścieżki zawierającej wszystkie krawędzie.")
    return False, None


# ------------------------------------------------------------------------------Eulerowski(cykl Eulera)
# - czy jest spojny oraz 
# -Wszystkie wierzchołki muszą mieć parzysty stopień

# Sprawdza czy jest cykl Eulera w grafie spójnym, którego wszystkie wierzchołki mają stopień parzysty
def is_eulerian(adjacency_list):
    cycle = fleury_algorithm(adjacency_list)
    return cycle

#Lista wierzchołków w kolejności cyklu Eulera lub komunikat o braku cyklu
def fleury_algorithm(adjacency_list):
    
    # Skopiuj graf, aby nie modyfikować oryginalnego
    graph_copy = {u: neighbors[:] for u, neighbors in adjacency_list.items()}
    
    # Zacznij od dowolnego wierzchołka
    start = next(iter(graph_copy))
    path = [start]
    current = start
    
    while any(graph_copy.values()):
        # Wybierz krawędź do przejścia
        for neighbor in graph_copy[current]:
            if len(graph_copy[current]) == 1 or not is_bridge(graph_copy, current, neighbor):
                # Usuń krawędź z grafu
                graph_copy[current].remove(neighbor)
                graph_copy[neighbor].remove(current)
                path.append(neighbor)
                current = neighbor
                break
        else:
            return "Nie znaleziono cyklu Eulera."

    return path

def is_bridge(graph, u, v):
    """
    Sprawdza, czy krawędź (u, v) jest mostem.
    :param graph: Lista sąsiedztwa grafu.
    :param u: Początkowy wierzchołek krawędzi.
    :param v: Końcowy wierzchołek krawędzi.
    :return: True, jeśli krawędź (u, v) jest mostem; False w przeciwnym razie.
    """
    # Liczba komponentów przed usunięciem krawędzi
    initial_components = len(find_components(graph))
    
    # Usuń krawędź (u, v)
    graph[u].remove(v)
    graph[v].remove(u)
    
    # Liczba komponentów po usunięciu krawędzi
    new_components = len(find_components(graph))
    
    # Przywróć krawędź (u, v)
    graph[u].append(v)
    graph[v].append(u)
    
    # Krawędź jest mostem, jeśli graf stał się bardziej rozspójny
    return new_components > initial_components


if __name__ == "__main__":

        # Pobierz macierz z inputu
        adjacency_matrix = input_adjacency_matrix()

        # Konwertuj na listę sąsiedztwa
        adjacency_list = adjacency_matrix_to_list(adjacency_matrix)

        # Wyświetl listę sąsiedztwa
        print(f"Lista sąsiedztwa: {adjacency_list} \n")
        # for vertex, neighbors in adjacency_list.items():
        #     print(f"{vertex}: {neighbors}")
        
        #-----------------------------------------------------Sprawdzenie spójności grafu
        print("SPÓJNOŚĆ")
        # Znajdowanie komponentów w oryginalnym grafie 
        komponenty = find_components(adjacency_list)
        num_components_original_graph = len(komponenty)
        print("liczba kompoentów w oryinalnym grafie :", num_components_original_graph)

        if num_components_original_graph > 1:
            print("Graf jest niespójny\n")
        else:
            print("Graf jest spójny\n")

        #----------------------------------------------------Sprawdzenie ciągu stopni w grafie
        print("STOPNIE")
        degree_sequence = calculate_degree_sequence(adjacency_list)
        print(F"Ciąg stopni wierzchołków: {degree_sequence}")


        if all_vertices_even(degree_sequence):
            print("Wszystkie wierzchołki parzyste, sprawdzam czy jest cykl Eulera.\n")
            # is_eulerian()
            pass
        else:
            if has_exactly_two_odd_degrees(degree_sequence):
                print(f"Dwa  wierzchołki nieparzyste, reszta stopnia parzystego, sprawdzam czy jest ścieżka Eulera.\n")
                #is_semi_eulerian(adjacency_list)
                result, euler_path = is_semi_eulerian(adjacency_list)
                print("Czy graf jest pół-Eulerowski?", result)

                if euler_path:
                     print("Ścieżka Eulera:", euler_path)
            else:
                print("Graf Nieeulerowski")



        #------------------------------------------------------Ogólne sprawdzenie
        # #sprawdzenie spojnosci grafu
        # if num_components_original_graph > 1:
        #     print("Graf jest niespójny")
        # else:
        #     #sprawdzenie czy nieuelerowski (jest spojny i jest sciezka ale powtarzalne krawedzie)
        #     if num_components_original_graph == 1:
        #         print("Graf jest spójny")
        #         print("Sprawdzam czy jest ścieżka eulera w ktorej są unikalne krawedzie")
        #     else: 
        #         if is_semi_eulerian(adjacency_list):
        #             print("Graf jest półeulerowski czyli jest ścieżka z unikalnymi krawędziami")


        # Znalezienie i wypisanie mostów
        bridges = find_bridges(adjacency_list)

        if bridges:
            print("Mosty :", bridges)
        else:
            print("BRAK MOSTÓW")


    
# def count_edges(self):
#     """Zlicza liczbę krawędzi w grafie."""
#     edge_count = 0  

#     for neighbors in self.adjacency_list:
#         edge_count += len(neighbors) - 1  # Odejmujemy 1, aby pominąć numer wierzchołka
    
#     return edge_count // 2 