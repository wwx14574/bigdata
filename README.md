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
python projekt.py

## Autor
Ryszard Chojnacki 160757
