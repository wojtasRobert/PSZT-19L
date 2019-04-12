---
title: Przeszukiwanie przestrzeni stanów -- Projekt
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
* Reprezentacja stanu jako lista list. Listę zewnętrzną uznajemy za stół, a listy wewnętrzne za stosy klocków. Jest to wygodne ze względu na częste iterowanie po elementach stanu.
* Utworzenie klasy `State` reprezentującą stan rozwiązania problemu. Stan jest podstawową jednostką, na której operujemy podczas wykonania programu. Stany są wyświetlane i rozwijane, do tego aby przejść z jednego stanu do drugiego należy wykonać zdefiniowany w zadaniu ruch. Uznaliśmy, że najlepszym i najwygodniejszym rozwiązaniem będzie działanie na stanach jako obiektach klasy poprzez wywołyłanie jej metod. 
* Zawarcie w klasie `State` pola `heuristics` w celu umożliwienia dodania kilku funkcji heurystycznych dla zadania. Wartość h(s) dla stanu s wybierana jako maksymalna wartość z zawartych funkcji heurystycznych.
* Wykorzystanie kilku funkcji heurystycznych. Funkcje zdefiniowane w odrębnym pliku, uniwersalne dla różnych układów problemu.

## Struktura programu

Podczas tworzenia projektu poszczególne elementy zadania zostały zrealizowane w oddzielnych plikach:

* `model.py` - klasa `State` reprezentująca stan aktualnie rozwiązywanego problemu. Konstruktor klasy przyjmuje rozstawienie klocków w stanie początkowym (liczba klocków i stosów) oraz listę zawierającą nazwy funkcji heurystycznych.
 W tym miejsu zostały zaimplementowane takie elementy jak operatory porównania oraz znak mniejszości, a także wszystkie możliwe funkcje reprezentujące czynności, które w danym 
 stanie możemy wykonać:
	* `heuristic` - funkcja obliczająca wartość funkcji heurystycznej dla danego stanu jako wartość maksymalna ze wszystkich wartości zwróconych przez zawarte funkcje heurystyczne. Mając kilka heurystyk będących dolnym oszacowaniem kosztu dotarcia do stanu terminalnego rozsądnie jest wybrać największą wartość.
	* `move` - funkcja wykonująca ruch z jednego stosu klocków na inny, przyjmuje jako argumenty numer stosu źródłowego i numer stosu docelowego.
	* `copy` - wykonuje głęboką kopię stanu 
	* `sprout` - rozwinięcie stanu na wszyskie możliwe sposoby osiągane poprzez przeiterowanie przez wszystkie możliwe stosy źrółowe i wszystkie docelowe. Stany pochodne zwracane jako lista.
	* `print_backtrace` - drukuje sekwencję ruchów potrzebnych do otrzymania stanu terminalnego. Zrealizowane dzięki użyciu pola klasy o nazwie `parent`. Iterując wstecz po kolejno wybieranych stanach w łatwy sposób możemy otrzymać poprzednika każdego z nich co skutkuje prostym wyświetlaniem sekwencji kolejnych stanów od początkowego do terminalnego.
	* `gen_layout` - generacja losowego stanu początkowego	
	* Równość stanów została zdefiniowana w taki sposób, że dwa stany o stosach z tymi samymi elementami, ale różniących się rozmieszczeniem na stole są sobie równe. 
* `tests.py` - plik zawierający testy jednostkowe	
* `heuristics.py` 
* `a_star_py`

### `heuristics.py` 

Plik zawierający zaimplementowane funkcje heurystyczne, które można wykorzystać do rozwiązania problemu.

#### `blocks_outside_first_stack`

Funkcja zwraca liczbę kolcków znajdującą się poza pierwszym stosem. W praktyce okazała się mało efektywna ze względu na brak uwzględnienia sortowania kolcków.

#### `misplaced_blocks`

Funkcja sprawdzająca prawidłowe rozmieszczenie klocków na stole, przy czym za prawidłowe uznawane jest ustawienie na pierwszym stosie, na pozycji odpowiadającej numerowi 
danego klocka. Wartość `h` jest zwiększana za każdy klocek, który znajduje się poza pierwszym stosem oraz za klocki na pierwszym stosie, które znajdują się na złej pozycji. 
W przypadku prawidłowego położenia klocka wartość `h` nie zwiększana.

#### `estimate_moves`

Funkcja szacująca ilość ruchów potrzebnych na przełożenie każdego klocka na prawowite miejsce. Dla pierwszego stosu rozważane są przypadki ustawienia klocka na miejscu 
poniżej i powyżej docelowego. W razie wykrycia takiej sytuacji, wartość `h` jest odpowiednio zwiększana. Dla stosów poza wartością dodawaną do `h` jest liczba klocków 
znajdujących się aktualnie nad badanym klockiem oraz liczba klocków znajdujących się na stosie pierwszym, nad pozycją docelowa danego klocka. 

### `a_star.py`

Plik, w którym została zaimplementowana funkcja wykonująca algorytm A*. Wersja algorytmu została zaczerpnięta ze skryptu autorstwa dra Pawła Wawrzyńśkiego. Początkowo algorytm 
realizowany był z wykorzystaniem list Pythona i funkcji na nich operujących. Następnie jednak została dokonana optymalizacja działania programu poprzez zastosowanie rodzaju kolejki
priorytetowej `heapq` oraz operujących na niej funkcji `heappush` i `heappop`. Kolejka `heapq` jest wykorzystywana przez kolejkę `PriorityQueue`, która jednak poza uwzględnieniem priorytetów
dodawanych obiektów, zapewnia bezpieczeństwo wątków. Nasz program działa w jednym wątku dlatego używamy `heapq`, co skutkuje szybszym działaniem. Kolejnym usprawnieniem było dodanie 
zbioru stanów zbadanych do algorytmu. Miało to na celu uniknięcie powielania tych samych stanów w zbiorze stanów otwartych. Algorytm wykonywany jest w pętli dopóki zbiór stanów otwartych jest niepusty. Przed rozpoczęciem pętli
można ustawić maksymalną liczbę iteracji, której przekroczenie skutkować będzie wyjątkiem `TooManyIterations` oraz traktowane będzie jako porażka w znalezieniu optymalej sekwencji ruchów.

\pagebreak

## Lista wykorzystanych narzędzi

* biblioteka `heapq`, funkcje: `heappop`, `heappush` w celu optymalizacji działania algorytmu
* biblioteki `functools`, `unittest` do testowania programu
* biblioteka `copy`, funkcja `deepcopy` używana przy rozwijaniu stanów
* biblioteka `random`, funkcje `shuffle` i `randrange` wykorzystywane przy generacji rozmieszczenia początkowego
* biblioteka `typing`, elementy `List`, `Callable` używane przy tworzeniu typów używanych w modelu 

## Instrukcja użytkownika

### CLI

Dla użytkownika przygotowaliśmy interfejs w wierszu poleceń. Aby zobaczyć dostepne opcje należy wykonać polecenie:

```bash
python3 -m blocks_world -h
```

Przykłady użycia:

```bash
# Rozwiąż losowy problem z sześcioma blokami ułożonymi w trzy stosy. Wypisuj stany oraz operatory.
python -m blocks_world --random --blocks 6 --stacks 3 --verbose

# Rozwiąż problem z tzema zadanymi stosami: (od dołu) 1, 3, 2 oraz 5 oraz 2, 4. Max. l. iteracji 1000.
python -m blocks_world --initial [[0,3,1],[5],[2,4]] -it 1000 --verbose
```

* Too many iterations - oznaczające przekroczenie liczby iteracji a co za tym idzie porażkę w poszukiwaniach optymalnej sekwencji operatorów prowadzących do prawidłowego ustawienia klocków
* Liczba wykonanych iteracji oraz kroków potrzebnych na posortowanie klocków na pierwszym stosie oznacza sukces. Powyżej wyświetlane są stany od początkowego do terminalnego oraz . 

### Interfejs w języku Python

Będąc użytkownikiem naszego programu, mamy wpływ na kilka znaczących kwestii takich jak dobór heurystyk, liczba klocków i stosów oraz maksymalna liczba iteracji. Musimy przemyśleć liczbę bloków i liczbę stosów w stanie początkowym. Następnie naszym zadaniem jest przypisanie tych wartości 
odpowiednim zmiennym (BLOCKS, STACKS) w skrypcie `example.py`. W tym samym skrypcie mamy możliwość określenia pożądanych heurystyk, wpisując ich nazwy w odpowiednie miejsce w konstruktorze.
 Tolerowaną liczbą iteracji możemy zmienić w pliku `a_star.py` przypisując wartość do zmiennej `max_iterations` w definicji funkcji `a_star`. Kolejnym krokiem jest uruchomienie skryptu `example.py`. 

## Analiza wyników

* Rozwiązaliśmy 500 losowych problemów dla każdego wiersza tabeli.
* Limit iteracji wynosił 400.

Kolumny tabeli:

* $N_B$ -- liczba bloków
* $N_S$ -- liczba stosów
* $\overline{I}$ -- średnia liczba iteracji
* $\sigma I$ -- odchylenie standardowe liczby iteracji
* $\overline{C}$ -- średnia liczba kroków do rozwiązania
* $\sigma C$ -- odchylenie standardowe kroków do rozwiązania
* $\overline{\frac{C}{I}}[\%]$ -- średni stosunek liczby kroków do liczby iteracji
* $F[\%]$ -- średni stosunek niepowodzeń (przekroczenie max. l. iteracji) do wszystkich prób

\pagebreak

### $h \equiv 0$

| $N_B$  | $N_S$  | $\overline{I}$ | $\sigma I$ | $\overline{C}$ | $\sigma C$ | $\overline{\frac{C}{I}}[\%]$ | $F[\%]$ |
|---|---|--------|--------|------|------|-------|-------|
| 1 | 1 | 1.00   | 0.00   | 0.00 | 0.00 | 0.00  | 0.00  |
| 2 | 1 | 1.88   | 1.00   | 0.88 | 1.00 | 29.33 | 0.00  |
| 2 | 2 | 2.47   | 0.50   | 1.00 | 0.00 | 42.17 | 0.00  |
| 3 | 1 | 12.76  | 6.86   | 3.13 | 1.55 | 21.77 | 0.00  |
| 3 | 2 | 12.64  | 5.46   | 2.58 | 0.70 | 24.07 | 0.00  |
| 3 | 3 | 12.84  | 2.95   | 2.00 | 0.00 | 16.43 | 0.00  |
| 4 | 1 | 100.74 | 35.52  | 5.51 | 1.01 | 5.99  | 0.00  |
| 4 | 2 | 93.42  | 43.94  | 4.27 | 0.96 | 6.95  | 0.00  |
| 4 | 3 | 85.01  | 38.13  | 3.46 | 0.74 | 5.19  | 0.00  |
| 4 | 4 | 88.43  | 17.98  | 3.00 | 0.00 | 3.55  | 0.00  |
| 5 | 1 | 637.32 | 278.76 | 7.15 | 0.83 | 1.40  | 38.00 |
| 5 | 2 | 645.74 | 257.27 | 5.76 | 0.82 | 1.21  | 22.00 |
| 5 | 3 | 633.85 | 218.20 | 4.99 | 0.81 | 0.97  | 28.00 |
| 5 | 4 | 662.42 | 233.95 | 4.41 | 0.69 | 0.78  | 20.00 |
| 5 | 5 | 728.94 | 125.81 | 4.00 | 0.00 | 0.57  | 0.00  |

### $h$: Liczba bloków poza największym stosem

| $N_B$  | $N_S$  | $\overline{I}$ | $\sigma I$ | $\overline{C}$ | $\sigma C$ | $\overline{\frac{C}{I}}[\%]$ | $F[\%]$ |
|---|---|--------|--------|------|------|-------|-------|
| 1 | 1 | 1.00   | 0.00   | 0.00 | 0.00 | 0.00  | 0.00  |
| 2 | 1 | 1.90   | 1.00   | 0.90 | 1.00 | 30.00 | 0.00  |
| 2 | 2 | 2.49   | 0.50   | 1.00 | 0.00 | 41.83 | 0.00  |
| 3 | 1 | 11.74  | 7.15   | 3.07 | 1.54 | 26.04 | 0.00  |
| 3 | 2 | 10.72  | 6.78   | 2.43 | 0.73 | 32.37 | 0.00  |
| 3 | 3 | 8.19   | 2.62   | 2.00 | 0.00 | 26.98 | 0.00  |
| 4 | 1 | 59.26  | 33.56  | 5.43 | 1.01 | 13.11 | 0.00  |
| 4 | 2 | 67.93  | 35.67  | 4.50 | 0.85 | 10.23 | 0.00  |
| 4 | 3 | 74.25  | 61.22  | 3.60 | 0.64 | 11.34 | 0.00  |
| 4 | 4 | 38.43  | 17.51  | 3.00 | 0.00 | 10.82 | 0.00  |
| 5 | 1 | 367.16 | 271.93 | 7.29 | 0.82 | 3.59  | 25.00 |
| 5 | 2 | 438.80 | 258.31 | 6.15 | 0.81 | 2.66  | 13.00 |
| 5 | 3 | 366.97 | 255.03 | 5.12 | 1.01 | 4.68  | 27.00 |
| 5 | 4 | 432.59 | 309.05 | 4.64 | 0.61 | 3.65  | 14.00 |
| 5 | 5 | 247.80 | 184.40 | 4.00 | 0.00 | 2.90  | 3.00  |
| 6 | 1 | 486.14 | 230.10 | 7.21 | 2.36 | 4.47  | 86.00 |
| 6 | 2 | 419.92 | 303.99 | 6.31 | 0.95 | 2.74  | 87.00 |
| 6 | 3 | 396.82 | 266.41 | 5.27 | 1.01 | 5.66  | 89.00 |
| 6 | 4 | 538.53 | 237.23 | 5.24 | 0.56 | 1.41  | 83.00 |
| 6 | 5 | 513.84 | 289.00 | 4.92 | 0.40 | 2.04  | 75.00 |
| 6 | 6 | 602.50 | 267.54 | 5.00 | 0.00 | 1.28  | 58.00 |

### $h$: Liczba bloków nieposortowanych na największym stosie

| $N_B$  | $N_S$  | $\overline{I}$ | $\sigma I$ | $\overline{C}$ | $\sigma C$ | $\overline{\frac{C}{I}}[\%]$ | $F[\%]$ |
|---|---|--------|--------|------|------|-------|-------|
| 1 | 1 | 1.00   | 0.00   | 0.00 | 0.00 | 0.00  | 0.00  |
| 2 | 1 | 2.08   | 1.00   | 1.08 | 1.00 | 36.00 | 0.00  |
| 2 | 2 | 2.00   | 0.00   | 1.00 | 0.00 | 50.00 | 0.00  |
| 3 | 1 | 8.99   | 4.18   | 3.30 | 1.38 | 33.99 | 0.00  |
| 3 | 2 | 8.51   | 3.00   | 2.58 | 0.71 | 32.03 | 0.00  |
| 3 | 3 | 7.13   | 1.07   | 2.00 | 0.00 | 28.80 | 0.00  |
| 4 | 1 | 70.54  | 34.50  | 5.40 | 1.26 | 9.10  | 0.00  |
| 4 | 2 | 70.02  | 43.08  | 4.31 | 0.87 | 9.14  | 0.00  |
| 4 | 3 | 61.23  | 29.26  | 3.66 | 0.61 | 7.75  | 0.00  |
| 4 | 4 | 53.95  | 18.66  | 3.00 | 0.00 | 6.39  | 0.00  |
| 5 | 1 | 476.57 | 210.85 | 7.34 | 0.76 | 2.01  | 12.00 |
| 5 | 2 | 496.68 | 284.34 | 6.01 | 0.96 | 2.32  | 22.00 |
| 5 | 3 | 460.64 | 256.70 | 5.07 | 0.96 | 1.88  | 17.00 |
| 5 | 4 | 466.80 | 222.16 | 4.54 | 0.60 | 1.33  | 7.00  |
| 5 | 5 | 387.15 | 165.26 | 4.00 | 0.00 | 1.20  | 2.00  |

### $h$: Maksimum z dwóch poprzednich heurystyk

| $N_B$  | $N_S$  | $\overline{I}$ | $\sigma I$ | $\overline{C}$ | $\sigma C$ | $\overline{\frac{C}{I}}[\%]$ | $F[\%]$ |
|---|---|--------|--------|------|------|-------|-------|
| 1 | 1 | 1.00   | 0.00   | 0.00 | 0.00 | 0.00  | 0.00  |
| 2 | 1 | 1.94   | 1.00   | 0.94 | 1.00 | 31.33 | 0.00  |
| 2 | 2 | 2.00   | 0.00   | 1.00 | 0.00 | 50.00 | 0.00  |
| 3 | 1 | 7.54   | 4.07   | 2.94 | 1.65 | 32.47 | 0.00  |
| 3 | 2 | 7.36   | 3.25   | 2.49 | 0.78 | 37.67 | 0.00  |
| 3 | 3 | 4.76   | 0.85   | 2.00 | 0.00 | 43.30 | 0.00  |
| 4 | 1 | 46.35  | 22.33  | 5.56 | 0.67 | 16.25 | 0.00  |
| 4 | 2 | 50.21  | 31.41  | 4.42 | 0.82 | 13.76 | 0.00  |
| 4 | 3 | 41.07  | 24.33  | 3.58 | 0.70 | 14.96 | 0.00  |
| 4 | 4 | 23.62  | 7.33   | 3.00 | 0.00 | 14.90 | 0.00  |
| 5 | 1 | 318.92 | 227.49 | 7.31 | 1.19 | 5.29  | 9.00  |
| 5 | 2 | 311.00 | 243.90 | 5.98 | 1.10 | 5.76  | 8.00  |
| 5 | 3 | 305.82 | 249.10 | 5.13 | 0.81 | 4.91  | 7.00  |
| 5 | 4 | 301.10 | 254.34 | 4.63 | 0.65 | 5.07  | 1.00  |
| 5 | 5 | 85.51  | 68.83  | 4.00 | 0.00 | 6.63  | 0.00  |
| 6 | 1 | 404.35 | 266.70 | 7.65 | 2.03 | 2.64  | 83.00 |
| 6 | 2 | 462.80 | 315.42 | 6.65 | 0.93 | 3.00  | 80.00 |
| 6 | 3 | 292.16 | 294.41 | 5.37 | 0.83 | 5.42  | 81.00 |
| 6 | 4 | 456.72 | 340.81 | 5.22 | 0.73 | 3.31  | 82.00 |
| 6 | 5 | 381.41 | 233.37 | 4.90 | 0.41 | 2.27  | 71.00 |
| 6 | 6 | 376.34 | 180.69 | 5.00 | 0.00 | 1.93  | 4.00  |


Analizując wyniki z tabeli można zauważyć kilka zależności.

* Przypadki, gdzie $N_B = N_S$ tzn. że każdy blok leży na oddzielnym stosie są proste do rozwiązania. Wymagają one najmniej iteracji algorytmu.
* Najwięcej iteracji zajmuje rozwiązanie takich przypadków, gdzie $N_B >> N_S$.

\pagebreak

## Profilowanie kodu

Lista najbardziej czasochłonnych czynności posortowana malejąco:

* Porządkowanie stosów przy stwierdzaniu równości stanów
* Obliczanie wartości funkcji heurystycznych
* Tworzenie głębokiej kopii stanów przy rozwijaniu stanów

## Wkład autorów

* Krystian Chachuła
	* model Stanu problemu
	* optymalizacja szybkości działania algorytmu A* przy wykorzystaniu kolejki priorytetowej
	* testy
	
* Robert Wojtaś
	* pierwotna implementacja algorytmu A*
	* implementacja funkcji heurystycznych
	* dokumentacja
