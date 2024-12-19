def quick_sort(array):
    def swap(A, i1, i2):
        print(f"Zamiana elementów: A[{i1}]={A[i1]} <-> A[{i2}]={A[i2]}")
        A[i1], A[i2] = A[i2], A[i1]  # Zamienia dwa elementy w tablicy

    def visualize_pointers(array, i, j, pivot_index):
        # Generuje wizualizację tablicy z wskaźnikami `i`, `j` i pivota
        array_str = " ".join(f"{x:2}" for x in array)
        pointers = ["  "] * len(array)  # Pusta linia na wskaźniki
        pivot_line = ["  "] * len(array)  # Pusta linia na podkreślenie pivota
        if 0 <= i < len(array):
            pointers[i] = "^i"  # Wskaźnik `i`
        if 0 <= j < len(array):
            pointers[j] = "^j"  # Wskaźnik `j`
        if 0 <= pivot_index < len(array):
            pivot_line[pivot_index] = "p"  # Podkreślenie pivota
        print(array_str)
        print(" ".join(pointers))
        print(" ".join(pivot_line))

    def partition(array, lo, hi):
        mid_point = (lo + hi) // 2
        pivot = array[mid_point]
        print(f"\nPodział: lo={array[lo]}, hi={array[hi]}, pivot=A[{mid_point}]={pivot}")
        i = lo - 1  # Indeks początkowy dla lewej strony
        j = hi + 1  # Indeks początkowy dla prawej strony

        while True:
            # Przesuń i w prawo, dopóki nie znajdziesz wartości >= pivot
            while True:
                i += 1
                visualize_pointers(array, i, j, mid_point)  # Wizualizacja wskaźników
                print(f"  Wskaźnik i={i}, A[i]={array[i]}")
                if array[i] >= pivot:
                    break
            # Przesuń j w lewo, dopóki nie znajdziesz wartości <= pivot
            while True:
                j -= 1
                visualize_pointers(array, i, j, mid_point)  # Wizualizacja wskaźników
                print(f"  Wskaźnik j={j}, A[j]={array[j]}")
                if array[j] <= pivot:
                    break
            # Jeżeli wskaźniki się miną, zwróć indeks podziału
            if j <= i:
                print(f"Zwracamy pivot_index={j}, stan tablicy: {array}")
                return j
            # Zamiana elementów na pozycjach i oraz j
            swap(array, i, j)
            print(f"Po zamianie: {array}")

    def recursive_quicksort(array, lo, hi):
        if lo >= hi:
            return  # Warunek zakończenia rekurencji
        print(f"\nRekurencja: lo={array[lo]}, hi={array[hi]}, tablica={array}")
        pivot_index = partition(array, lo, hi)  # Znajdź pivot i podziel tablicę
        recursive_quicksort(array, lo, pivot_index)  # Sortuj lewą część
        recursive_quicksort(array, pivot_index + 1, hi)  # Sortuj prawą część

    print(f"Tablica początkowa: {array}")
    recursive_quicksort(array, 0, len(array) - 1)  # Wywołanie funkcji sortującej
    print(f"Tablica posortowana: {array}")

# Przykład użycia:
arr = [3, 4, 9, 1, 7, 0, 5, 2, 6, 8]
quick_sort(arr)

#                             j
# [3, 4, 9, 1, 7, 0, 5, 2, 6, 8]
#  i
