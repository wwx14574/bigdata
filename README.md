# Dashboard jakości powietrza w polskich miastach

## Opis projektu

Projekt jest aplikacją analityczną przygotowaną w Streamlit. Dashboard pobiera rzeczywiste dane godzinowe z Open-Meteo Air Quality API, czyści je, analizuje i prezentuje w formie interaktywnych wykresów.

Aplikacja pozwala porównywać jakość powietrza w wybranych polskich miastach, sprawdzać zmiany w czasie, analizować rozkład wartości oraz zależności między zanieczyszczeniami.

## Źródło danych

Dane pochodzą z publicznego API:

https://air-quality-api.open-meteo.com/v1/air-quality

W projekcie wykorzystano dane dla wybranych polskich miast, m.in. Warszawy, Krakowa, Wrocławia, Poznania, Gdańska, Łodzi i Katowic.

Pobierane wskaźniki:

- PM10
- PM2.5
- NO2
- O3
- SO2
- CO

## Funkcje aplikacji

Aplikacja zawiera:

- pobieranie danych z prawdziwego źródła przez API,
- czyszczenie i przygotowanie danych,
- obsługę braków i błędnych wartości,
- kolumny pochodne, np. data, godzina, udział PM2.5 w PM10,
- KPI z najważniejszymi informacjami,
- interaktywne filtry w panelu bocznym,
- minimum 5 typów wykresów:
  - mapa,
  - wykres liniowy,
  - wykres słupkowy,
  - scatter plot,
  - histogram,
  - boxplot,
  - heatmapa korelacji.

## Filtry

W aplikacji dostępne są filtry:

- zakres dat,
- województwo,
- miasto,
- rodzaj zanieczyszczenia,
- minimalna wartość wskaźnika.

Po zmianie filtrów aplikacja automatycznie przelicza wykresy, KPI i tabele.

## Struktura projektu

```text
.
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Uruchomienie lokalne

1. Sklonuj repozytorium lub pobierz pliki projektu.
2. Zainstaluj wymagane pakiety:

```bash
pip install -r requirements.txt
```

3. Uruchom aplikację:

```bash
streamlit run app.py
```

4. Otwórz aplikację w przeglądarce pod adresem wyświetlonym w terminalu, zwykle:

```text
http://localhost:8501
```

## Autor

Ryszard Chojnacki 160757
