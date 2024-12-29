
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

#Iteracyjny DFS, który odwiedza wierzchołki i zbiera krawędzie
def dfs_iter_with_edges(adj_list, start):

    visited = {node: False for node in adj_list}
    stack = [start]
    visited_edges = set()  # Zbiór odwiedzonych krawędzi

    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            for neighbor in adj_list[node]:
                edge = tuple(sorted((node, neighbor)))  # Reprezentacja krawędzi w grafie nieskierowanym
                if edge not in visited_edges:
                    visited_edges.add(edge) 
                    stack.append(neighbor)

    return visited_edges

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


# ----------------------------------------------------------------------------------cyklicznosc grafu
def vertex_count(self):
        """Zwraca liczbę wierzchołków w grafie."""
        return len(self.adjacency_list)
    
def count_edges(self):
    """Zlicza liczbę krawędzi w grafie."""
    edge_count = 0  

    for neighbors in self.adjacency_list:
        edge_count += len(neighbors) - 1  # Odejmujemy 1, aby pominąć numer wierzchołka
    
    return edge_count // 2 


def get_degrees(graph_adj_list):
    '''Funkcja zwracająca ciąg stopni wierzchołków'''
    degrees = []
    for neighbors in graph_adj_list:
        degrees.append(len(neighbors) - 1)  # Odejmujemy 1, aby pominąć numer wierzchołka
    return degrees


def find_components(graph):
    """
    Znajduje komponenty spójności grafu.
    :param graph: Lista sąsiedztwa jako słownik.
    :return: Lista komponentów spójności (każdy komponent to lista wierzchołków).
    """
    visited = set()
    components = []

    def dfs(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, component)

    for node in graph.keys():
        if node not in visited:
            component = []
            dfs(node, component)
            components.append(component)

    return components

#sprawdzenie czy półeulorwski , czyli ze zawiera ścieżkę eulera
# -warunek ścieżki- każdy jego wierzchołek za wyjątkiem dwóch musi posiadać parzysty stopień.
# - warunek zaliczenia wszystkich krawędzi z grafu – zbior unikalnych krawędzi bez powtórek
# - graf musi być spojny – tylko 1 komponent spojnosci sprawdzany dfs
def is_semi_eulerian(adjacency_list):

    # Warunek 1: Sprawdź spójność grafu
    components = find_components(adjacency_list)
    num_components = len(components)
    print("Liczba komponentów spójności:", num_components)

    if num_components > 1:
        print("Graf jest niespójny, więc nie jest pół-Eulerowski.")
        return False

    # Warunek 2: Sprawdź, czy dokładnie dwa wierzchołki mają stopień nieparzysty
    odd_degree_vertices = 0
    for vertex, neighbors in adjacency_list.items():
        degree = len(neighbors)
        print(f"stopien dla {vertex} to {degree}")
        if degree % 2 != 0:
            odd_degree_vertices += 1

    print("Liczba wierzchołków o nieparzystym stopniu:", odd_degree_vertices)
    if odd_degree_vertices != 2:
        print("Graf nie spełnia warunku stopni wierzchołków (dokładnie dwa wierzchołki o nieparzystym stopniu).")
        return False

     # Warunek 3: Sprawdź unikalność krawędzi podczas DFS
    for vertex in graph:
        visited_edges = dfs_iter_with_edges(graph, vertex)
        all_edges = set(tuple(sorted((u, v))) for u in graph for v in graph[u])
        if visited_edges == all_edges:
            print(f"Znaleziono unikalną ścieżkę zawierającą wszystkie krawędzie, zaczynając od wierzchołka {vertex}.")
            return True

    print("Nie znaleziono unikalnej ścieżki zawierającej wszystkie krawędzie.")
    return False



if __name__ == "__main__":
    # Sprawdź, czy graf jest pół-Eulerowski
    result = is_semi_eulerian(graph)
    print("Czy graf jest pół-Eulerowski?", result)


if __name__ == "__main__":

        # Pobierz macierz z inputu
        adjacency_matrix = input_adjacency_matrix()

        # Konwertuj na listę sąsiedztwa
        adjacency_list = adjacency_matrix_to_list(adjacency_matrix)

        # Wyświetl listę sąsiedztwa
        print(f"Lista sąsiedztwa: {adjacency_list}")
        # for vertex, neighbors in adjacency_list.items():
        #     print(f"{vertex}: {neighbors}")

        # Znajdowanie komponentów w oryginalnym grafie
        komponenty = find_components(adjacency_list)
        num_components_original_graph = len(komponenty)
        print("liczba kompoentów w oryinalnym grafie :", num_components_original_graph)

        #sprawdzenie spojnosci grafu
        if num_components_original_graph > 1:
            print("Graf jest niespójny")
        else:
                print("Graf jest spójny")

                
        
        result = is_semi_eulerian(adjacency_list)
        print("Czy graf jest pół-Eulerowski?", result)

        
        #sprawdzenie spojnosci grafu
        if num_components_original_graph > 1:
            print("Graf jest niespójny")
        else:
            #sprawdzenie czy nieuelerowski (jest spojny i jest sciezka ale powtarzalne krawedzie)
            if num_components_original_graph == 1:
                print("Graf jest spójny")
                print("Sprawdzam czy jest ścieżka eulera w ktorej są unikalne krawedzie")
            else: 
                if is_semi_eulerian(adjacency_list):
                    print("Graf jest półeulerowski czyli jest ścieżka z unikalnymi krawędziami")

                    
        # Znalezienie i wypisanie mostów
        bridges = find_bridges(adjacency_list)

        if bridges:
            print("Mosty :", bridges)
        else:
            print("BRAK MOSTÓW")

        
        result = is_semi_eulerian(graph)
        print("Czy graf jest pół-Eulerowski?", result)

