import math

class Graph:
    def __init__(self, adjacency_list):
        """Inicjalizacja grafu na podstawie listy sąsiedztwa."""
        self.adjacency_list = adjacency_list

    def vertex_count(self):
        """Zwraca liczbę wierzchołków w grafie."""
        return len(self.adjacency_list)
    
    def count_edges(self):
        """Zlicza liczbę krawędzi w grafie."""
        edge_count = sum(len(neighbors) for neighbors in self.adjacency_list)
        return edge_count // 2  # Ponieważ każda krawędź jest liczona dwukrotnie
    
    def get_degrees(self):
        """Zwraca ciąg stopni wierzchołków."""
        return [len(neighbors) for neighbors in self.adjacency_list]
    
    def calculate_average_degree(self):
        """Oblicza średni stopień grafu."""
        total_degrees = sum(self.get_degrees())
        vertex_count = self.vertex_count()
        return total_degrees / vertex_count if vertex_count > 0 else 0

    def is_cycle(self):
        """Sprawdza, czy graf jest cyklem."""
        edge_count = self.count_edges()
        degrees = self.get_degrees()
        vertex_count = self.vertex_count()
        
        if vertex_count != edge_count:  # Liczba krawędzi powinna być równa liczbie wierzchołków
            return False
        
        if all(degree == 2 for degree in degrees):  # Każdy wierzchołek musi mieć stopień 2
            return True
        
        return False

    def is_completed(self):
        """Sprawdza, czy graf jest pełny."""
        degrees = self.get_degrees()
        vertex_count = self.vertex_count()
        return all(degree == vertex_count - 1 for degree in degrees)
    
    def is_path(self):
        """Sprawdza, czy graf jest ścieżką."""
        degrees = self.get_degrees()
        vertex_count = self.vertex_count()
        degree_1_count = degrees.count(1)
        degree_2_count = degrees.count(2)
        
        return degree_1_count == 2 and degree_2_count == vertex_count - 2

    def is_tree(self):
        """Sprawdza, czy graf jest drzewem."""
        edge_count = self.count_edges()
        degrees = self.get_degrees()
        vertex_count = self.vertex_count()
        
        # Liczba krawędzi powinna wynosić liczba wierzchołków - 1 i graf nie może być cyklem
        if edge_count == vertex_count - 1 and not self.is_cycle():
            return all(degree > 0 for degree in degrees)  # Brak wierzchołków izolowanych
        return False
    
    def is_hypercube(self):
        """Sprawdza, czy graf jest hiperkostką."""
        degrees = self.get_degrees()
        vertex_count = self.vertex_count()
        
        # Liczba wierzchołków musi być potęgą liczby 2 (2^n)
        if vertex_count == 0 or not (math.log2(vertex_count)).is_integer():
            return False
        
        # Każdy wierzchołek musi mieć stopień równy log2(vertex_count)
        dimension = int(math.log2(vertex_count))
        return all(degree == dimension for degree in degrees)


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


# Wczytanie grafu
graph = read_graph()

# Obliczanie cech grafu
vertex_count = graph.vertex_count()
edge_count = graph.count_edges()
degrees = graph.get_degrees()
average_degree = graph.calculate_average_degree()

# Wyświetlenie podstawowych informacji o grafie
print(f"Ilość wierzchołków: {vertex_count}")
print(f"Ilość krawędzi: {edge_count}")
print("Stopnie wierzchołków:", ' '.join(map(str, degrees)))
print(f"Średni stopień: {average_degree:.2f}")

# Sprawdzanie klasy grafu
if graph.is_completed():
    print("Jest to graf pełny")
elif graph.is_cycle():
    print("Jest to cykl")
elif graph.is_path():
    print("Jest to ścieżka")
elif graph.is_tree():
    print("Jest to drzewo")
elif graph.is_hypercube():
    print("Jest to hiperkostka")
else:
    print("Graf nie należy do żadnej z podstawowych klas")
