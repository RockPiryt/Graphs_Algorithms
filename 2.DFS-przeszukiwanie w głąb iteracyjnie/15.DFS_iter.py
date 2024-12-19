import math

def read_graph():
    '''Funkcja wczytująca graf jako lista sąsiedztwa'''
    graph = []
    try:
        while True:
            line = input().strip()
            if line:
                split_line = line.split()
                neighbors = []
                for x in split_line:
                    try:
                        neighbors.append(int(x))
                    except ValueError:
                        print("BŁĄD")
                        exit(1)
            else:
                neighbors = []
            graph.append(neighbors)
    except EOFError:
        pass
    return graph


def read_vertex(graph):
    """Sprawdza, czy wprowadzony numer jest poprawny (niepusty, nieujemny, mieści się w zakresie grafu)."""
    try:
        input_value = input("Podaj numer wierzchołka startowego: ")
        
        if not input_value: 
            raise ValueError("Wprowadzono pustą wartość.")
        
        s_vertex = int(input_value)  
        
        if s_vertex < 1: 
            raise ValueError("Numer wierzchołka nie może być mniejszy niż 1.")
        
        if s_vertex > len(graph):  
            raise ValueError(f"Numer wierzchołka {s_vertex} wykracza poza zakres grafu (1-{len(graph)}).")
        
        start_point = s_vertex - 1  # Zmiana numeru na indeks listy (od 0)
        return start_point

    except ValueError as e:
        print(f"BŁĄD: {e}")
        exit(1)  


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

graph = read_graph()  
start_vertex = read_vertex(graph)  # Wczytanie numeru startowego wierzchołka
graph = Graph(graph) 

# Wykonanie DFS
order, visited = graph.dfs_iter(start_vertex)

print("Porządek DFS:", " ".join(map(str, order)))
# print(f"visited: {visited}")

# Sprawdzenie spójności grafu — jeśli po wykonaniu DFS wszystkie wierzchołki są odwiedzone, graf jest spójny.
is_connected = True  

for v in visited:
    if not v:  # Jeśli false na liście visited
        is_connected = False
        break  

if is_connected:
    print("Graf jest spójny")
else:
    print("Graf jest niespójny")

