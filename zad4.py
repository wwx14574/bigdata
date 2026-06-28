import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Domyślny jasny szablon wykresów
import plotly.io as pio
pio.templates.default = "plotly_white"


# Część 1 - Wczytanie i eksploracja danych
# Wczytanie danych z pliku CSV oraz sprawdzenie podstawowych informacji o zbiorze danych.


df = pd.read_csv("koncerty_polska.csv", parse_dates=["data"])

print("Shape:", df.shape)
print(df.head())
print(df.dtypes)

print("Liczba unikalnych miast:", df["miasto"].nunique())
print("Liczba unikalnych gatunków:", df["gatunek"].nunique())


# Część 2 - Łączny przychód według miasta
# Analiza przychodów generowanych przez koncerty w poszczególnych miastach.

przychod_miasto = (
    df.groupby("miasto", as_index=False)["przychod_pln"]
    .sum()
    .sort_values("przychod_pln", ascending=False)
)

fig = px.bar(
    przychod_miasto,
    x="miasto",
    y="przychod_pln",
    title="Łączny przychód z koncertów według miasta",
    labels={"miasto": "Miasto", "przychod_pln": "Łączny przychód [PLN]"},
    text_auto=",.0f"
)
fig.update_layout(xaxis_tickangle=-35, height=500)
fig.show()

# Część 3 - Analiza liczby koncertów w czasie
# Sprawdzenie zmian liczby koncertów w kolejnych miesiącach oraz podział według typu obiektu.

df["miesiac"] = df["data"].dt.to_period("M").astype(str)

koncerty_miesiac = (
    df.groupby("miesiac", as_index=False)
    .size()
    .rename(columns={"size": "liczba_koncertow"})
)

fig = px.line(
    koncerty_miesiac,
    x="miesiac",
    y="liczba_koncertow",
    markers=True,
    title="Liczba koncertów w poszczególnych miesiącach",
    labels={"miesiac": "Miesiąc", "liczba_koncertow": "Liczba koncertów"}
)
fig.update_layout(height=500)
fig.show()


koncerty_miesiac_typ = (
    df.groupby(["miesiac", "typ_obiektu"], as_index=False)
    .size()
    .rename(columns={"size": "liczba_koncertow"})
)

fig = px.line(
    koncerty_miesiac_typ,
    x="miesiac",
    y="liczba_koncertow",
    color="typ_obiektu",
    markers=True,
    title="Miesięczna liczba koncertów według typu obiektu",
    labels={
        "miesiac": "Miesiąc",
        "liczba_koncertow": "Liczba koncertów",
        "typ_obiektu": "Typ obiektu"
    }
)
fig.update_layout(height=550)
fig.show()

# Część 4 - Histogram cen i boxplot przychodów
# Analiza rozkładu cen biletów oraz porównanie przychodów dla różnych typów obiektów.

fig = px.histogram(
    df,
    x="cena_biletu_pln",
    nbins=50,
    title="Rozkład cen biletów",
    labels={"cena_biletu_pln": "Cena biletu [PLN]", "count": "Liczba koncertów"}
)
fig.update_layout(height=500)
fig.show()

# %%
fig = px.box(
    df,
    x="typ_obiektu",
    y="przychod_pln",
    title="Przychód z koncertów według typu obiektu",
    labels={"typ_obiektu": "Typ obiektu", "przychod_pln": "Przychód [PLN]"}
)
fig.update_layout(height=500)
fig.show()

# Część 5 - Cena biletu a wypełnienie obiektu
# Sprawdzenie zależności pomiędzy ceną biletu a poziomem zapełnienia obiektu.

df["wypelnienie"] = df["bilety_sprzedane"] / df["pojemnosc"]

fig = px.scatter(
    df,
    x="cena_biletu_pln",
    y="wypelnienie",
    color="gatunek",
    size="pojemnosc",
    hover_data=["miasto", "typ_obiektu"],
    title="Cena biletu a wypełnienie sali",
    labels={
        "cena_biletu_pln": "Cena biletu [PLN]",
        "wypelnienie": "Wypełnienie sali",
        "gatunek": "Gatunek",
        "pojemnosc": "Pojemność"
    }
)
fig.update_layout(height=600)
fig.show()



# Część 6 - Mapa koncertów w Polsce
# Wizualizacja liczby koncertów i średnich cen biletów w poszczególnych miastach.

miasta_agregacja = (
    df.groupby(["miasto", "latitude", "longitude"], as_index=False)
    .agg(
        srednia_cena_biletu=("cena_biletu_pln", "mean"),
        liczba_koncertow=("event_id", "count"),
        laczny_przychod=("przychod_pln", "sum")
    )
)

fig = px.scatter_mapbox(
    miasta_agregacja,
    lat="latitude",
    lon="longitude",
    size="liczba_koncertow",
    color="srednia_cena_biletu",
    hover_name="miasto",
    hover_data={
        "srednia_cena_biletu": ":.2f",
        "liczba_koncertow": True,
        "laczny_przychod": ":,.0f",
        "latitude": False,
        "longitude": False
    },
    zoom=5,
    center={"lat": 52, "lon": 19},
    mapbox_style="open-street-map",
    height=600,
    title="Mapa koncertów w Polsce"
)
fig.show()

# Część 7 - Subploty podsumowujące analizę
# Zestawienie najważniejszych wykresów w jednej figurze.

przychod_miasto = df.groupby("miasto", as_index=False)["przychod_pln"].sum().sort_values("przychod_pln", ascending=False)
koncerty_gatunek = df.groupby("gatunek", as_index=False).size().rename(columns={"size": "liczba_koncertow"}).sort_values("liczba_koncertow", ascending=False)

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Przychód według miasta",
        "Liczba koncertów według gatunku",
        "Histogram cen biletów",
        "Wypełnienie według typu obiektu"
    )
)

fig.add_trace(go.Bar(x=przychod_miasto["miasto"], y=przychod_miasto["przychod_pln"], name="Przychód"), row=1, col=1)
fig.add_trace(go.Bar(x=koncerty_gatunek["gatunek"], y=koncerty_gatunek["liczba_koncertow"], name="Liczba koncertów"), row=1, col=2)
fig.add_trace(go.Histogram(x=df["cena_biletu_pln"], nbinsx=50, name="Cena biletu"), row=2, col=1)

for typ in sorted(df["typ_obiektu"].unique()):
    fig.add_trace(
        go.Box(y=df.loc[df["typ_obiektu"] == typ, "wypelnienie"], name=typ),
        row=2, col=2
    )

fig.update_layout(
    title_text="Podsumowanie rynku koncertów muzycznych w Polsce",
    height=850,
    showlegend=False
)
fig.update_xaxes(tickangle=-35, row=1, col=1)
fig.update_xaxes(tickangle=-35, row=1, col=2)
fig.show()

# Część 8 - Wnioski
# Podsumowanie wyników przeprowadzonej analizy rynku koncertowego w Polsce.

# 1. Największy łączny przychód osiąga **Warszawa**, ponieważ ma najwięcej koncertów i największy potencjał rynku.
# 2. Najwyższe przychody generują przede wszystkim **stadiony** i **festiwale**, bo mają największą pojemność oraz wyższe ceny biletów.
# 3. W danych widać zróżnicowanie cen między typami obiektów — wydarzenia stadionowe i arenowe są zazwyczaj droższe niż koncerty klubowe.
# 4. Liczba koncertów zmienia się w czasie, więc można zauważyć sezonowość i miesiące z większą liczbą wydarzeń.
# 5. Sama cena biletu nie decyduje jednoznacznie o wypełnieniu sali — droższe koncerty także mogą mieć wysoką frekwencję.