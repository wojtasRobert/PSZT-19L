---
title: Blocks World Problem -- dokumentacja wstępna
author: Krystian Chachuła, Robert Wojtaś
date: 11 kwietnia 2019
lang: pl-PL
geometry:
    - margin=1in
---
## Zadanie do wykonania

Załóżmy, że mamy N sześciennych, ponumerowanych klocków ułożonych w konfiguracji początkowej od 1 do N stosów, w których klocki ułożone są jeden na drugim w określonej kolejności. 
(Przykładowa konfiguracja początkowa dla N = 5 klocków to dwa stosy: (2, 5, 3) i (1, 4), albo jeden stos (1, 4, 5, 3, 2), albo 5 stosów: (1), (2), (3), (4), (5), itp.). 
Problem polega na ułożeniu klocków w jeden stos (1, 2, …, N) w minimalnej liczbie ruchów (akcji), przy czym pojedynczy ruch zdefiniowany jest jako zdjęcie jednego z klocków ze szczytu 
stosu i położenie go na szczycie innego stosu (lub stole, czyli „pustym stosie”). Przedstawiony problem należy rozwiązać przy wykorzystaniu algorytmu A* wyposażonego w zaproponowaną 
przez siebie stosowną heurystką. Rozwiązanie należy zaprezentować w formie implementacji programowej, umożliwiającej ustawienie wartości parametru N, zdefiniowanie konfiguracji 
początkowej, i następnie przedstawienie wynikowej minimalnej sekwencji ruchów wiodących do ułożenia klocków ww. konfiguracji docelowej.

## Kluczowe decyzje projektowe

* Projekt został napisany w języku Python.
* Program działa w trybie wsadowym. Wyniki działania wizualizowane są w konsoli.
* Wykorzystanie kilku funkcji heurystycznych i przyjmowanie wartości h(s) dla stanu s jako maksymalna wartość z zawartych funkcji.

## Struktura programu

Podczas tworzenia projektu poszczególne elementy zadania zostały zrealizowane w oddzielnych plikach:

* `model.py` - klasa reprezentująca stan problemu. Konstruktor klasy przyjmuje rozstawienie klocków w stanie początkowym (liczba klocków i stosów) oraz listę zawierającą nazwy funkcji heurystycznych.
 W tym miejsu zostały zaimplementowane takie elementy jak operatory porównania oraz znak mniejszości, a także wszystkie możliwe funkcje reprezentujące czynności, które w danym 
 stanie możemy wykonać:
	* `heuristic` - funkcja obliczająca wartość funkcji heurystycznej dla danego stanu jako wartość maksymalna z .
	* `move` - funkcja wykonująca ruch z jednego stosu klocków na inny, przyjmuje jako argumenty numer stosu źródłowego i numer stosu docelowego.
	* `copy` - wykonuje głęboką kopię stanu 
	* `sprout` - rozwinięcie stanu na wszyskie możliwe sposoby osiągane poprzez przeiterowanie przez wszystkie możliwe stosy źrółowe i wszystkie docelowe. Stany pochodne zwracane jako lista.
	* `print_backtrace` - drukuje sekwencję ruchów potrzebnych do otrzymania stanu terminalnego
	* `_level_to_str` -
	* `gen_layout` - generacja losowego stanu początkowego	

* `tests.py` - plik zawierający testy jednostkowe	
* `heuristics.py` 
* `a_star_py`

### `heuristics.py` 

Plik zawierający zaimplementowane funkcje heurystyczne, które można wykorzystać do rozwiązania problemu.

#### `blocks_outside_first_stack`

Funkcja zwraca liczbę kolcków znajdującą się poza pierwszym stosem. W praktyce okazała się mało efektywna ze względu braku uwzględnienia sortowania kolcków.

#### `misplaced_blocks`

Funkcja sprawdzająca prawidłowe rozmieszczenie klocków na stole, przy czym za prawidłowe uznawane jest ustawienie na pierwszym stosie, na pozycji odpowiadającej numerowi 
danego klocka. Wartość `h` jest zwiększana za każdy klocek, który znajduje się poza pierwszym stosem oraz za klocki na pierwszym stosie, które znajdują się na złej pozycji. 
W przypadku prawidłowego położenia klocka wartość `h` nie zwiększana.

#### `best_heuristic_ever`

Funkcja szacująca ilość ruchów potrzebnych na przełożenie każdego klocka na prawowite miejsce. Dla pierwszego stosu rozważane są przypadki ustawienia klocka na miejscu 
poniżej i powyżej docelowego. W razie wykrycia takiej sytuacji, wartość `h` jest odpowiednio zwiększana. Dla stosów poza wartością dodawaną do `h` jest liczba klocków 
znajdujących się aktualnie nad badanym klockiem oraz liczba klocków znajdujących się na stosie pierwszym, nad pozycją docelowa danego klocka. 

### `a_star.py`

