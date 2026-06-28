# Analiza rynku koncertów muzycznych w Polsce

## Opis projektu

Projekt polega na analizie danych dotyczących rynku koncertów muzycznych w Polsce z wykorzystaniem języka Python oraz biblioteki Plotly do tworzenia interaktywnych wizualizacji danych.

Celem projektu było poznanie podstaw wizualizacji prezentacyjnej oraz przygotowanie zestawu wykresów umożliwiających analizę rynku koncertowego w Polsce.

## Wykorzystane technologie

* Python
* pandas
* numpy
* plotly

## Zakres projektu

### 1. Wczytanie i eksploracja danych

Dane zostały wczytane z pliku `koncerty_polska.csv`. Następnie przeprowadzono podstawową analizę zbioru danych:

* liczba rekordów,
* liczba kolumn,
* typy danych,
* liczba unikalnych miast,
* liczba gatunków muzycznych.

### 2. Analiza przychodów według miasta

Przygotowano interaktywny wykres słupkowy przedstawiający łączny przychód wygenerowany przez koncerty w poszczególnych miastach.

### 3. Analiza liczby koncertów w czasie

Przedstawiono liczbę koncertów w kolejnych miesiącach oraz przeanalizowano wpływ typu obiektu na liczbę organizowanych wydarzeń.

### 4. Analiza cen biletów i przychodów

Wykorzystano histogram do przedstawienia rozkładu cen biletów oraz wykres pudełkowy do porównania przychodów dla różnych typów obiektów.

### 5. Analiza zależności pomiędzy ceną biletu a wypełnieniem obiektu

Obliczono poziom wypełnienia obiektu oraz zbadano zależność pomiędzy ceną biletu a frekwencją na koncertach.

### 6. Wizualizacja danych na mapie

Przygotowano interaktywną mapę Polski przedstawiającą liczbę koncertów oraz średnią cenę biletów w poszczególnych miastach.

### 7. Dashboard podsumowujący

Stworzono zestaw subplotów prezentujących najważniejsze informacje dotyczące rynku koncertowego w Polsce.

## Wnioski

* Najwięcej koncertów organizowanych jest w największych miastach Polski.
* Najwyższe przychody generują koncerty stadionowe oraz festiwale.
* Najwyższe średnie ceny biletów występują na dużych wydarzeniach organizowanych na stadionach.
* Widoczna jest sezonowość rynku koncertowego, szczególnie w okresie wiosenno-letnim.

## Uruchomienie projektu

Instalacja wymaganych bibliotek:

```bash
pip install pandas numpy plotly
```

Uruchomienie programu:

```bash
python zadanie.py
```

## Autor

Ryszard Chojnacki 160757
