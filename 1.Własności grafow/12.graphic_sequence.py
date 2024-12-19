"""Zadanie 1 (1 pkt)

Napisz program, który wczyta od użytkownika ciąg liczb, a następnie określi, 
czy ciąg ten jest graficzny czy nie (wyświetlając informacje TAK/NIE).

Sample Input 1:3 2 2 2 1
Sample Output 1:TAK
Sample Input 2:3 2 2 2 0
Sample Output 2:NIE
"""

"""
Wykorzystujemy:
----Lemat o uściskach dłoni: Jeśli suma stopni wierzchołków jest nieparzysta, to ciąg nie może być graficzny.
 Jeśli jest parzysta, przechodzimy do dalszej weryfikacji.

------Twierdzenie Hakima-Havela: Postępujemy iteracyjnie:
Sortujemy ciąg stopni w kolejności nierosnącej.
Pobieramy pierwszy element d1 (największy stopień) i 
redukujemy pierwsze d1 kolejnych elementów o 1 (symulując połączenie krawędzi).
Jeśli którykolwiek element w ciągu staje się ujemny, ciąg nie jest graficzny.
Powtarzamy kroki do momentu, gdy ciąg stopni zredukuje się do wszystkich zer (wtedy ciąg jest graficzny) 
lub natrafimy na ujemne liczby (wtedy nie jest graficzny).
"""

def is_graphic_sequence(sequence):
    # Lemat o uściskach dłoni
    if sum(sequence) % 2 != 0:
        return "NIE"
    
    # Sortujemy ciąg w porządku nierosnącym
    sequence.sort(reverse=True)
    
    
    # Twierdzenie Hakima-Havela
    while sequence and sequence[0] > 0:
        # Pobieramy i usuwamy pierwszy element (największy stopień)
        d = sequence.pop(0)
        
        # Jeśli d jest większe niż pozostała liczba elementów, nie jest graficzny
        if d > len(sequence):
            return "NIE"
        
        # Redukujemy pierwsze d elementów o 1
        for i in range(d):
            sequence[i] -= 1
            # Jeśli którykolwiek element jest ujemny, ciąg nie jest graficzny
            if sequence[i] < 0:
                return "NIE"
        
        sequence.sort(reverse=True)
    
    return "TAK"

# Wczytywanie danych wejściowych i uruchomienie programu
user_input = input().strip()
string_sequence = user_input.split()
sequence = [int(num) for num in string_sequence]

print(is_graphic_sequence(sequence))
