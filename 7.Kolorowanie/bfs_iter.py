def bfs_iter(adj_list, start):
    """
    Wykonaj iteracyjne przeszukiwanie wszerz (BFS) w grafie bez użycia deque.
    
    :param adj_list: Słownik reprezentujący listę sąsiedztwa {wierzchołek: [sąsiedzi]}.
    :param start: Wierzchołek początkowy.
    :return: Lista odwiedzonych wierzchołków w kolejności odwiedzania oraz odwiedzone wierzchołki.
    """
    visited = {node: False for node in adj_list}  # Inicjalizacja odwiedzonych wierzchołków
    queue = [start]  # Zwykła lista używana jako kolejka
    order = []  # Kolejność odwiedzonych wierzchołków

    visited[start] = True  # Oznacz wierzchołek startowy jako odwiedzony

    while queue:
        node = queue.pop(0)  # Pobierz pierwszy element z kolejki (powolniejsze niż deque)
        order.append(node)  # Dodaj wierzchołek do kolejności

        for neighbor in sorted(adj_list[node]):  # Przeszukuj sąsiadów w kolejności rosnącej
            if not visited[neighbor]:
                visited[neighbor] = True  # Oznacz sąsiada jako odwiedzonego
                queue.append(neighbor)  # Dodaj sąsiada na koniec kolejki

    return order, visited

# Przykład użycia
if __name__ == "__main__":
    adjacency_list = {
        1: [2, 3],
        2: [1, 4],
        3: [1, 4, 5],
        4: [2, 3],
        5: [3]
    }

    start_vertex = 1
    bfs_order, visited_nodes = bfs_iter(adjacency_list, start_vertex)
    print("Kolejność odwiedzonych wierzchołków:", bfs_order)
    print("Odwiedzone wierzchołki:", visited_nodes)
 