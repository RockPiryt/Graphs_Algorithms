'''Zadanie 7 (0.4 pkt)

W sieci społecznej, użytkownicy są połączeni ze sobą poprzez różne relacje (np. przyjaźń, współpraca, itp.).
 Twoim zadaniem jest napisanie programu, który analizuje tę sieć i odpowiada na zapytania dotyczące relacji między użytkownikami. Sieć społeczna będzie reprezentowana jako nieskierowany graf, gdzie wierzchołki to użytkownicy, a krawędzie oznaczają relacje między nimi. Dane wejściowe będą podane jako słownik w Pythonie.

Napisz program, który polega na implementacji funkcji, która:

Wczytuje słownik reprezentujący listę sąsiedztwa z poziomu klawiatury.
Odpowiada na zapytania o:
Liczbę bezpośrednich sąsiadów danego użytkownika.
Czy dani dwaj użytkownicy są bezpośrednio połączeni.
Wejście:
Słownik reprezentujący listę sąsiedztwa. Klucze to identyfikatory użytkowników, a wartości to listy sąsiadów.
Liczba 
q (1 ≤ q ≤ 100) - liczba zapytań.
Następnie q linii, każda zawierająca zapytanie w jednym z trzech formatów:
neighbours x: Zapytanie o liczbę sąsiadów użytkownika x.
connection x y: Czy użytkownicy x i y są bezpośrednio połączeni? - ma zwrócić Yes/No w zależności od odpowiedzi.'''



'''Przykładowe wejście i wyjście
Wejście
{0: [1, 2], 1: [0, 2], 2: [0, 1]}
2
neighbours 0
connection 0 2

Wyjaśnienie
Słownik {0: [1, 2], 1: [0, 2], 2: [0, 1]} definiuje graf nieskierowany, gdzie:
Użytkownik 0 jest połączony z 1 i 2.
Użytkownik 1 jest połączony z 0 i 2.
Użytkownik 2 jest połączony z 0 i 1.

q = 2 oznacza, że są dwa zapytania:

neighbours 0: Ile połączeń ma użytkownik 0? (Odpowiedź: 2)

connection 0 2: Czy użytkownicy 0 i 2 są połączeni? (Odpowiedź: Yes)



Oczekiwane wyjście
2
Yes'''

import ast

def process_queries(graph, queries):
    results = []
    
    for query in queries:
        query_parts = query.split()
        command = query_parts[0]
        
        if command == "neighbours":
            x = int(query_parts[1])
            # Sprawdzamy liczbę sąsiadów użytkownika x
            num_neighbours = len(graph.get(x, []))
            results.append(str(num_neighbours))
        
        elif command == "connection":
            x = int(query_parts[1])
            y = int(query_parts[2])
            # Sprawdzamy, czy użytkownicy x i y są bezpośrednio połączeni
            if y in graph.get(x, []):
                results.append("Yes")
            else:
                results.append("No")
                
    return results



# wczytanie słownika z wejścia
graph = ast.literal_eval(input().strip()) 
# Wczytanie liczby zapytań
q = int(input().strip())                   

# Wczytanie zapytań
queries = []
for _ in range(q):
    queries.append(input().strip())

# Przetwarzanie zapytań i wyświetlanie wyników
results = process_queries(graph, queries)
for result in results:
    print(result)