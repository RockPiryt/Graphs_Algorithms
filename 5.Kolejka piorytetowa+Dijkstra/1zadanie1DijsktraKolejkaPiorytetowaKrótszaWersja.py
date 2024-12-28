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

class MinHeap:
    def __init__(self, capacity):
        self.storage = [None] * capacity
        self.capacity = capacity
        self.size = 0



    def getParentIndex(self, index):
        return (index - 1) // 2

    def getLeftChildIndex(self, index):
        return 2 * index + 1

    def getRightChildIndex(self, index):
        return 2 * index + 2

    def hasParent(self, index):
        return self.getParentIndex(index) >= 0

    def hasLeftChild(self, index):
        return self.getLeftChildIndex(index) < self.size

    def hasRightChild(self, index):
        return self.getRightChildIndex(index) < self.size

    def swap(self, index1, index2):
        self.storage[index1], self.storage[index2] = self.storage[index2], self.storage[index1]

    def resize(self):
        """Podwaja pojemność kopca."""
        self.capacity *= 2
        self.storage.extend([None] * (self.capacity - len(self.storage)))

    def insertHeap(self, element):
        if self.size == self.capacity:
            self.resize()  # Zwiększenie rozmiaru kopca
        self.storage[self.size] = element
        self.size += 1
        self.heapifyUp()

    def heapifyUp(self):
        index = self.size - 1
        while self.hasParent(index):
            parent_index = self.getParentIndex(index)
            if self.storage[parent_index][0] <= self.storage[index][0]:
                break
            self.swap(parent_index, index)
            index = parent_index

    def removeFromHeap(self):
        if self.size == 0:
            raise Exception("Kopiec pusty")
        removed_element = self.storage[0]
        self.storage[0] = self.storage[self.size - 1]
        self.size -= 1
        self.heapifyDown()
        return removed_element

    def heapifyDown(self):
        index = 0
        while self.hasLeftChild(index):
            smaller_child_index = self.getLeftChildIndex(index)
            if self.hasRightChild(index) and self.storage[self.getRightChildIndex(index)][0] < self.storage[smaller_child_index][0]:
                smaller_child_index = self.getRightChildIndex(index)
            if self.storage[index][0] <= self.storage[smaller_child_index][0]:
                break
            self.swap(index, smaller_child_index)
            index = smaller_child_index

    def printHeap(self):
        print("Kopiec:", self.storage[:self.size])



def dijkstra(graph, start):
    # Determine the number of vertices in the graph
    num_vertex = len(graph)
    
    # Initialize previous, visited, and distances dictionaries
    previous = {v: None for v in range(num_vertex)}
    visited = {v: False for v in range(num_vertex)}
    distances = {v: float("inf") for v in range(num_vertex)}
    distances[start] = 0

    # Initialize MinHeap with a capacity of the number of vertices
    min_heap = MinHeap(num_vertex)

    # Insert the start vertex with a distance of 0 into the heap
    min_heap.insertHeap((distances[start], start))
            
    while min_heap.size > 0:
        removed_distance, removed_vertex = min_heap.removeFromHeap()
        visited[removed_vertex] = True

        
        # Explore all neighbors of the current vertex
        for neighbor in range(num_vertex):
            # print(f"neighbor {neighbor}")
            weight = graph[removed_vertex][neighbor]
            # print(f"waga {weight}")
        

            
            # If the vertex has been visited, skip it
            if visited[neighbor]:
                continue
            if weight > 0:  
                # print(f"obecny dystans {distances[neighbor]}")
                new_distance = removed_distance + weight
                # print(f"nowy dystans {new_distance}")
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = removed_vertex
                    # print(f"parent nieghbora po aktualizacji {previous[neighbor]}")
                    # print(f"parent lista po aktualizacji {previous}")

                    current_distance = distances[neighbor]
                    # print(f"dystans po aktualizacji {current_distance}")

                    # print(f"wstawiany neighbor do kopca {neighbor}")

                    tupla_wst=(current_distance,neighbor)
                    # print(f"wstawiana tupla {tupla_wst}")
                
                    # Add the neighbor to the heap with the updated distance
                    min_heap.insertHeap(tupla_wst)
                    # min_heap.printHeap()

   
    return distances




if __name__ == "__main__":
    # Wprowadź dane grafu z wejścia
    # print("Wprowadź dane grafu:")
    graph, start_vertex, error = read_graph_and_vertex()

    if error:
        # print("Błąd przy wczytywaniu grafu.")
        print("BŁĄD")
    else:
        # print("Macierz sąsiedztwa:")
        # for row in graph:
        #     print(row)
        
        # print(f"Wierzchołek startowy: {start_vertex}")  # Wypisujemy numer wierzchołka startowego (1-based)
        # print(f"Wierzchołek startowy +1: {start_vertex + 1}")  # Wypisujemy numer wierzchołka startowego (1-based)


        distances = dijkstra(graph, start_vertex)

        # print("Shortest distances from start vertex:")
        for vertex, distance in distances.items():
            print(f"{vertex + 1} = {distance}")

        

