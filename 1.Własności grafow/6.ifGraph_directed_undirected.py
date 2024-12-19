'''Zadanie 8 (0.2 pkt)

Napisz program, który pobierze od użytkownika macierz sąsiedztwa, 
a następnie wyświetli informację czy graf jest skierowany czy nie wyświetlając odpowiedni 
komunikat (Graf jest nieskierowany lub Graf jest skierowany)

Sample Input 1:

0 0 0 1 1
0 0 0 0 0
0 0 0 0 1
1 0 0 0 1
1 0 1 1 0
Sample Output 1:

Graf jest nieskierowany
Sample Input 2:

0 0 0 1 0
0 0 0 1 1
0 0 0 1 1
0 0 0 0 0
1 0 0 1 0
Sample Output 2:

Graf jest skierowany'''

def is_graph_directed(matrix):
    n = len(matrix)  # size of the matrix (number of vertices)
    
    # Check if the matrix is symmetric along the diagonal
    for i in range(n):
        for j in range(i + 1, n):  # only check the upper half
            if matrix[i][j] != matrix[j][i]:
                return "Graf jest skierowany"
    
    return "Graf jest nieskierowany"

# Function to read the adjacency matrix from the user
def get_matrix():
    print("Enter the adjacency matrix, with each row separated by a newline:")
    
    # Take multiline input from the user, where rows are separated by a newline
    matrix_input = ""
    while True:
        try:
            row = input()  # Read each row
            if not row:  # End input on empty line
                break
            matrix_input += row + "\n"
        except EOFError:
            break
    
    # Process the input into a 2D list (matrix)
    matrix = []
    rows = matrix_input.strip().split("\n")
    for row in rows:
        row_elements = row.split()  #  get individual elements
        row_int = [] 
        for element in row_elements:
            row_int.append(int(element))  
        matrix.append(row_int)  # Append the list of integers to the matrix

    
    return matrix

# Main part of the program
matrix = get_matrix()
result = is_graph_directed(matrix)
print(result)
