import sys

def main():
    try:
        input_lines = sys.stdin.read().strip().split('\n')

        # Sprawdzenie minimalnej liczby linii
        if len(input_lines) < 4:
            raise ValueError('BŁĄD')

        # Parsowanie pierwszej linii z n, k, m
        n_k_m = list(map(int, input_lines[0].split()))
        if len(n_k_m) != 3:
            raise ValueError('BŁĄD')
        n, k, m = n_k_m

        if not (2 <= n <= 30 and 1 <= k <= 5 and 1 <= m <= 3):
            raise ValueError('BŁĄD')

        # Sprawdzenie liczby linii dla macierzy sąsiedztwa
        if len(input_lines) < n + 3:
            raise ValueError('BŁĄD')

        # Odczytanie macierzy sąsiedztwa
        adjacency_matrix = []
        for i in range(1, n + 1):
            row = list(map(int, input_lines[i].split()))
            if len(row) != n:
                raise ValueError('BŁĄD')
            if any(val not in (0, 1) for val in row):
                raise ValueError('BŁĄD')
            adjacency_matrix.append(row)

        # Odczytanie listy wyjść ewakuacyjnych
        exits = list(map(int, input_lines[n + 1].split()))
        if len(exits) != k:
            raise ValueError('BŁĄD')
        if any(not (1 <= val <= n) for val in exits):
            raise ValueError('BŁĄD')
        # Sortowanie listy wyjść
        quick_sort(exits, 0, len(exits) - 1)

        # Odczytanie listy pomieszczeń zagrożonych
        threats = list(map(int, input_lines[n + 2].split()))
        if len(threats) != m:
            raise ValueError('BŁĄD')
        if any(not (1 <= val <= n) for val in threats):
            raise ValueError('BŁĄD')
        # Sortowanie listy zagrożeń
        quick_sort(threats, 0, len(threats) - 1)

        # Sprawdzenie, czy listy są posortowane rosnąco
        if not is_sorted(exits) or not is_sorted(threats):
            raise ValueError('BŁĄD')

        # Przechowywanie wyników dla każdego zagrożonego pomieszczenia
        status = 'BEZPIECZNY'
        paths = []
        for threat in threats:
            result = dfs(adjacency_matrix, threat, exits)
            if result['found']:
                paths.append(result['path'])
            else:
                paths.append(f'BRAK DROGI Z POMIESZCZENIA {threat}')
                status = 'NIEBEZPIECZNY'

        print(status)
        for path in paths:
            if isinstance(path, list):
                print(' '.join(map(str, path)))
            else:
                print(path)

        # Jeśli status BEZPIECZNY, wykonujemy pełny DFS
        if status == 'BEZPIECZNY':
            full_traversal = full_dfs(adjacency_matrix, threats[0])
            print(' '.join(map(str, full_traversal)))

    except Exception:
        print('BŁĄD')

# Implementacja QuickSort z wyborem pivota jako elementu środkowego, stabilna
def quick_sort(arr, left, right):
    if left >= right:
        return
    pivot_index = (left + right) // 2
    pivot_value = arr[pivot_index]
    lt, gt = partition(arr, left, right, pivot_value)
    quick_sort(arr, left, lt - 1)
    quick_sort(arr, gt + 1, right)

def partition(arr, left, right, pivot_value):
    lt = left
    i = left
    gt = right

    while i <= gt:
        if arr[i] < pivot_value:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot_value:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1
    return lt, gt

# Sprawdzenie, czy lista jest posortowana rosnąco
def is_sorted(arr):
    return all(arr[i - 1] <= arr[i] for i in range(1, len(arr)))

# Implementacja DFS dla znalezienia ścieżki do wyjścia
def dfs(matrix, start, exits):
    n = len(matrix)
    visited = [False] * (n + 1)
    stack = []
    parent = [-1] * (n + 1)
    stack.append(start)
    visited[start] = True

    while stack:
        v = stack[-1]

        if v in exits:
            # Znaleziono wyjście
            path = []
            current = v
            while current != -1:
                path.append(current)
                current = parent[current]
            path.reverse()
            return {'found': True, 'path': path}

        neighbors = []
        for i in range(n):
            if matrix[v - 1][i] == 1 and not visited[i + 1]:
                neighbors.append(i + 1)
                parent[i + 1] = v

        if neighbors:
            # Sortujemy sąsiadów
            quick_sort(neighbors, 0, len(neighbors) - 1)
            # Dodajemy najmniejszego sąsiada na stos
            next_node = neighbors[0]
            visited[next_node] = True
            stack.append(next_node)
        else:
            stack.pop()
    return {'found': False}

# Implementacja pełnego DFS dla kolejności ewakuacji
def full_dfs(matrix, start):
    n = len(matrix)
    visited = [False] * (n + 1)
    stack = []
    traversal_order = []
    visited[start] = True
    stack.append(start)
    traversal_order.append(start)

    while stack:
        v = stack[-1]
        neighbors = []
        for i in range(n):
            if matrix[v - 1][i] == 1 and not visited[i + 1]:
                neighbors.append(i + 1)

        if neighbors:
            # Sortujemy sąsiadów
            quick_sort(neighbors, 0, len(neighbors) - 1)
            # Dodajemy najmniejszego sąsiada na stos
            next_node = neighbors[0]
            visited[next_node] = True
            stack.append(next_node)
            traversal_order.append(next_node) # Dodajemy do kolejności odwiedzin
        else:
            stack.pop()
    return traversal_order

if __name__ == '__main__':
    main()
