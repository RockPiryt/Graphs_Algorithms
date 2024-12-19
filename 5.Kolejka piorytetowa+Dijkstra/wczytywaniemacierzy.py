import sys

# Funkcja wczytująca dane z wejścia
def read_graph_and_vertex():
    """Funkcja wczytująca graf jako macierz sąsiedztwa z wagami oraz wierzchołek startowy."""
    try:
        input_data = sys.stdin.read().strip()
        if not input_data:
            return None, None, True

        lines = input_data.split('\n')
        if len(lines) < 2:
            return None, None, True

        graph = []
        # Wczytujemy macierz sąsiedztwa (wagi krawędzi)
        for line in lines[:-1]:
            if line.strip():
                try:
                    weights = list(map(int, line.split()))
                    if len(weights) != len(lines) - 1:  # Sprawdzamy, czy liczba kolumn jest odpowiednia
                        return None, None, True
                    if not all(weight >= 0 for weight in weights):  # Sprawdzamy, czy wagi są nieujemne
                        return None, None, True
                    graph.append(weights)
                except ValueError:
                    return None, None, True

        start_vertex = lines[-1].strip()
        if not start_vertex.isdigit():
            return None, None, True

        start_vertex = int(start_vertex)
        if start_vertex < 1 or start_vertex > len(graph):
            return None, None, True

        return graph, start_vertex - 1, False  # Zwracamy macierz sąsiedztwa, indeks startowy (0-based) i brak błędu
    except Exception:
        return None, None, True


# Przykładowe użycie:
if __name__ == "__main__":
    print("Wprowadź dane grafu:")
    graph, start_vertex, error = read_graph_and_vertex()

    if error:
        print("Błąd przy wczytywaniu grafu.")
    else:
        print("Macierz sąsiedztwa:")
        for row in graph:
            print(row)
        
        print(f"Wierzchołek startowy: {start_vertex + 1}")  # Wypisujemy numer wierzchołka startowego (1-based)
