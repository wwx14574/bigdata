# Czyszczenie i analiza danych e-commerce

## Opis projektu
Projekt polega na wygenerowaniu brudnych danych dotyczących zamówień e-commerce, a następnie ich oczyszczeniu, przekształceniu oraz wykonaniu podstawowej analizy danych i wizualizacji.

Dane zostały przygotowane w Pythonie przy użyciu biblioteki pandas.

## Technologie
- Python
- pandas
- numpy
- matplotlib

## Zakres projektu

### 1. Generowanie danych
Program generuje plik zamowienia_messy.csv.

### 2. Eksploracja danych
Wykonano:
- sprawdzenie rozmiaru danych
- podgląd pierwszych rekordów
- analizę typów danych
- analizę braków danych
- analizę kategorii i wartości

### 3. Czyszczenie danych
W projekcie wykonano:
- usunięcie duplikatów
- standaryzację tekstu
- konwersję dat
- konwersję cen do typu float
- obsługę brakujących wartości
- usunięcie błędnych rekordów

### 4. Transformacje
Dodano nowe kolumny:
- wartosc_zamowienia
- rok
- miesiac
- nazwa_dnia
- email_poprawny

### 5. Analiza danych
Wykonano analizę:
- łącznej wartości zamówień w miesiącach
- top 5 klientów
- średniej wartości zamówienia według kategorii

### 6. Wizualizacja
Utworzono wykres słupkowy przedstawiający łączną wartość zamówień w każdym miesiącu.

### 7. Zapis danych
Oczyszczone dane zapisano do pliku zamowienia_clean.csv.

## Jak uruchomić

1. Zainstaluj wymagane biblioteki:
```
pip install pandas numpy matplotlib
```
2. Uruchom program:
```
python zad2.py
```
## Pliki projektu
- zad2.py
- zamowienia_messy.csv
- zamowienia_clean.csv
- README.md
- .gitignore

## Autor
Imię i nazwisko: ................................
