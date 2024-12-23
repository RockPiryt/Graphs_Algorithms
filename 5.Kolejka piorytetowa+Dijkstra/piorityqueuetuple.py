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


if __name__ == "__main__":
    # Tworzymy kopiec - max 10 elementów
    min_heap = MinHeap(10)

    # Wstawiamy elementy do kopca jako tuplę (priority, value)
    min_heap.insertHeap((10, "Task A"))
    min_heap.insertHeap((5, "Task B"))
    min_heap.insertHeap((3, "Task C"))
    min_heap.insertHeap((2, "Task D"))
    min_heap.insertHeap((8, "Task E"))

    # Print the current state of the heap
    min_heap.printHeap()

    # Usuwamy elementy z kopca i wyświetlamy
    print("Usunięty element:", min_heap.removeFromHeap())
    min_heap.printHeap()

    print("Usunięty element:", min_heap.removeFromHeap())
    min_heap.printHeap()
