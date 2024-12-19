import heapq

def dijkstra(matrix, start):
    n = len(matrix)  # liczba wierzchołków
    distances = [float('inf')] * n  # początkowo wszystkie odległości są nieskończone
    distances[start] = 0  # odległość do wierzchołka początkowego wynosi 0
    priority_queue = [(0, start)]  # kolejka priorytetowa w postaci (dystans, wierzchołek)

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Jeśli aktualny dystans jest większy niż już zapisany, pomijamy
        if current_distance > distances[current_vertex]:
            continue

        # Sprawdzamy sąsiadów
        for neighbor in range(n):
            weight = matrix[current_vertex][neighbor]
            if weight > 0:  # Istnieje krawędź
                distance = current_distance + weight

                # Jeśli znaleziono krótszą ścieżkę do sąsiada
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

    return distances

# Odczyt danych wejściowych
def main():
    matrix = [
        [0, 0, 0, 7],
        [0, 0, 3, 0],
        [0, 3, 0, 7],
        [7, 0, 7, 0]
    ]
    start_vertex = 1  # Wierzchołek początkowy (indeksowanie od 1)

    # Przekształcamy indeks wierzchołka startowego na indeksowanie od 0
    start_index = start_vertex - 1

    # Wywołujemy funkcję Dijkstry
    distances = dijkstra(matrix, start_index)

    # Wyświetlamy wyniki
    for i, distance in enumerate(distances):
        print(f"{i + 1} = {distance}")

if __name__ == "__main__":
    main()
