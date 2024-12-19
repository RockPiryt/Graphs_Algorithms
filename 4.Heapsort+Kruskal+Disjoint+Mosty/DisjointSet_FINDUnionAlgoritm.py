#DisjoinSet wykorzystywana do wykrywania cykli w grafie oraz w algorytmie Kruskala (który wyznacza min drzewo spinające)

# Cykl gdy oba analizowane wierzchołki w grafie mają rodziców należących do tego samego subset
# find_parent(node) == find_parent(neighboor) - Cycled Graph

class DisjointSet:
    # zestaw zbiorów 1 elementowych, gdzie każdy wierzchołek jest swoim rodzicem
    parent=[0,1,2]

     #szukanie rodzica
    def Find_parent(self, a):
        # jeśli jest sam dla siebie rodzicem
        if a == self.parent[a]:
            return a
        # w przeciwnym wypadku szukaj rodzica subset
        else:
            #rekurencyjne wywołanie
            return self.Find_parent(self.parent[a])
          
     # łączenie 2 subset w jeden poprzez okreslenie rodzica dla analizowanego wierzchołka 
    def Union (self, x, y):
        xroot = self.Find_parent(x)
        yroot = self.Find_parent(y) 
        self.parent[xroot]=yroot

if __name__ == '__main__':
    ds=DisjointSet()

    graph = {
        0:[1,2],
        1:[2],
        2:[]
    }
    
    #DFS po sąsiadach
    for node in graph:
        for neighboor in graph[node]:
            nodeParent = ds.Find_parent(node)
            neighboorParent = ds.Find_parent(neighboor) 
            if nodeParent == neighboorParent:
                print("Cyclic Grpah")
            ds.Union(nodeParent, neighboorParent)
    
