# Analiza danych o krajach świata

## Opis projektu
Projekt polega na pobraniu danych o krajach świata z API REST Countries, przetworzeniu ich w Pythonie, zapisaniu do bazy SQLite oraz wykonaniu analizy danych przy użyciu SQL. Na końcu tworzony jest wykres przedstawiający populację w podziale na regiony.

## Technologie
- Python
- pandas
- requests
- sqlite3
- matplotlib

## Zakres projektu

### 1. Pobieranie danych
Dane zostały pobrane z API:
https://restcountries.com/

Z API wyciągnięto:
- nazwa kraju
- stolica
- region
- subregion
- populacja
- powierzchnia
- waluta

### 2. Przetwarzanie danych
Dane zostały przekształcone do formatu DataFrame (pandas).

### 3. Baza danych
Dane zapisano do bazy SQLite: kraje_swiata.db  
Tabela: kraje

### 4. Analiza SQL
Wykonane zapytania:
- suma populacji świata
- 10 najludniejszych krajów
- liczba krajów i średnia populacja w regionach
- kraje większe niż Polska
- kraj o największej gęstości zaludnienia

### 5. Wizualizacja
Wykres słupkowy pokazujący populację w podziale na regiony.

## Jak uruchomić

1. Zainstaluj biblioteki:
pip install pandas requests matplotlib

2. Uruchom program:
python zad1.py

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
Ryszard Chojnacki 160757
