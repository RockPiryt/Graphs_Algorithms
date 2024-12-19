
'''Aby sprawdzić, czy istnieje ścieżka między dwoma wierzchołkami 
a i  d w grafie, można zastosować przeszukiwanie grafu w głąb (DFS)'''

import sys

def read_graph_and_vertex():
    """Funkcja wczytująca graf jako lista sąsiedztwa oraz wierzchołek startowy."""
    try:
        input_data = sys.stdin.read().strip()
        if not input_data:
            return None, None, True

        lines = input_data.split('\n')
        if len(lines) < 2:
            return None, None, True

        graph = []
        for line in lines[:-1]:
            if line.strip():
                try:
                    neighbors = list(map(int, line.split()))
                    if not all(n > 0 for n in neighbors):
                        return None, None, True
                    graph.append(neighbors)
                except ValueError:
                    return None, None, True
            else:
                graph.append([])

        start_vertex = lines[-1].strip()
        if not start_vertex.isdigit():
            return None, None, True

        start_vertex = int(start_vertex)
        if start_vertex < 1 or start_vertex > len(graph):
            return None, None, True

        return graph, start_vertex - 1, False  # Zwróć graf, indeks startowy (0-based) i brak błędu
    except Exception:
        return None, None, True


class Graph:
    def __init__(self, adjacency_list):
        """Inicjalizacja grafu na podstawie listy sąsiedztwa."""
        self.adjacency_list = adjacency_list

    
    def getNeighbours(self, vertex_index):
        """Zwraca sąsiadów wybranego wierzchołka na podstawie numeru wprowadzonego przez użytkownika."""
        try:
            
            # Pobranie listy sąsiadów
            neighbors = self.adjacency_list[vertex_index][1:]
            
            # # Wyświetlenie sąsiadów (jeśli istnieją)
            # if neighbors:
            #     print(f"Sąsiedzi wierzchołka {vertex_index + 1} to    -----: {', '.join(map(str, neighbors))}")
            # else:
            #     print(f"Wierzchołek {vertex_index + 1} nie ma sąsiadów.")
            
            return neighbors

        except IndexError:
            print("BŁĄD: Nie można znaleźć sąsiadów dla podanego wierzchołka.")
            exit(1)

    def vertex_count(self):
        """Zwraca liczbę wierzchołków w grafie."""
        return len(self.adjacency_list)
    
    def count_edges(self):
        """Zlicza liczbę krawędzi w grafie."""
        edge_count = 0  
    
        for neighbors in self.adjacency_list:
            edge_count += len(neighbors) - 1  # Odejmujemy 1, aby pominąć numer wierzchołka
        
        return edge_count // 2  
    
    def get_degrees(self):
        '''Funkcja zwracająca ciąg stopni wierzchołków'''
        degrees = []
        for neighbors in self.adjacency_list:
            degrees.append(len(neighbors) - 1)  # Odejmujemy 1, aby pominąć numer wierzchołka
        return degrees
    
    def dfs_iter(self, start):
        """Przeszukiwanie grafu w głąb (DFS) w iteracyjnej wersji."""

        n = len(self.adjacency_list)
        visited = [False] * n  # Wszystkie wierzchołki oznaczamy jako nieodwiedzone
        stack = [start]  # Stos zaczyna się od wierzchołka startowego (0-based)
        order = []  # Kolejność odwiedzania wierzchołków

        while stack:
            # Pobieramy wierzchołek ze stosu
            node = stack.pop()
            node_neighbors = self.getNeighbours(node)
            if not visited[node]:  # Jeśli wierzchołek jeszcze nie został odwiedzony
                visited[node] = True  # Oznacz jako odwiedzony
                order.append(node + 1)  # Dodajemy do porządku, ale jako 1-based

                # Dodaj sąsiadów do stosu w odwrotnej kolejności
                reversed_neighbors = sorted(node_neighbors, reverse=True)
                updated_neighbors = [neighbor - 1 for neighbor in reversed_neighbors] #odjęcie od każdego 1, zeby indexy sie zgadzaly
                for neighbor in updated_neighbors:
                    if not visited[neighbor]:
                        stack.append(neighbor)

        return order, visited
# Wczytaj graf i wierzchołek początkowy
graph, start_vertex, error_flag = read_graph_and_vertex()

if error_flag:
    print(f"BŁĄD")
else:
    graph = Graph(graph)
    # Wykonanie DFS
    order, visited = graph.dfs_iter(start_vertex)

    # Sprawdzenie spójności grafu — jeśli po wykonaniu DFS wszystkie wierzchołki są odwiedzone, graf jest spójny.
    is_connected = True  

    for v in visited:
        if not v:  # Jeśli false na liście visited
            is_connected = False
            break  

    if is_connected:
        print("Porządek DFS:", " ".join(map(str, order)))
        print("Graf jest spójny")
    else:
        print("Graf jest niespójny")


