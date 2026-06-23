# Analiza rynku mieszkań w Warszawie

## Opis projektu
Projekt polega na przeprowadzeniu eksploracyjnej analizy danych (EDA) dotyczących ofert sprzedaży mieszkań w Warszawie.

Dane zostały wygenerowane w Pythonie, a następnie poddane analizie statystycznej, wizualizacji, wykrywaniu wartości odstających oraz procesowi czyszczenia danych.

## Technologie
- Python
- pandas
- numpy
- matplotlib
- seaborn

## Zakres projektu

### 1. Wczytanie i eksploracja danych
Wykonano:
- wczytanie pliku mieszkania_warszawa.csv
- analizę rozmiaru zbioru danych
- analizę typów danych
- statystyki opisowe
- sprawdzenie brakujących wartości

### 2. Statystyki opisowe
Dla kolumny cena_pln obliczono:
- średnią
- medianę
- odchylenie standardowe
- współczynnik skośności (skewness)
- kurtozę (kurtosis)

Dla kolumny metraz_m2 obliczono:
- pierwszy kwartyl (Q1)
- trzeci kwartyl (Q3)
- rozstęp międzykwartylowy (IQR)

Dodatkowo wykonano analizę:
- liczby unikalnych dzielnic
- liczby ofert przypadających na każdą dzielnicę

### 3. Analiza pojedynczych zmiennych
Utworzono:
- histogram i KDE ceny mieszkań
- histogram i KDE metrażu mieszkań
- boxplot ceny mieszkań
- wykres liczby ofert według dzielnic

### 4. Analiza zależności
Wykonano:
- macierz korelacji zmiennych numerycznych
- wykres zależności metrażu od ceny
- analizę ceny za m² w podziale na dzielnice

Dodatkowo określono dzielnicę o najwyższej medianie ceny za metr kwadratowy.

### 5. Detekcja outlierów
W projekcie wykorzystano:
- metodę IQR
- metodę Z-score
- metodę Modified Z-score

Dodatkowo:
- wykryto outliery metrażu metodą IQR
- znaleziono błędne lata budowy

### 6. Czyszczenie danych
W projekcie wykonano:
- usunięcie nielogicznych lat budowy
- winsoryzację cen mieszkań (1 i 99 percentyl)
- transformację logarytmiczną ceny

### 7. Wizualizacja
Utworzono wykresy przedstawiające:
- rozkład cen mieszkań
- rozkład metrażu mieszkań
- liczbę ofert według dzielnic
- zależność metrażu od ceny
- korelacje pomiędzy zmiennymi
- ceny za m² w podziale na dzielnice
- wpływ transformacji logarytmicznej na rozkład cen

### 8. Wnioski
Na podstawie przeprowadzonej analizy sformułowano wnioski dotyczące:
- rozkładu cen mieszkań w Warszawie
- wpływu metrażu na cenę mieszkania
- różnic cenowych pomiędzy dzielnicami
- występowania wartości odstających
- jakości danych i potrzeby ich czyszczenia

## Jak uruchomić

1. Zainstaluj wymagane biblioteki:

pip install pandas numpy matplotlib seaborn

2. Uruchom program:

python analiza.py

## Pliki projektu
- analiza.py
- mieszkania_warszawa.csv
- README.md
- .gitignore

## Autor
Ryszard Chojnacki 160757
