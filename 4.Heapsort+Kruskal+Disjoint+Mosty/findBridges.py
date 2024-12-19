def dfs_iter(graph, start):
    """
    Przeszukiwanie grafu w głąb (DFS) w iteracyjnej wersji.

    :param graph: Lista sąsiedztwa reprezentująca graf.
    :param start: Wierzchołek początkowy (1-based).
    :return: Kolejność odwiedzania wierzchołków (1-based) oraz lista odwiedzonych wierzchołków.
    """
    n = len(graph)  # Liczba wierzchołków
    visited = [False] * n  # Wszystkie wierzchołki oznaczamy jako nieodwiedzone
    stack = [start - 1]  # Stos zaczyna się od wierzchołka startowego (0-based)
    order = []  # Kolejność odwiedzania wierzchołków

    while stack:
        # Pobieramy wierzchołek ze stosu
        node = stack.pop()
        node_neighbors = graph[node][1:]  # Pobieramy sąsiadów wierzchołka (pomijamy indeks)
        
        if not visited[node]:  # Jeśli wierzchołek jeszcze nie został odwiedzony
            visited[node] = True  # Oznacz jako odwiedzony
            order.append(node + 1)  # Dodajemy do porządku (1-based)

            # Dodaj sąsiadów do stosu w odwrotnej kolejności
            reversed_neighbors = sorted(node_neighbors, reverse=True)
            updated_neighbors = [neighbor - 1 for neighbor in reversed_neighbors]  # Konwersja na 0-based
            for neighbor in updated_neighbors:
                if not visited[neighbor]:
                    stack.append(neighbor)

    return order, visited


def isConnected(graph, n, start, excluded_edge):
    visited = [False] * n

    def dfs(v):
        visited[v] = True
        for u, _ in graph[v]:  # Ignorujemy wagę krawędzi
            if not visited[u - 1] and (v + 1, u) != excluded_edge and (u, v + 1) != excluded_edge:
                dfs(u - 1)

    dfs(start - 1)
    return all(visited)


def findBridges(graph, n):
    bridges = []

    # Iteracja po wszystkich wierzchołkach
    for v in range(1, n + 1):  # Używamy numeracji 1-based
        for u, _ in graph[v - 1]:  # Ignorujemy wagę krawędzi i przekształcamy na 0-based
            if v < u:  # Sprawdź każdą krawędź tylko raz
                # Wykluczamy krawędź (v, u) i sprawdzamy, czy graf pozostaje spójny
                if not isConnected(graph, n, v, (v, u)):
                    bridges.append((v, u))

    return bridges


# Przykład grafu
graph = {
    0: [(3, 1), (2, 2)],  # Wierzchołek 1 (0-based): sąsiedzi (3, 1) i (2, 2)
    1: [(0, 1), (2, 3), (4, 5)],  # Wierzchołek 2 (1-based): sąsiedzi (0, 1), (2, 3) i (4, 5)
    2: [(0, 2), (1, 3), (3, 3)],  # Wierzchołek 3 (2-based): sąsiedzi (0, 2), (1, 3), (3, 3)
    3: [(2, 3), (1, 2), (4, 4)],  # Wierzchołek 4 (3-based): sąsiedzi (2, 3), (1, 2), (4, 4)
    4: [(3, 4), (1, 5)]   # Wierzchołek 5 (4-based): sąsiedzi (3, 4) i (1, 5)
}

# Zmienna n (liczba wierzchołków)
n = len(graph)

# Znajdowanie mostów
bridges = findBridges(graph, n)

# Wyświetlenie mostów
print("Mosty w grafie:", bridges)
