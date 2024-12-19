'''Napisz program, który wczytuje graf podany jako macierz sąsiedztwa i wyświetla listę sąsiedztwa danego grafu.

Elementy na liście są posortowane (można tutaj korzystać z wbudowanych funkcji/metod sortujących).

Sample Input 1:

0 1
1 0
Sample Output 1:

1 2
2 1
Sample Input 2:

0 1 0 1 1 0 1 1 1 1
1 0 1 1 1 0 0 1 1 1
0 1 0 1 0 1 1 0 1 0
1 1 1 0 1 1 1 1 1 1
1 1 0 1 0 1 0 0 1 0
0 0 1 1 1 0 1 1 0 1
1 0 1 1 0 1 0 1 0 1
1 1 0 1 0 1 1 0 1 1
1 1 1 1 1 0 0 1 0 0
1 1 0 1 0 1 1 1 0 0
Sample Output 2:

1 2 4 5 7 8 9 10
2 1 3 4 5 8 9 10
3 2 4 6 7 9
4 1 2 3 5 6 7 8 9 10
5 1 2 4 6 9
6 3 4 5 7 8 10
7 1 3 4 6 8 10
8 1 2 4 6 7 9 10
9 1 2 3 4 5 8
10 1 2 4 6 7 8'''

def read_adjacency_matrix():
    matrix = []
    try:
        while True:
            line = input().strip()
            if line:
                row = []
                elements = line.split()
                for x in elements:
                    row.append(int(x)) 
                matrix.append(row)
            else:
                break
    except EOFError:
        pass
    
    return matrix

def adjacency_matrix_to_list(matrix):
    adjacency_list = []
    num_vertices = len(matrix)

    for i in range(num_vertices):
        neighbors = []
        for j in range(num_vertices):
            if matrix[i][j] == 1:
                neighbors.append(j + 1)  # +1 to convert from 0-indexed to 1-indexed
        neighbors.sort()  # Sort the list of neighbors
        adjacency_list.append(neighbors)
    
    return adjacency_list

def print_adjacency_list(adjacency_list):
    for index in range(len(adjacency_list)):
        # Create a string of neighbors directly from the list
        neighbors_str = ' '.join(str(neighbor) for neighbor in adjacency_list[index])
        print(f"{index + 1} {neighbors_str}")

# Read the adjacency matrix from input
matrix = read_adjacency_matrix()

# Convert the adjacency matrix to an adjacency list
adjacency_list = adjacency_matrix_to_list(matrix)

# Print the adjacency list
print_adjacency_list(adjacency_list)

