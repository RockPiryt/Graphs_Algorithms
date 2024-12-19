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

def getNeighbours(graph, vertex_index):
    """Zwraca sąsiadów wybranego wierzchołka na podstawie numeru wprowadzonego przez użytkownika."""
    try:
        
        # Pobranie listy sąsiadów
        neighbors = graph[vertex_index][1:]
        
        # Wyświetlenie sąsiadów (jeśli istnieją)
        if neighbors:
            print(f"Sąsiedzi wierzchołka {vertex_index + 1}: {', '.join(map(str, neighbors))}")
        else:
            print(f"Wierzchołek {vertex_index + 1} nie ma sąsiadów.")
        
        return neighbors

    except IndexError:
        print("BŁĄD: Nie można znaleźć sąsiadów dla podanego wierzchołka.")
        exit(1)



class Graph:
    def __init__(self, adjacency_list):
        """Inicjalizacja grafu na podstawie listy sąsiedztwa."""
        self.adjacency_list = adjacency_list

    def display_graph(self):
        """Wyświetla listę sąsiedztwa grafu."""
        print("Lista sąsiedztwa grafu:")
        vertex_number = 1  # Numerujemy wierzchołki od 1
        for neighbors in self.adjacency_list:
            neighbors_str = ", ".join(map(str, neighbors))
            print(f"Wierzchołek {vertex_number}: {neighbors_str}")
            vertex_number += 1
    
    def getNeighbours(self, vertex_index):
        """Zwraca sąsiadów wybranego wierzchołka na podstawie numeru wprowadzonego przez użytkownika."""
        try:
            
            # Pobranie listy sąsiadów
            neighbors = self.adjacency_list[vertex_index][1:]
            
            # Wyświetlenie sąsiadów (jeśli istnieją)
            if neighbors:
                print(f"Sąsiedzi wierzchołka {vertex_index + 1} to    -----: {', '.join(map(str, neighbors))}")
            else:
                print(f"Wierzchołek {vertex_index + 1} nie ma sąsiadów.")
            
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
    
    def calculate_average_degree(self):
        """Oblicza średni stopień grafu."""
        total_degrees = sum(self.get_degrees())
        vertex_count = self.vertex_count()
        return total_degrees / vertex_count if vertex_count > 0 else 0
    
    def calculate_average_degree(self):
        '''funckja licząca średni stopień grafu'''
        total_degrees = sum(self.get_degrees())
        vertex_count = self.vertex_count()
        average_degree = total_degrees / vertex_count
        return average_degree
    
    def is_cycle(self):
        """Sprawdza, czy graf jest cyklem."""
        edge_count = self.count_edges()
        degrees = self.get_degrees()
        vertex_count = self.vertex_count()
        # m = n (ilośc krawędzi musi być równa ilości wierzchołków)
        if vertex_count != edge_count:  
            return False
    
         # każdy wierzchołek 2 stopnia
        for degree in degrees:
            if degree != 2:
                return False  
        return True 

    
    def is_completed(self):
        """Sprawdza, czy graf jest pełny."""
        degrees = self.get_degrees()
        vertex_count = self.vertex_count()
        edge_count = self.count_edges()
        
        # Warunek: stopień każdego wierzchołka musi być równy n-1
        for degree in degrees:
            if degree != vertex_count - 1:
                return False
        
        # Warunek: liczba krawędzi musi być równa n(n-1)/2
        expected_edges = vertex_count * (vertex_count - 1) // 2
        if edge_count != expected_edges:
            return False
        
        return True 
    
    def is_path(self):
        '''funkcja sprawdzająca czy graf jest ścieżka'''
        degrees = self.get_degrees()
        vertex_count = self.vertex_count()
        
        # flagi 
        degree_1_count = 0
        degree_2_count = 0
        
        # Iterujemy przez stopnie wierzchołków i zliczamy wierzchołki o stopniu 1 i 2
        for degree in degrees:
            if degree == 1:
                degree_1_count += 1
            elif degree == 2:
                degree_2_count += 1
        
        # dwa wierzchołki na krańcach maja 1,reszta stopnia 2
        if degree_1_count == 2 and degree_2_count == vertex_count - 2:
            return True
        else:
            return False

    def is_tree(self):
        '''funkcja sprawdzająca czy graf jest drzewem'''
        edge_count = self.count_edges()
        degrees = self.get_degrees()
        vertex_count = self.vertex_count()
        
        #m=n-1 oraz niecykliczny, brak wierzchołków izolowanych
        if edge_count == vertex_count - 1 and not self.is_cycle():
            for degree in degrees:
                if degree == 0:  
                    return False
            return True
        return False
    
    def is_hypercube(self):
        '''funkcja sprawdzająca czy graf jest hiperkostka'''
        degrees = self.get_degrees()
        vertex_count = self.vertex_count()
    
        # Liczba wierzchołków musi być potęgą liczby 2 (2^n)
        if vertex_count == 0 or not (math.log2(vertex_count)).is_integer():
            return False
        
        # Obliczamy wymiar hiperkostki: n = log2(vertex_count)
        dimension = int(math.log2(vertex_count))
        
        # Sprawdzamy, czy każdy wierzchołek ma dokładnie 'dimension' sąsiadów
        for degree in degrees:
            if degree != dimension:
                return False
        
        return True

    
    def dfs_iter(self, start):
        """Przeszukiwanie grafu w głąb (DFS) w iteracyjnej wersji."""

        n = len(self.adjacency_list)
        visited = [False] * n  # Wszystkie wierzchołki oznaczamy jako nieodwiedzone
        print(f"visited: {visited}")
        stack = [start]  # Stos zaczyna się od wierzchołka startowego (0-based)
        print(f"start:{start}")
        order = []  # Kolejność odwiedzania wierzchołków

        print("\nDFS:")

        while stack:
            # Pobieramy wierzchołek ze stosu
            node = stack.pop()
            print(f"aktualny analizowany wierzcholek: {node}")
            node_neighbors = self.getNeighbours(node)
            print(f"sasiedzi analizowanego wierzcholka: {node_neighbors}")
            if not visited[node]:  # Jeśli wierzchołek jeszcze nie został odwiedzony
                visited[node] = True  # Oznacz jako odwiedzony
                print(f"visited: {visited}")
                order.append(node + 1)  # Dodajemy do porządku, ale jako 1-based
                print(node + 1, end=" ")  # Wypisujemy jako 1-based
                print(f"order: {order}")

                # Dodaj sąsiadów do stosu w odwrotnej kolejności
                reversed_neighbors = sorted(node_neighbors, reverse=True)
                print(f"reversed_neighbors: {reversed_neighbors}")
                updated_neighbors = [neighbor - 1 for neighbor in reversed_neighbors]
                print(f"updated_neighbors: {updated_neighbors}")
                for neighbor in updated_neighbors:
                    print(f"neighbor: {neighbor}")
                    neighbor_index = neighbor   # Przechodzimy na 0-based
                    if not visited[neighbor_index]:
                        stack.append(neighbor_index)

        return order, visited




if __name__ == "__main__":
    graph = read_graph()  
    start_vertex = read_vertex(graph)  # Wczytanie numeru startowego wierzchołka
    graph = Graph(graph) 

    # Wykonanie DFS
    order, visited = graph.dfs_iter(start_vertex)
    
    print("Porządek DFS:", " ".join(map(str, order)))
    print(f"visited: {visited}")

    # Sprawdzenie spójności grafu — jeśli po wykonaniu DFS wszystkie wierzchołki są odwiedzone, graf jest spójny.
    is_connected = True  

    for v in visited:
        if not v:  # Jeśli false na liście visited
            is_connected = False
            break  

    if is_connected:
        print("Graf jest spójny.")
    else:
        print("Graf nie jest spójny.")


