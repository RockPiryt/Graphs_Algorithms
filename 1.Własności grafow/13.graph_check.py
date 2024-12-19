import math

def read_graph():
    '''funkcja wczytująca graf jako lista sąsiedztwa'''
    graph = []
    
    # Read data until EOF
    try:
        while True:
            line = input().strip()
            if line:
                split_line = line.split() 
                neighbors = []                
                for x in split_line:
                    try:
                        neighbors.append(int(x))  
                    except ValueError:
                        # Pomijamy znaki, które nie są liczbami
                        continue    
            else:
                neighbors = []  # Create an empty list for vertices with no neighbors
            graph.append(neighbors)
    except EOFError:
        pass
    
    return graph

def count_edges(graph):
    '''funkcja zliczająca ilość krawędzi'''
    edge_count = 0  
    
    for neighbors in graph:
        edge_count += len(neighbors) - 1  # Odejmujemy 1, aby pominąć numer wierzchołka
        
    return edge_count // 2  

def get_degrees(graph):
    '''Funkcja zwracająca ciąg stopni wierzchołków'''
    degrees = []
    for neighbors in graph:
        degrees.append(len(neighbors) - 1)  # Odejmujemy 1, aby pominąć numer wierzchołka
    return degrees


def calculate_average_degree(graph):
    '''funckja licząca średni stopień grafu'''
    total_degrees = 0
    num_vertices = len(graph)
    
    for vertex in graph:
        total_degrees += len(vertex) - 1  # Odejmujemy 1, aby pominąć numer wierzchołka
    
    average_degree = total_degrees / num_vertices
        
    return average_degree

# ----------------------------------------------------------------------------------sprawdzenie klasy grafu
def is_cycle(graph, vertex_count, edge_count, degrees):
    ''' funkcja sprawdzajaca czy graf jest cyklem'''

    # m = n (ilośc krawędzi musi być równa ilości wierzchołków)
    if vertex_count  != edge_count:
        return False
    

    # każdy wierzchołek 2 stopnia
    degrees = get_degrees(graph)  
    for degree in degrees:
        if degree != 2:
            return False  
    return True  

def is_completed(vertex_count, degrees):
    '''Funkcja sprawdzająca, czy graf jest pełny '''
    
    # Sprawdzamy, czy stopień każdego wierzchołka jest równy n-1
    for degree in degrees:
        if degree != vertex_count - 1:
            return False  
    
    return True  

def is_path(vertex_count, degrees):
    '''funkcja sprawdzająca czy graf jest ścieżka'''
    # flagi 
    degree_1_count = 0
    degree_2_count = 0
    
    # Iterujemy przez stopnie wierzchołków i zliczamy wierzchołki o stopniu 1 i 2
    for degree in degrees:
        if degree == 1:
            degree_1_count += 1
        elif degree == 2:
            degree_2_count += 1
    
    # dwa wierzchołki na krańcach maja 1,reszta stopnia 2
    if degree_1_count == 2 and degree_2_count == vertex_count - 2:
        return True
    else:
        return False
    
def is_tree(graph, vertex_count, edge_count, degrees):
    '''funkcja sprawdzająca czy graf jest drzewem'''
    #m=n-1 oraz niecykliczny, brak wierzchołków izolowanych
    if edge_count == vertex_count - 1 and not is_cycle(graph, vertex_count, edge_count, degrees):
        for degree in degrees:
            if degree == 0:  
                return False
        return True
    return False


    

def is_hypercube(vertex_count, degrees):
    '''funkcja sprawdzająca czy graf jest hiperkostka'''
    # Liczba wierzchołków musi być potęgą liczby 2 (2^n)
    if vertex_count == 0 or not (math.log2(vertex_count)).is_integer():
        return False
    
    # Obliczamy wymiar hiperkostki: n = log2(vertex_count)
    dimension = int(math.log2(vertex_count))
    
    # Sprawdzamy, czy każdy wierzchołek ma dokładnie 'dimension' sąsiadów
    for degree in degrees:
        if degree != dimension:
            return False
    
    return True

# Read the graph
graph = read_graph()
vertex_count = len(graph)
edge_count = count_edges(graph)

# Obliczenie ciągu stopni wierzchołków
degrees = get_degrees(graph) #3 3 1 2 4 4 3 2 4 2
# Obliczanie średniego stopnia grafu
average_degree = calculate_average_degree(graph)


# Sprawdzanie klasy grafu
ifcycled_graph = is_cycle(graph, vertex_count, edge_count, degrees)
ifcompleted_graph = is_completed(vertex_count, degrees)
ifpathed_graph = is_path(vertex_count, degrees)
iftree_graph = is_tree(graph, vertex_count, edge_count, degrees)
ifhipercube_graph = is_hypercube(vertex_count, degrees)

print(f"Ilość wierzchołków: {vertex_count}")
print(f"Ilość krawędzi: {edge_count}")
print("Stopnie wierzchołków:", ' '.join(map(str, degrees)))
print(f"Średni stopień: {average_degree:.2f}")

#print(f"Graf cykliczny: {ifcycled_graph} ")
#print(f"Graf pełny: {ifcompleted_graph} ")
#print(f"Graf jest scieżką: {ifpathed_graph} ")
#print(f"Graf jest drzewem: {iftree_graph} ")
#print(f"Graf jest hiperkostką: {ifhipercube_graph} ")

#print(f"Określenie klasy grafu---------------")

# Sprawdzanie, do jakiej klasy należy graf
if ifcompleted_graph:
    print("Jest to graf pełny")
if ifcycled_graph:
    print("Jest to cykl")
if ifpathed_graph:
    print("Jest to ścieżka")
if iftree_graph:
    print("Jest to drzewo")
if ifhipercube_graph:
    print("Jest to hiperkostka")

if not (ifpathed_graph or iftree_graph or ifcycled_graph or ifcompleted_graph or ifhipercube_graph):
    print("Graf nie należy do żadnej z podstawowych klas")








