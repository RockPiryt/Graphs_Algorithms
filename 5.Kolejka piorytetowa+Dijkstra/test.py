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


# Priority queue (Min heap)
class MinHeap:
    def __init__(self, capacity):
        self.storage = []  # Przechowujemy elementy w liście
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
    
    def parent(self, index):
        return self.storage[self.getParentIndex(index)]
    
    def leftChild(self, index):
        return self.storage[self.getLeftChildIndex(index)]
    
    def rightChild(self, index):
        return self.storage[self.getRightChildIndex(index)]
    
    def isFull(self):
        return self.size == self.capacity
    
    def swap(self, index1, index2):
        temp = self.storage[index1]
        self.storage[index1] = self.storage[index2]
        self.storage[index2] = temp
    
    def insertHeap(self, element):
        if self.isFull():
            raise ValueError("Heap is full")
        self.storage.append(element)
        self.size += 1
        self.heapifyUp()

    def heapifyUp(self):
        index = self.size - 1
        while self.hasParent(index) and self.parent(index)[0] > self.storage[index][0]:
            self.swap(self.getParentIndex(index), index)
            index = self.getParentIndex(index)

    def removeFromHeap(self):
        if self.size == 0:
            raise ValueError("Heap is empty")
        root = self.storage[0]
        self.storage[0] = self.storage[self.size - 1]
        self.size -= 1
        self.heapifyDown()
        return root  # Zwracamy całą krotkę (distance, vertex)

    def heapifyDown(self):
        index = 0
        while self.hasLeftChild(index):
            smallerChildIndex = self.getLeftChildIndex(index)
            if (self.hasRightChild(index) and self.rightChild(index)[0] < self.leftChild(index)[0]):
                smallerChildIndex = self.getRightChildIndex(index)

            if self.storage[index][0] < self.storage[smallerChildIndex][0]:
                break
            else:
                self.swap(index, smallerChildIndex)
            index = smallerChildIndex




def dijkstra(graph, start_vertex):

    num_vertices = len(graph)
    visited = [False] * num_vertices 
    print(f"visited {visited}")
    parent = [None] * num_vertices
    distances = [float('inf')] * num_vertices  
    
    distances[start_vertex] = 0  

    # Min-Heap, elementy to tuple(odległość, wierzchołek)
    min_heap = MinHeap(num_vertices)
    min_heap.insertHeap((0, start_vertex))  # Wstawiamy startowy wierzchołek z odległością 0

    path=[]

    while min_heap.size > 0:
        # Pobieramy wierzchołek z najmniejszą odległością (pierwszy z listy kolejkowej)
        removed_distance, removed_vertex = min_heap.removeFromHeap() # tupla
        visited[removed_vertex] = True
        end=1

        # #print the final path and distance to end point
        # if removed_vertex is end:
        #     while parent[removed_vertex]:
        #         path.append(removed_vertex.value)
        #         removed_vertex = parent[removed_vertex]
        #     path.append(start_vertex.value)
        #     print(f"shortest distance to {end.value}: ", distances[end])
        #     print(f"path to {end.value}: ", path[::-1])
        #     return
        


        for neighbor in range(num_vertices):
            # Jeśli już odwiedzony, przechodzimy dalej
            if visited[removed_vertex]:
                continue
            if weight > 0 and not visited[neighbor]: # Sprawdzamy, czy istnieje krawędź
                weight = graph[removed_vertex][neighbor]
                print(f"Waga pomiędzy {removed_vertex} i {neighbor} to {weight}")
                #licze nowy dystans
                new_distance = removed_distance + weight
                print(f"nowy obliczony dystans {new_distance} do sasiada {neighbor}")
                #Jeśli nowa odległość jest krótsza, aktualizujemy
                sasiad_odl = distances[neighbor] 
                print(f"obecnie najkrtosza droga do sasiada {sasiad_odl}")
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parent[neighbor] = removed_vertex
                    min_heap.insertHeap((new_distance, neighbor))

    return distances
            


if __name__ == "__main__":
    # Wprowadź dane grafu z wejścia
    print("Wprowadź dane grafu:")
    graph, start_vertex, error = read_graph_and_vertex()

    if error:
        print("Błąd przy wczytywaniu grafu.")
    else:
        print("Macierz sąsiedztwa:")
        for row in graph:
            print(row)
        
        print(f"Wierzchołek startowy: {start_vertex}")  # Wypisujemy numer wierzchołka startowego (1-based)
        print(f"Wierzchołek startowy +1: {start_vertex + 1}")  # Wypisujemy numer wierzchołka startowego (1-based)
        # Obliczamy najkrótsze ścieżki z wierzchołka startowego
        result = dijkstra(graph, start_vertex)

        # print(f"Najkrótsze ścieżki od wierzchołka {start_vertex + 1}:")
        # for i, dist in enumerate(result):
        #     print(f"Do wierzchołka {i + 1} = {dist}")
