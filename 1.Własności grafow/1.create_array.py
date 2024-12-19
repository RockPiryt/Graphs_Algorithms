'''Zadanie 3 (0.1 pkt)

Napisz program, które pobierze liczbę naturalną n, 
a następnie wyświetli macierz sąsiedztwa wypełnione zerami rozmiaru  n×n. 
W przypadku podania złej liczby program ma wypisać komunikat BŁĄD oraz zakończyć działanie.

Sample Input:

4
Sample Output:

0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0'''

# Asking the user for the dimension of the matrix
#print("Insert size of array: ")
n = int(input())
if n <= 0:
    print("BŁĄD")

# Creating an empty matrix
matrix = []

# Filling the matrix with zeros using nested loops
for i in range(n):
    row = []
    for j in range(n):
        row.append(0)  
    matrix.append(row)  

# Print the matrix 
for i in range(n):
    for j in range(n):
        if j == n - 1:  
            print(matrix[i][j], end="")  # No space after the last element
        else:
            print(matrix[i][j], end=" ") 
    print()  