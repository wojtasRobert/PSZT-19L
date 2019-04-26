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
przez siebie stosowną heurystkę. Rozwiązanie należy zaprezentować w formie implementacji programowej, umożliwiającej ustawienie wartości parametru N, zdefiniowanie konfiguracji 
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

#### `move_once_or_twice`

Omawiana heurystyka szacuje ilość potrzebnych do wykonania ruchów operujących na danym klocku, w celu przemieszczenia go na docelową pozycję. Dopuszczalne scenariusze to jeden lub
dwa ruchy przypadające na brany pod uwagę klocek. Funkcja dla każdego stanu bada wszystkie stosy zaczynając od najwyższego. Dopóki pozycja klocka zgadza się z jego pozycją docelową wartość `h` nie jest zwiększana. 
W momencie napotkania klocka o nieprawidłowej pozycji `h` jest zwiększane o ilość klocków ponad aktualnie badanym (plus klocek badany). Dla tych klockó należy wykonać co najmniej 
dwa ruchy. Dla pozostałych stosów, klocek leżący na stole zawsze wymaga tylko jednego ruchu. Każdy inny klocek wymaga jednego lub dwóch ruchów, w zależności od tego czy numer klocka 
jest większy lub mniejszy od klocka bezpośrednio pod nim. W programie zostały utworzone zmienne `h1` i `h2` odpowiadające ilości klocków wymagających jednego ruchu i ilości klocków 
wymagających dwóch ruchów. Funkcja `move_once_or_twice` zwraca sumę `h1 + h2`. 

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
# Rozwiąż losowy problem z sześcioma blokami ułożonymi w trzy stosy. 
# Wypisuj stany oraz operatory.
python -m blocks_world --random --blocks 6 --stacks 3 --verbose

# Rozwiąż problem z tzema zadanymi stosami: (od dołu) 1, 3, 2 oraz 5 oraz 2, 4.
# Max. l. iteracji 1000.
python -m blocks_world --initial [[0,3,1],[5],[2,4]] -it 1000 --verbose
```

Aby wypróbować różne funkcje heurystyczne, należy użyć parametru `--heuristics`, o którym możemy poczytać w `--help`.
```python
# -he
#     0 -- deafult, max of all heuristics; " \
#     1 -- blocks_outside_biggest_stack; " \
#     2 -- unsorted_biggest_stack_blocks; " \
#     3 -- move_once_or_twice"
python -m blocks_world -i [[0,3,1],[2]] -vv -he 3
```

### Interfejs w języku Python

Będąc użytkownikiem naszego programu, mamy wpływ na kilka znaczących kwestii takich jak dobór heurystyk, liczba klocków i stosów oraz maksymalna liczba iteracji. Musimy przemyśleć liczbę bloków i liczbę stosów w stanie początkowym. Następnie naszym zadaniem jest przypisanie tych wartości 
odpowiednim zmiennym (BLOCKS, STACKS) w skrypcie `example.py`. W tym samym skrypcie mamy możliwość określenia pożądanych heurystyk, wpisując ich nazwy w odpowiednie miejsce w konstruktorze.
 Tolerowaną liczbą iteracji możemy zmienić w pliku `a_star.py` przypisując wartość do zmiennej `max_iterations` w definicji funkcji `a_star`. Kolejnym krokiem jest uruchomienie skryptu `example.py`. 

## Analiza wyników

* Rozwiązaliśmy 500 losowych problemów dla każdego wiersza tabeli.
* Limit iteracji wynosił 500.

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

| $N_B$  | $N_S$  | $\overline{I}$ | $\sigma I$ | $\overline{C}$ | $\sigma C$ | $\overline{\frac{C}{I}}[\%]$ | $F[\%]$ |
|---|---|--------|--------|------|------|-------|-------|
| 2 | 1 | 0.96  | 1.00  | 0.96 | 1.00 | 100.00 | 0.00 |
| 2 | 2 | 1.48  | 0.50  | 1.00 | 0.00 | 76.20  | 0.00 |
| 3 | 1 | 11.50 | 6.78  | 3.13 | 1.51 | 43.01  | 0.00 |
| 3 | 2 | 10.35 | 5.43  | 2.44 | 0.79 | 32.33  | 0.00 |
| 3 | 3 | 11.64 | 2.78  | 2.00 | 0.00 | 18.21  | 0.00 |
| 4 | 1 | 93.15 | 40.03 | 5.26 | 1.30 | 10.43  | 0.00 |
| 4 | 2 | 92.59 | 41.21 | 4.28 | 0.96 | 7.07   | 0.00 |
| 4 | 3 | 91.72 | 35.95 | 3.59 | 0.64 | 4.74   | 0.00 |
| 4 | 4 | 89.66 | 17.38 | 3.00 | 0.00 | 3.49   | 0.00 |

Table: $h \equiv 0$ \label{t_noh}

Analizując tabelę \ref{t_noh} można zaobserwować jak szybko rośnie średnia liczba iteracji algorytmu wraz ze stopniem skomplikowania problemu, w sytuacji gdy funkcja heurystyczna jest tożsamościowo równa zero.
Maksymalna liczba bloków, dla jakiej dało się otrzymać rozwiązanie w sensownym czasie to 4.
Najwięcej iteracji wymagało rozwiązanie zadania, w którym 4 bloków było ułozone w 1 stos.
Warto też zauważyć, że dla przypadków, gdzie $N_B = N_S$, tzn. każdy blok leży na oddzielnym stosie, zawsze wystarczy wykonać $N_B - 1$ ruchów, aby uporządkować klocki na jednym stosie.
Zatem dla każdego wiersza takiego, że $N_B = N_S$, powinno być $\overline{C} = N_B - 1$ i $\sigma C = 0$.
Wszystkie zamieszczone tutaj tabele potwierdzają ten wniosek.


| $N_B$  | $N_S$  | $\overline{I}$ | $\sigma I$ | $\overline{C}$ | $\sigma C$ | $\overline{\frac{C}{I}}[\%]$ | $F[\%]$ |
|---|---|--------|--------|------|------|-------|-------|
| 2 | 1 | 1.02   | 1.00   | 1.02 | 1.00 | 100.00 | 0.00  |
| 2 | 2 | 1.50   | 0.50   | 1.00 | 0.00 | 75.00  | 0.00  |
| 3 | 1 | 10.85  | 7.10   | 3.11 | 1.50 | 48.18  | 0.00  |
| 3 | 2 | 10.35  | 6.46   | 2.49 | 0.77 | 42.49  | 0.00  |
| 3 | 3 | 7.31   | 2.80   | 2.00 | 0.00 | 31.77  | 0.00  |
| 4 | 1 | 61.81  | 34.31  | 5.41 | 1.21 | 16.01  | 0.00  |
| 4 | 2 | 59.60  | 35.70  | 4.33 | 0.85 | 13.32  | 0.00  |
| 4 | 3 | 70.51  | 51.43  | 3.64 | 0.64 | 11.87  | 0.00  |
| 4 | 4 | 38.97  | 17.90  | 3.00 | 0.00 | 10.68  | 0.00  |
| 5 | 1 | 227.36 | 140.77 | 6.75 | 1.25 | 7.85   | 48.20 |
| 5 | 2 | 220.91 | 140.92 | 5.56 | 0.98 | 6.82   | 48.60 |
| 5 | 3 | 212.03 | 143.02 | 4.77 | 0.77 | 6.14   | 44.00 |
| 5 | 4 | 188.81 | 141.94 | 4.26 | 0.62 | 6.02   | 46.60 |
| 5 | 5 | 174.17 | 91.17  | 4.00 | 0.00 | 3.75   | 10.40 |

Table: $h$: Liczba bloków poza największym stosem \label{t_outside}

W tabeli \ref{t_outside} widać poprawę działania algorytmu w porównaniu z tabelą \ref{t_noh}.
Tym razem dla układu $4, 1$ średnia liczba iteracji wynosiła $61.81$ zamiast $93.15$.
Udało nam się także w rozsądnym czasie uzyskać wyniki dla 5 klocków.
Wprowadzenie funkcji heurystycznej wyraźnie poprawia wydajność algorytmu.


| $N_B$  | $N_S$  | $\overline{I}$ | $\sigma I$ | $\overline{C}$ | $\sigma C$ | $\overline{\frac{C}{I}}[\%]$ | $F[\%]$ |
|---|---|--------|--------|------|------|-------|-------|
| 2 | 1 | 1.01   | 1.00   | 1.01 | 1.00 | 100.00 | 0.00  |
| 2 | 2 | 1.00   | 0.00   | 1.00 | 0.00 | 100.00 | 0.00  |
| 3 | 1 | 7.46   | 4.06   | 3.20 | 1.43 | 54.43  | 0.00  |
| 3 | 2 | 7.09   | 3.32   | 2.48 | 0.76 | 42.50  | 0.00  |
| 3 | 3 | 6.03   | 1.15   | 2.00 | 0.00 | 34.64  | 0.00  |
| 4 | 1 | 65.24  | 34.20  | 5.30 | 1.29 | 14.00  | 0.00  |
| 4 | 2 | 68.88  | 40.15  | 4.28 | 0.98 | 10.59  | 0.00  |
| 4 | 3 | 58.99  | 31.18  | 3.61 | 0.65 | 8.70   | 0.00  |
| 4 | 4 | 50.59  | 17.57  | 3.00 | 0.00 | 6.77   | 0.00  |
| 5 | 1 | 280.50 | 131.78 | 6.63 | 1.12 | 5.41   | 64.60 |
| 5 | 2 | 277.54 | 146.74 | 5.37 | 1.00 | 3.51   | 54.00 |
| 5 | 3 | 271.85 | 127.08 | 4.60 | 0.73 | 2.54   | 53.00 |
| 5 | 4 | 299.37 | 123.60 | 4.25 | 0.62 | 1.79   | 51.00 |
| 5 | 5 | 334.50 | 83.61  | 4.00 | 0.00 | 1.28   | 22.40 |

Table: $h$: Liczba bloków nieposortowanych na największym stosie \label{t_nosort}

| $N_B$  | $N_S$  | $\overline{I}$ | $\sigma I$ | $\overline{C}$ | $\sigma C$ | $\overline{\frac{C}{I}}[\%]$ | $F[\%]$ |
|---|---|--------|--------|------|------|-------|-------|
| 2 | 1 | 1.05   | 1.00   | 1.05 | 1.00 | 100.00 | 0.00  |
| 2 | 2 | 1.00   | 0.00   | 1.00 | 0.00 | 100.00 | 0.00  |
| 3 | 1 | 5.26   | 2.87   | 3.18 | 1.41 | 71.78  | 0.00  |
| 3 | 2 | 4.87   | 2.50   | 2.50 | 0.77 | 64.37  | 0.00  |
| 3 | 3 | 2.00   | 0.00   | 2.00 | 0.00 | 100.00 | 0.00  |
| 4 | 1 | 22.69  | 18.06  | 5.46 | 1.47 | 40.15  | 0.00  |
| 4 | 2 | 24.05  | 19.30  | 4.42 | 1.08 | 34.09  | 0.00  |
| 4 | 3 | 22.15  | 16.01  | 3.84 | 0.87 | 39.12  | 0.00  |
| 4 | 4 | 3.00   | 0.00   | 3.00 | 0.00 | 100.00 | 0.00  |
| 5 | 1 | 137.91 | 113.95 | 7.71 | 1.24 | 12.92  | 0.00  |
| 5 | 2 | 120.14 | 106.70 | 6.32 | 1.10 | 12.37  | 1.60  |
| 5 | 3 | 116.64 | 110.47 | 5.61 | 1.08 | 16.03  | 1.20  |
| 5 | 4 | 105.38 | 119.48 | 4.90 | 1.02 | 36.71  | 0.20  |
| 5 | 5 | 4.00   | 0.00   | 4.00 | 0.00 | 100.00 | 0.00  |
| 6 | 1 | 218.05 | 133.42 | 9.35 | 1.23 | 8.98   | 44.00 |
| 6 | 2 | 219.06 | 148.04 | 7.80 | 1.15 | 8.03   | 39.60 |
| 6 | 3 | 197.94 | 138.73 | 6.99 | 1.02 | 8.13   | 41.40 |
| 6 | 4 | 166.17 | 148.58 | 6.21 | 1.14 | 17.47  | 37.80 |
| 6 | 5 | 97.18  | 153.31 | 5.62 | 0.89 | 45.42  | 34.40 |
| 6 | 6 | 5.00   | 0.00   | 5.00 | 0.00 | 100.00 | 0.00  |


Table: $h$: Ilosc potrzebnych ruchow dla danego klocka \label{t_rob}

Trzecia rozważana funkcja heurystyczna radzi sobie zdecydowanie najlepiej z przewidywaniem właściwego kierunku ruchu.
W tabeli \ref{t_rob} można zauważyć dużo mniejsze średnie liczby iteracji niż do tej pory.
Co ciekawe, dla $N_B = N_S$ algorytm zawsze od początku do końca szedł ścieżką prowadzącą do rozwiązania, co widać po wskaźniku $\overline{\frac{C}{I}}[\%]$.


| $N_B$  | $N_S$  | $\overline{I}$ | $\sigma I$ | $\overline{C}$ | $\sigma C$ | $\overline{\frac{C}{I}}[\%]$ | $F[\%]$ |
|---|---|--------|--------|------|------|-------|-------|
| 2 | 1 | 0.95   | 1.00   | 0.95 | 1.00 | 100.00 | 0.00  |
| 2 | 2 | 1.00   | 0.00   | 1.00 | 0.00 | 100.00 | 0.00  |
| 3 | 1 | 5.32   | 2.93   | 3.17 | 1.43 | 71.13  | 0.00  |
| 3 | 2 | 4.82   | 2.55   | 2.47 | 0.79 | 64.90  | 0.00  |
| 3 | 3 | 2.00   | 0.00   | 2.00 | 0.00 | 100.00 | 0.00  |
| 4 | 1 | 24.13  | 17.51  | 5.60 | 1.39 | 36.99  | 0.00  |
| 4 | 2 | 24.80  | 19.46  | 4.48 | 1.09 | 33.39  | 0.00  |
| 4 | 3 | 23.67  | 16.35  | 3.95 | 0.93 | 37.76  | 0.00  |
| 4 | 4 | 3.00   | 0.00   | 3.00 | 0.00 | 100.00 | 0.00  |
| 5 | 1 | 130.97 | 107.59 | 7.73 | 1.26 | 13.55  | 0.00  |
| 5 | 2 | 127.56 | 121.63 | 6.30 | 1.19 | 13.15  | 1.40  |
| 5 | 3 | 113.36 | 106.84 | 5.58 | 1.04 | 15.62  | 0.80  |
| 5 | 4 | 114.37 | 123.51 | 4.97 | 0.99 | 34.79  | 0.40  |
| 5 | 5 | 4.00   | 0.00   | 4.00 | 0.00 | 100.00 | 0.00  |
| 6 | 1 | 198.39 | 128.58 | 9.19 | 1.25 | 9.26   | 42.40 |
| 6 | 2 | 208.78 | 146.77 | 7.78 | 1.20 | 8.25   | 42.00 |
| 6 | 3 | 207.55 | 145.08 | 6.89 | 1.00 | 8.66   | 39.80 |
| 6 | 4 | 175.41 | 144.54 | 6.48 | 1.09 | 16.04  | 43.00 |
| 6 | 5 | 87.73  | 146.76 | 5.59 | 0.87 | 46.34  | 30.60 |
| 6 | 6 | 5.00   | 0.00   | 5.00 | 0.00 | 100.00 | 0.00  |

Table: $h$: Maksimum z trzech poprzednich heurystyk \label{t_max1}

Podczas konsultacji z dr. Tomaszem Martynem dowiedzieliśmy się, że mając kilka funkcji heurystycznych będących dolnym oszacowaniem (\textit{ang. admissible}), można otrzymać trzecią -- dającą lepsze oszacowanie -- poprzez obliczanie maksimum z wartości tych funkcji dla każdego stanu.
Tak też postąpiliśmy, używając trzech, wcześniej wspomnianych heurystyk.
Wyniki tego działania można zaobserwować w tabeli \ref{t_max1}.
Od razu można zauważyć że wyniki te są lepsze niż jakiekolwiek inne uzyskane do tej pory.


Podsumowując:

* Przypadki, gdzie $N_B = N_S$ tzn. że każdy blok leży na oddzielnym stosie są proste do rozwiązania zarówno przez człowieka, jak i przez algorytm A* z dobrą heurystyką.
* Warto łączyć \textit{admissible} heurystyki za pomocą funkcji maksimum, aby otrzymać lepszą funkcję heurystyczną.
* Liczba iteracji nie rośnie tak szybko, wraz ze stopniem komplikacji zadania, gdy użyta jest dobra funkcja heurystyczna w porównaniu z przypadkiem gdy funkcja heurystyczna jest zawsze równa zero.
* Najbardziej skomplikowane problemy, jakich rozwiązanie udało nam się uzyskać w rozsądnym czasie to takie, gdzie $N_B = 6$.

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
