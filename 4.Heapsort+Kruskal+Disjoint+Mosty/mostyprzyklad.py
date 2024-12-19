import sys

def main():
    try:
        input_data = sys.stdin.read().strip().split('\n')

        # Sprawdzamy minimalną liczbę wierszy
        if len(input_data) < 2:
            raise ValueError('BŁADD')

        # Parsowanie pierwszego wiersza z n i m
        n, m = map(int, input_data[0].split())
        if n < 2 or n > 100 or m < n - 1 or m > (n * (n - 1)) // 2:
            raise ValueError('BŁĄD')

        # Odczytanie krawędzi
        edges = []
        for i in range(1, m + 1):
            a, b, w = map(int, input_data[i].split())
            if not (1 <= a <= n and 1 <= b <= n and 1 <= w <= 1000000):
                raise ValueError('BŁĄD')
            if a > b:
                a, b = b, a
            edges.append((a, b, w))

        # Algorytm Kruskala
        mst = kruskal(edges, n)

        # Wyświetlanie minimalnego drzewa spinającego
        print('MINIMALNE DRZEWO SPINAJĄCE:')
        total_cost = 0
        for edge in mst:
            print(f"{edge[0]} {edge[1]} {edge[2]}")
            total_cost += edge[2]
        print(f'Łączny koszt: {total_cost}')

        # Budowanie grafu z krawędzi
        graph = build_graph(edges, n)

        # Wyszukiwanie mostów
        bridges = find_bridges(graph, n)

        # Wyświetlanie mostów
        print('\nMOSTY:')
        if not bridges:
            print('BRAK MOSTÓW')
        else:
            for bridge in bridges:
                print(f"{bridge[0]} {bridge[1]}")

        # Usuwanie mostów z grafu
        for bridge in bridges:
            remove_edge(graph, bridge[0], bridge[1])

        # Wyszukiwanie komponentów
        components = find_components(graph, n)

        # Wyświetlanie komponentów
        print('\nKOMPONENTY:')
        for comp in components:
            print(f"[{' '.join(map(str, comp))}]")

    except Exception:
        print('BŁĄD')

# Algorytm Kruskala
def kruskal(edges, n):
    edges = sort_edges(edges)  # Użycie własnej funkcji sortowania
    parent = list(range(n + 1))
    mst = []

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        parent[root_y] = root_x

    for a, b, w in edges:
        if find(a) != find(b):
            mst.append((a, b, w))
            union(a, b)
        if len(mst) == n - 1:
            break

    return mst

# Własna funkcja sortowania krawędzi
def sort_edges(edges):
    for i in range(len(edges)):
        for j in range(len(edges) - 1):
            if compare_edges(edges[j], edges[j + 1]) > 0:
                edges[j], edges[j + 1] = edges[j + 1], edges[j]
    return edges

# Funkcja porównująca krawędzie
def compare_edges(edge1, edge2):
    if edge1[2] != edge2[2]:
        return edge1[2] - edge2[2]
    if edge1[0] != edge2[0]:
        return edge1[0] - edge2[0]
    return edge1[1] - edge2[1]

# Budowanie grafu
def build_graph(edges, n):
    graph = {i: [] for i in range(1, n + 1)}
    for a, b, w in edges:
        graph[a].append((b, w))
        graph[b].append((a, w))
    return graph

# Wyszukiwanie mostów
def find_bridges(graph, n):
    time = 0
    visited = [False] * (n + 1)
    disc = [0] * (n + 1)
    low = [0] * (n + 1)
    parent = [-1] * (n + 1)
    bridges = []

    def dfs(u):
        nonlocal time
        visited[u] = True
        disc[u] = low[u] = time
        time += 1

        neighbors = sorted(graph[u])  # Sortowanie sąsiadów
        for v, _ in neighbors:
            if not visited[v]:
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append((min(u, v), max(u, v)))
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i)

    return sorted(bridges, key=lambda x: (x[0], x[1]))

# Usuwanie krawędzi z grafu
def remove_edge(graph, u, v):
    graph[u] = [edge for edge in graph[u] if edge[0] != v]
    graph[v] = [edge for edge in graph[v] if edge[0] != u]

# Wyszukiwanie komponentów spójności
def find_components(graph, n):
    visited = [False] * (n + 1)
    components = []

    def dfs(u, comp):
        visited[u] = True
        comp.append(u)
        for v, _ in graph[u]:
            if not visited[v]:
                dfs(v, comp)

    for i in range(1, n + 1):
        if not visited[i]:
            comp = []
            dfs(i, comp)
            components.append(sorted(comp))

    return components

if __name__ == '__main__':
    main()
