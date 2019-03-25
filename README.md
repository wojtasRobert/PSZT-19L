# Zadanie projektowe 1 z PSZT, semestr letni 2019

* dr hab. inż. Tomasz Martyn, martyn@ii.pw.edu.pl
* konsultacje: piątki, godz. 10.15-12.00, pok. nr 312
* Termin oddania projektu: 12 kwietnia 2019 r.
* Punktacja: 0 – 15 p.
* Każdy rozpoczęty tydzień zwłoki powyżej terminu oddania: -5 p.

## Zawartość projektu.

1. Projekty realizowane są zespołach 2-osobowych.
2. Cały projekt składa się z dwóch części: dokumentacji oraz projektu właściwego.
3. Dokumentacja powinna być zwięzła i MUSI zawierać:
    - imiona i nazwiska autorów projektu,
    - zestawienie kluczowych decyzji projektowych,
    - opis struktury programu, ze szczególnym uwzględnieniem części dotyczącej implementacji mechanizmów sztucznej inteligencji,
    - listę wykorzystanych narzędzi, bibliotek, itp.
    - instrukcję użytkownika programu, w szczególności opis interfejsu użytkownika,
    - wymienienie wkładu poszczególnych autorów w projekt (tzn. kto co zrobił).
4. Projektem właściwym jest implementacja programowa zadania projektowego, wykonana przy wykorzystaniu dowolnego języka programowania średniego poziomu (C++, C#, Java, Python, etc.): należy dostarczyć zarówno kod źródłowy, jak i program wykonywalny (o ile wykorzystany język programowania jest kompilowalny), przy czym kod programu musi być klarowny, odpowiednio zorganizowany i dobrze skomentowany, zgodnie z zasadami inżynierii oprogramowania.
5. O ile nie uzgodniono tego wcześniej ze mną, w implementacji NIE MOŻNA korzystać z istniejących bibliotek mechanizmów sztucznej inteligencji – wszystkie algorytmy w tym zakresie należy zaimplementować samemu.

## Oddawania projektu i warunki zaliczenia.

1. Projekty oddawane są w całości w wersji elektronicznej (zarówno dokumentacja, jak i projekt właściwy).
2. W celu oddania projektu należy mi go w pierwszej kolejności zaprezentować zarówno w działaniu, jak i w zakresie kodu źródłowego, przy czym należy mieć na uwadze, iż mogę mieć pytania odnoszące się do różnych szczegółów implementacyjnych, dlatego podczas demonstrowania projektu pożądana jest obecność całego zespołu wykonawców.
3. W przypadku braku jednego ze składników projektu projekt, o których mowa w pkt. 2.a, projekt uznaje się za niezaliczony.
4. W ocenie będą brane pod uwagę następujące elementy:
    - aplikacja w zakresie udostępnianej przez nią funkcjonalności, ze szczególnych uwzględnieniem jej działania w zakresie wdrożenia mechanizmów sztucznej inteligencji;
    - jakość kodu źródłowego, ze szczególnym uwzględnieniem implementacji algorytmów sztucznej inteligencji;
    - dokumentacja.

## Treść zadania

Załóżmy, że mamy N sześciennych, ponumerowanych klocków ułożonych w konfiguracji początkowej od 1 do N stosów, w których klocki ułożone są jeden na drugim w określonej kolejności. (Przykładowa konfiguracja początkowa dla N = 5 klocków to dwa stosy: (2, 5, 3) i (1, 4), albo jeden stos (1, 4, 5, 3, 2), albo 5 stosów: (1), (2), (3), (4), (5), itp.). Problem polega na ułożeniu klocków w jeden stos (1, 2, …, N) w minimalnej liczbie ruchów (akcji), przy czym pojedynczy ruch zdefiniowany jest jako zdjęcie jednego z klocków ze szczytu stosu i położenie go na szczycie innego stosu (lub stole, czyli „pustym stosie”). Przedstawiony problem należy rozwiązać przy wykorzystaniu algorytmu A* wyposażonego w zaproponowaną przez siebie stosowną heurystką. Rozwiązanie należy zaprezentować w formie implementacji programowej, umożliwiającej ustawienie wartości parametru N, zdefiniowanie konfiguracji początkowej, i następnie przedstawienie wynikowej minimalnej sekwencji ruchów wiodących do ułożenia klocków ww. konfiguracji docelowej.

## Info z konsultacji

* Python to dobry wybór
* program ma działać w trybie wsadowym, prezentacja nie jest bardzo istotna
* nasz problem jest klasyczny (Blocks World Problem), można znaleźć heurystyki w internecie (https://ai.stackexchange.com/a/4110)
