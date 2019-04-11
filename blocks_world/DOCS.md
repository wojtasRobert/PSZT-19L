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
	* `_level_to_str` -
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

#### `best_heuristic_ever`

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

## Lista wykorzystanych narzędzi

* biblioteka `heapq`, funkcje: `heappop`, `heappush` w celu optymalizacji działania algorytmu
* biblioteki `functools`, `unittest` do testowania programu
* biblioteka `copy`, funkcja `deepcopy` używana przy rozwijaniu stanów
* biblioteka `random`, funkcje `shuffle` i `randrange` wykorzystywane przy generacji rozmieszczenia początkowego
* biblioteka `typing`, elementy `List`, `Callable` używane przy tworzeniu typów używanych w modelu 

## Instrukcja użytkownika

Będąc użytkownikiem naszego programu, mamy wpływ na kilka znaczących kwestii takich jak dobór heurystyk, liczba klocków i stosów oraz maksymalna liczba iteracji. Musimy przemyśleć liczbę bloków i liczbę stosów w stanie początkowym. Następnie naszym zadaniem jest przypisanie tych wartości 
odpowiednim zmiennym (BLOCKS, STACKS) w skrypcie `example.py`. W tym samym skrypcie mamy możliwość określenia pożądanych heurystyk, wpisując ich nazwy w odpowiednie miejsce w konstruktorze.
 Tolerowaną liczbą iteracji możemy zmienić w pliku `a_star.py` przypisując wartość do zmiennej `max_iterations` w definicji funkcji `a_star`. Kolejnym krokiem jest uruchomienie skryptu `example.py`. 
 W konsoli pojawi się jedna z dwóch wiadomości:

* Too many iterations! - oznaczające przekroczenie liczby iteracji a co za tym idzie porażkę w poszukiwaniach optymalnej sekwencji operatorów prowadzących do prawidłowego ustawienia klocków
* Liczba wykonanych iteracji oraz kroków potrzebnych na posortowanie klocków na pierwszym stosie oznacza sukces. Powyżej wyświetlane są stany od początkowego do terminalnego. 

## Wkład autorów

* Krystian Chachuła
	* model Stanu problemu
	* optymalizacja szybkości działania algorytmu A* przy wykorzystaniu kolejki priorytetowej
	* testy
	
* Robert Wojtaś
	* pierwotna implementacja algorytmu A*
	* implementacja funkcji heurystycznych
	* dokumentacja