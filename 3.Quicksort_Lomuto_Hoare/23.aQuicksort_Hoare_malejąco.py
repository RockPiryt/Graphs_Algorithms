"""malejąco"""

def quick_sort_desc(array):
    def swap(A, i1, i2):
        A[i1], A[i2] = A[i2], A[i1]  

    def partition(array, lo, hi):
        mid_point = (lo + hi) // 2
        pivot = array[mid_point]
        i = lo - 1
        j = hi + 1  

        while True:
            # Przesuń i w prawo, dopóki nie znajdziesz wartości <= pivot
            while True:
                i += 1
                if array[i] <= pivot:
                    break
            # Przesuń j w lewo, dopóki nie znajdziesz wartości >= pivot
            while True:
                j -= 1
                if array[j] >= pivot:
                    break
            # Jeżeli wskaźniki się miną, zwróć indeks podziału
            if j <= i:
                return j
            swap(array, i, j)

    def recursive_quicksort(array, lo, hi):
        if lo >= hi:
            return 
        pivot_index = partition(array, lo, hi)  # Znajdź pivot i podziel tablicę
        recursive_quicksort(array, lo, pivot_index)  # Sortuj lewą część
        recursive_quicksort(array, pivot_index + 1, hi)  # Sortuj prawą część

    recursive_quicksort(array, 0, len(array) - 1) 

# Przykład użycia:
arr = [3, 4, 9, 1, 7, 0, 5, 2, 6, 8]
quick_sort_desc(arr)
print("Posortowana tablica (malejąco):", arr)
