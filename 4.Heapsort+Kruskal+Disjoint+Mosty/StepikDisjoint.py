class DisjointSet:
    def __init__(self, n):
        # zestaw zbiorów 1 elementowych, gdzie każdy wierzchołek jest swoim rodzicem
        self.parent = list(range(n))  
        self.rank = [0] * n          

    def Find_parent(self, x):
        # jeśli jest sam dla siebie rodzicem
        if x == self.parent[x]:
            return x
        # w przeciwnym wypadku szukaj rodzica subset
        else:
            #rekurencyjne wywołanie
            return self.Find_parent(self.parent[x])

    def union(self, x, y):
        xRoot = self.Find_parent(x)
        yRoot = self.Find_parent(y)

        if xRoot == yRoot:
            print("Cyclic Grpah")
            return  # x and y are already in the same set

        # Union by rank: attach smaller rank tree under the root of the higher rank tree
        if self.rank[xRoot] < self.rank[yRoot]:
            self.parent[xRoot] = yRoot
        elif self.rank[xRoot] > self.rank[yRoot]:
            self.parent[yRoot] = xRoot
        else:
            # If ranks are the same, make one root and increment its rank
            self.parent[yRoot] = xRoot
            self.rank[xRoot] += 1

# Example usage:
ds = DisjointSet(5)  # Create a disjoint set with 5 elements: 0, 1, 2, 3, 4

# Union some sets
ds.union(0, 1)
ds.union(1, 2)
ds.union(3, 4)

# Find representatives of sets
print(ds.Find_parent(0))  # Output: 0 (representative of set containing 0, 1, 2)
print(ds.Find_parent(1))  # Output: 0 (same set as 0, path compression)
print(ds.Find_parent(2))  # Output: 0 (same set as 0 and 1)
print(ds.Find_parent(3))  # Output: 3 (representative of set containing 3, 4)
print(ds.Find_parent(4))  # Output: 3 (same set as 3)
