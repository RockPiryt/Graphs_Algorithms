'''Zadanie 3 (0.1 pkt)

Napisz program, który wczytuje graf nieskierowany podany jako lista sąsiedztwa i oblicza średni stopień całego grafu.

Wynik średniej zaokrąglamy do drugiego miejsca po przecinku.

Sample Input 1:

1 
2 
3 13 15 16
4 16
5 11 13
6 11 13
7 13 14 16
8 14 15
9 14 15
10 13 15
11 5 6
12 
13 3 5 6 7 10
14 7 8 9
15 3 8 9 10
16 3 4 7
Sample Output 1: 2.13

Sample Input 2:
1 2
2 1
Sample Output 2: 1.0
'''


#import math
from decimal import Decimal, ROUND_HALF_UP

def calculate_average_degree(graph):
    total_degrees = 0
    num_vertices = len(graph)
    
    # Calculate the degree of each vertex, excluding the first element (vertex label)
    for vertex in graph:
        total_degrees += len(vertex) - 1  # Odejmujemy 1, aby pominąć numer wierzchołka
    
    # Calculate the average degree
    average_degree = total_degrees / num_vertices
    #return round(average_degree, 2)

     # Use ceil to round to up
    #average_degree_ceiling = math.ceil(average_degree * 100) / 100.0
    average_degree_roundDecimal = Decimal(average_degree).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
    return average_degree_roundDecimal

def read_graph():
    graph = []
    
    # Read data until EOF
    try:
        while True:
            line = input().strip()
            if line:
                split_line = line.split() 
                neighbors = []                
                for x in split_line:           
                    neighbors.append(int(x))    
            else:
                neighbors = []  # Create an empty list for vertices with no neighbors
            graph.append(neighbors)
    except EOFError:
        pass
    
    return graph

# Read the graph
graph = read_graph()
#print("Readed Graph:\n")
#print(graph)

# Calculate the average degree of the graph
average_degree = calculate_average_degree(graph)

# Print the result
print(float(average_degree))  





