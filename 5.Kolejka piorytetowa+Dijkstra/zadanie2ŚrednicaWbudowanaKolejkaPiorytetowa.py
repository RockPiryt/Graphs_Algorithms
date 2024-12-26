import heapq
import sys

def read_graph():
    input_data = sys.stdin.read().strip()
    if not input_data:
        return None, True

    lines = input_data.split('\n')
    graph = []
    for line in lines:
        if line.strip():
            weights = list(map(int, line.split()))
            if not all(weight >= 0 for weight in weights):
                return None, True
            graph.append(weights)

    n = len(graph)
    for row in graph:
        if len(row) != n:
            return None, True

    return graph, False


def dijkstra(graph, start):
    num_vertex = len(graph)
    distances = [float("inf")] * num_vertex
    distances[start] = 0
    visited = set()
    heap = [(0, start)]

    while heap:
        current_distance, current_vertex = heapq.heappop(heap)

        if current_vertex in visited:
            continue

        visited.add(current_vertex)

        for neighbor, weight in enumerate(graph[current_vertex]):
            if weight > 0 and neighbor not in visited:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(heap, (distance, neighbor))

    return distances


def graph_diameter_with_dijkstra(graph):
    num_vertices = len(graph)
    max_distances = []

    for start_vertex in range(num_vertices):
        distances = dijkstra(graph, start_vertex)
        max_distance = max(distances)
        max_distances.append(max_distance)

    return max(max_distances)


if __name__ == "__main__":
    graph, error = read_graph()
    if error:
        print("BŁĄD")
    else:
        diameter = graph_diameter_with_dijkstra(graph)
        print(diameter)
