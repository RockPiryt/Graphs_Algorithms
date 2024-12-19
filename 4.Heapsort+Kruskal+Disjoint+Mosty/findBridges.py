def isConnected(graph, n, start, excluded_edge):
    """
    Sprawdza, czy graf pozostaje spójny po usunięciu krawędzi.
    
    :param graph: Lista sąsiedztwa reprezentująca graf (wierzchołek, sąsiad, waga).
    :param n: Liczba wierzchołków.
    :param start: Wierzchołek początkowy.
    :param excluded_edge: Krawędź, która ma zostać usunięta z grafu (w postaci krotki (v, u)).
    :return: True, jeśli graf pozostaje spójny, w przeciwnym razie False.
    """
    visited = [False] * n

    # Używamy funkcji dfs_iter zamiast rekurencyjnej wersji DFS
    def dfs_iter(graph, start):
        n = len(graph)  # Liczba wierzchołków
        visited = [False] * n  # Wszystkie wierzchołki oznaczamy jako nieodwiedzone
        stack = [start]  # Stos zaczyna się od wierzchołka startowego
        order = []  # Kolejność odwiedzania wierzchołków

        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                order.append(node)

                # Przeglądamy sąsiadów wierzchołka
                for neighbor, _ in graph[node]:
                    # Ignorujemy krawędź do usunięcia
                    if (node, neighbor) != excluded_edge and (neighbor, node) != excluded_edge:
                        if not visited[neighbor]:
                            stack.append(neighbor)

        return visited

    # Wykonaj DFS zaczynając od wierzchołka startowego
    visited = dfs_iter(graph, start)

    # Zwracamy True, jeśli wszystkie wierzchołki są odwiedzone (graf jest spójny)
    return all(visited)

def findBridges(graph, n):
    """
    Funkcja do znajdowania mostów w grafie.

    :param graph: Lista sąsiedztwa reprezentująca graf (wierzchołek, sąsiad, waga).
    :param n: Liczba wierzchołków.
    :return: Lista mostów w postaci krotek (v, u).
    """
    bridges = []

    # Iterujemy po każdej krawędzi w grafie
    for v in range(n):
        for u, _ in graph[v]:  # Ignorujemy wagę krawędzi
            if v < u:  # Sprawdzamy każdą krawędź tylko raz
                if not isConnected(graph, n, v, (v, u)):  # Sprawdzamy, czy usunięcie krawędzi powoduje rozdzielenie
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
