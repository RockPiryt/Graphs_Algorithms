def max_heapify(Array, n, i):

    largest = i
    left = 2*i + 1
    right =2*i +2   

    # ustalam największą wartość z rozpatrywanej trójki (rodzc+dzieci)
    # largest so far is compared with right child
    if right < n  and Array[largest] < Array[right]:
        largest = right

    # largest so far is compared with left child
    if left < n  and Array[largest] < Array[left]:
        largest = left

    # kiedy rodzic nie jest większy od dzieci
    # change parent
    if  largest !=i:
        Array[i], Array[largest] = Array[largest], Array[i]
    
        # recursive call
        max_heapify(Array, n, largest)


def heapSort(Array):
    n=len(Array)
    lastElement = n - 1 
    firstElement = 0 
    step = -1 # cofanie
    for i in range (lastElement, firstElement, step):# i to  aktualna ilość elementów do sortowania, najpierw są wszystkie elementy, potem o 1 mniej itd.  6,5,4,3,2,1
        #Zmiana największego elementu z Max heap (root) z ostatnim elementem
        Array[i], Array[firstElement] =  Array[firstElement], Array[i]
       
        # przywracanie własności kopca metoda rekurencyjną
        max_heapify(Array, i , 0)


if __name__ == "__main__":
    # Entry data
    myList = [5, 16, 8, 14, 20, 1, 26]
    n=len(myList)

    # Build Heap Max
    lpn = n//2 - 1 #last parent node
    end = -1 #aby objeło także index 0 
    step = -1 # cofanie się o krok ndeksy odwiedzane przez pętlę: lpn =2, lpn-1=1 lpn-2=0(root)
    for i in range(lpn, end, step):
        max_heapify(myList, n, i)

    # Display
    print("Kopiec typu max:")
    for i in range(n):
        print(myList[i])

    heapSort(myList)
    print(f"lista posortowana: {myList}")


    

    
    
