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


class MinHeap:
    def __init__(self, capacity):
        self.storage = [None] * capacity  # wszystkie jako None dla lepszej czytelności
        self.capacity = capacity  # wielkość kopca
        self.size = 0  # początkowa wielkość kopca

    #-------------------------------------------------------- pobieranie indexów rodzica i dzieci
    def getParentIndex(self, index):
        return (index - 1) // 2

    def getLeftChildIndex(self, index):
        return 2 * index + 1

    def getRightChildIndex(self, index):
        return 2 * index + 2

    #------------------------------------------------------- sprawdzenie posiadania rodzica/dzieci
    def hasParent(self, index):
        # index rodzica musi być większy lub równy 0 (może być root)
        return self.getParentIndex(index) >= 0

    def hasLeftChild(self, index):
        # index dziecka musi być mniejszy od aktualnej wielkości kopca
        return self.getLeftChildIndex(index) < self.size

    def hasRightChild(self, index):
        # index dziecka musi być mniejszy od aktualnej wielkości kopca
        return self.getRightChildIndex(index) < self.size

    #-------------------------------------------------------- zwracanie wartości na konkretnym indexie rodzica, left i right
    def parent(self, index):
        # wyciągam z listy storage aktualną wartość na wybranym indexie
        return self.storage[self.getParentIndex(index)]

    def leftChild(self, index):
        return self.storage[self.getLeftChildIndex(index)]

    def rightChild(self, index):
        return self.storage[self.getRightChildIndex(index)]

    # ------------------------------------------------------- pomocnicze funkcje
    def isFull(self):
        return self.size == self.capacity

    def swap(self, index1, index2):
        temp = self.storage[index1]
        self.storage[index1] = self.storage[index2]
        self.storage[index2] = temp

    # ------------------------------------------------------ iteracyjnie wkładania do stosu
    # wkładanie do stosu 
    def insertHeap(self, element):
        if self.isFull():
            raise Exception("Kopiec pełny")
        # wstawienie elementu na ostatnim miejscu kopca
        self.storage[self.size] = element
        self.size += 1
        # przywrócenie własności kopca min
        self.heapifyUp()

    # przywracanie własności kopca min idąc w górę (rodzic ma być mniejszy lub równy dzieciom)
    def heapifyUp(self):
        # index wstawianego ostatnio elementu
        index = self.size - 1
        # jeżeli obecny węzeł ma rodzica i rodzic jest większy od tego noda to zrób swap
        while (self.hasParent(index) and self.parent(index)[0] > self.storage[index][0]):
            self.swap(self.getParentIndex(index), index)
            # kontynuacja w górę swapowania jeżeli potrzeba
            index = self.getParentIndex(index)

    # ------------------------------------------------------ iteracyjnie usuwanie ze stosu
    # usuwanie ze stosu 
    def removeFromHeap(self):
        # gdy kopiec pusty
        if self.size == 0:
            raise Exception("Kopiec pusty")
        
        # kopiec zawiera elementy
        # usuwany będzie root zawsze (bo to najmniejszy element w kopcu min)
        removedElement = self.storage[0]
        # ustanowienie nowego root, nowym root staje się ostatni element w kopcu
        self.storage[0] = self.storage[self.size - 1]
        self.size -= 1
        # przywracam własność kopca w dół
        self.heapifyDown()

        # zwrot co zostało usunięte
        return removedElement

    def heapifyDown(self):
        # zaczynam od root bo z tamtąd był usuwany element
        index = 0
        # muszę sprawdzić które dziecko lewe czy prawe ma mniejszą wartość i wtedy zamienić z mniejszym dzieckiem 
        # musi mieć dziecko jak ma być przywracana własność (jak ma prawe to ma też lewe (musi być kompletnym drzewem binarnym), dlatego sprawdzam tylko czy ma lewe)
        while (self.hasLeftChild(index)):
            # pobieram wartość lewego dziecka - na razie zakładam że lewe jest mniejsze
            smallerChildIndex = self.getLeftChildIndex(index)

            # sprawdzam czy prawe dziecko nie jest mniejsze od lewego
            if (self.hasRightChild(index) and self.rightChild(index)[0] < self.leftChild(index)[0]):
                smallerChildIndex = self.getRightChildIndex(index)
            
            # jeśli root mniejszy od dzieci to ok
            if (self.storage[index][0] < self.storage[smallerChildIndex][0]):
                break
            else:
                # jeśli jest rodzic większy od dzieci to zamień miejscami
                self.swap(index, smallerChildIndex)
            # przywracanie własności ma iść do końca jeżeli potrzeba, więc ustawiam smallerChildIndex jako index do kolejnego sprawdzenia
            index = smallerChildIndex

    def printHeap(self):
        """Print the current state of the heap."""
        print("Kopiec po wstawieniu elementów:", self.storage[:self.size])



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





def graph_diameter_with_dijkstra(graph):
    """
    Oblicza średnicę grafu wykorzystując algorytm Dijkstry.
    :param graph: Macierz sąsiedztwa z wagami.
    :return: Średnica grafu.
    """
    num_vertices = len(graph)
    max_distances = []

    for start_vertex in range(num_vertices):
        distances = dijkstra(graph, start_vertex)
        # Maksymalna odległość z danego wierzchołka
        max_distance = max(distances.values())
        max_distances.append(max_distance)

    # Średnica grafu to największa odległość
    return max(max_distances)




if __name__ == "__main__":
    # print("Wprowadź dane grafu:")
    graph, error = read_graph()

    if error:
        print("BŁĄD")
    else:

        # print("Macierz sąsiedztwa:")
        # for row in graph:
        #     print(row)
        
        # start_vertex=0
        # distances = dijkstra(graph, start_vertex)

        # print("Shortest distances from start vertex:")
        # for vertex, distance in distances.items():
        #     print(f"{vertex + 1} = {distance}")

        
        # Obliczenie średnicy grafu
        diameter = graph_diameter_with_dijkstra(graph)
        # print("Średnica grafu:", diameter)
        print( diameter)
