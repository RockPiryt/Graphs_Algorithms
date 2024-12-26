import sys
import math

def read_graph():
    """Funkcja wczytująca graf jako macierz sąsiedztwa z wagami."""
    try:
        input_data = sys.stdin.read().strip()
        if not input_data:
            return None, True

        lines = input_data.split('\n')
        if len(lines) < 1:
            return None, True

        graph = []
        for line in lines:
            if line.strip():
                try:
                    weights = list(map(int, line.split()))
                    if not all(weight >= 0 for weight in weights):  # Sprawdzamy, czy wagi są nieujemne
                        return None, True
                    graph.append(weights)
                except ValueError:
                    return None, True

        n = len(graph)
        for row in graph:
            if len(row) != n:  # Sprawdzamy, czy macierz jest kwadratowa
                return None, True

        return graph, False
    except Exception:
        return None, True

def floyd_warshall(graph):
    """Funkcja obliczająca najkrótsze ścieżki między wszystkimi parami wierzchołków."""
    n = len(graph)
    dist = [[math.inf] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                dist[i][j] = 0
            elif graph[i][j] > 0:
                dist[i][j] = graph[i][j]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist

def graph_diameter(graph):
    """Funkcja obliczająca średnicę grafu."""
    dist = floyd_warshall(graph)
    n = len(graph)

    diameter = 0
    for i in range(n):
        for j in range(n):
            if dist[i][j] != math.inf:
                diameter = max(diameter, dist[i][j])

    return diameter

if __name__ == "__main__":
    graph, error = read_graph()
    if error or graph is None:
        print("Błąd danych wejściowych")
    else:
        diameter = graph_diameter(graph)
        print("Średnica grafu:", diameter)
