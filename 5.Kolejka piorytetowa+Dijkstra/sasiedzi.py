def traverse_neighbors(graph):
    """
    Funkcja przechodzi po wszystkich sąsiadach każdego wierzchołka w grafie
    i wypisuje ich informacje.

    :param graph: 2D lista reprezentująca ważoną macierz sąsiedztwa grafu
    """
    num_vertices = len(graph)
    
    for vertex in range(num_vertices):
        print(f"Wierzchołek {vertex} ma sąsiadów:")
        for neighbor in range(num_vertices):
            weight = graph[vertex][neighbor]
            if weight > 0:  # Sprawdzamy, czy istnieje krawędź
                print(f"  Sąsiad: {neighbor}, Waga krawędzi: {weight}")
        print()

if __name__ == "__main__":
    # Przykładowa macierz sąsiedztwa
    graph = [
        [0, 0, 0, 7],
        [0, 0, 3, 0],
        [0, 3, 0, 7],
        [7, 0, 7, 0]
    ]

    # Przechodzimy po sąsiadach każdego wierzchołka
    traverse_neighbors(graph)
