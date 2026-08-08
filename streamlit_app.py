import datetime as dt
from typing import Dict, List

import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(
    page_title="Jakość powietrza w Polsce",
    page_icon="🌫️",
    layout="wide",
)

CITY_COORDS: Dict[str, Dict[str, object]] = {
    "Warszawa": {"lat": 52.2297, "lon": 21.0122, "region": "mazowieckie"},
    "Kraków": {"lat": 50.0647, "lon": 19.9450, "region": "małopolskie"},
    "Łódź": {"lat": 51.7592, "lon": 19.4560, "region": "łódzkie"},
    "Wrocław": {"lat": 51.1079, "lon": 17.0385, "region": "dolnośląskie"},
    "Poznań": {"lat": 52.4064, "lon": 16.9252, "region": "wielkopolskie"},
    "Gdańsk": {"lat": 54.3520, "lon": 18.6466, "region": "pomorskie"},
    "Szczecin": {"lat": 53.4285, "lon": 14.5528, "region": "zachodniopomorskie"},
    "Bydgoszcz": {"lat": 53.1235, "lon": 18.0084, "region": "kujawsko-pomorskie"},
    "Lublin": {"lat": 51.2465, "lon": 22.5684, "region": "lubelskie"},
    "Białystok": {"lat": 53.1325, "lon": 23.1688, "region": "podlaskie"},
    "Katowice": {"lat": 50.2649, "lon": 19.0238, "region": "śląskie"},
    "Gdynia": {"lat": 54.5189, "lon": 18.5305, "region": "pomorskie"},
    "Częstochowa": {"lat": 50.8118, "lon": 19.1203, "region": "śląskie"},
    "Radom": {"lat": 51.4027, "lon": 21.1471, "region": "mazowieckie"},
    "Sosnowiec": {"lat": 50.2863, "lon": 19.1041, "region": "śląskie"},
    "Toruń": {"lat": 53.0138, "lon": 18.5984, "region": "kujawsko-pomorskie"},
    "Kielce": {"lat": 50.8661, "lon": 20.6286, "region": "świętokrzyskie"},
    "Rzeszów": {"lat": 50.0412, "lon": 21.9991, "region": "podkarpackie"},
    "Gliwice": {"lat": 50.2945, "lon": 18.6714, "region": "śląskie"},
    "Zabrze": {"lat": 50.3249, "lon": 18.7857, "region": "śląskie"},
    "Olsztyn": {"lat": 53.7784, "lon": 20.4801, "region": "warmińsko-mazurskie"},
    "Bielsko-Biała": {"lat": 49.8224, "lon": 19.0584, "region": "śląskie"},
    "Bytom": {"lat": 50.3484, "lon": 18.9328, "region": "śląskie"},
    "Zielona Góra": {"lat": 51.9356, "lon": 15.5062, "region": "lubuskie"},
    "Rybnik": {"lat": 50.0971, "lon": 18.5418, "region": "śląskie"},
    "Ruda Śląska": {"lat": 50.2558, "lon": 18.8556, "region": "śląskie"},
    "Opole": {"lat": 50.6751, "lon": 17.9213, "region": "opolskie"},
    "Tychy": {"lat": 50.1372, "lon": 18.9664, "region": "śląskie"},
    "Gorzów Wielkopolski": {"lat": 52.7368, "lon": 15.2288, "region": "lubuskie"},
    "Dąbrowa Górnicza": {"lat": 50.3182, "lon": 19.2374, "region": "śląskie"},
    "Elbląg": {"lat": 54.1522, "lon": 19.4088, "region": "warmińsko-mazurskie"},
    "Płock": {"lat": 52.5468, "lon": 19.7064, "region": "mazowieckie"},
    "Wałbrzych": {"lat": 50.7714, "lon": 16.2843, "region": "dolnośląskie"},
    "Włocławek": {"lat": 52.6482, "lon": 19.0678, "region": "kujawsko-pomorskie"},
    "Tarnów": {"lat": 50.0121, "lon": 20.9858, "region": "małopolskie"},
    "Chorzów": {"lat": 50.2976, "lon": 18.9543, "region": "śląskie"},
    "Koszalin": {"lat": 54.1944, "lon": 16.1722, "region": "zachodniopomorskie"},
    "Kalisz": {"lat": 51.7611, "lon": 18.0910, "region": "wielkopolskie"},
    "Legnica": {"lat": 51.2070, "lon": 16.1550, "region": "dolnośląskie"},
    "Grudziądz": {"lat": 53.4841, "lon": 18.7537, "region": "kujawsko-pomorskie"},
    "Jaworzno": {"lat": 50.2053, "lon": 19.2740, "region": "śląskie"},
    "Słupsk": {"lat": 54.4641, "lon": 17.0287, "region": "pomorskie"},
    "Jastrzębie-Zdrój": {"lat": 49.9554, "lon": 18.5748, "region": "śląskie"},
    "Nowy Sącz": {"lat": 49.6218, "lon": 20.6971, "region": "małopolskie"},
    "Jelenia Góra": {"lat": 50.9044, "lon": 15.7194, "region": "dolnośląskie"},
    "Siedlce": {"lat": 52.1677, "lon": 22.2902, "region": "mazowieckie"},
    "Konin": {"lat": 52.2230, "lon": 18.2511, "region": "wielkopolskie"},
    "Piotrków Trybunalski": {"lat": 51.4052, "lon": 19.7030, "region": "łódzkie"},
    "Inowrocław": {"lat": 52.7989, "lon": 18.2630, "region": "kujawsko-pomorskie"},
    "Lubin": {"lat": 51.4008, "lon": 16.2015, "region": "dolnośląskie"},
    "Ostrów Wielkopolski": {"lat": 51.6550, "lon": 17.8069, "region": "wielkopolskie"},

    "Ostrołęka": {"lat": 53.0862, "lon": 21.5753, "region": "mazowieckie"},
    "Nidzica": {"lat": 53.3600, "lon": 20.4270, "region": "warmińsko-mazurskie"},
    "Lidzbark": {"lat": 53.2628, "lon": 19.8266, "region": "warmińsko-mazurskie"},
    "Grajewo": {"lat": 53.6473, "lon": 22.4554, "region": "podlaskie"},
    "Mikołajki": {"lat": 53.8020, "lon": 21.5711, "region": "warmińsko-mazurskie"},
    "Czaplinek": {"lat": 53.5585, "lon": 16.2332, "region": "zachodniopomorskie"},
    "Bytów": {"lat": 54.1706, "lon": 17.4919, "region": "pomorskie"},
    "Zamość": {"lat": 50.7231, "lon": 23.2519, "region": "lubelskie"},
    "Krosno": {"lat": 49.6884, "lon": 21.7700, "region": "podkarpackie"},
    "Lesko": {"lat": 49.4701, "lon": 22.3304, "region": "podkarpackie"},
    "Ustrzyki Górne": {"lat": 49.1054, "lon": 22.6332, "region": "podkarpackie"},
    "Lubaczów": {"lat": 50.1570, "lon": 23.1234, "region": "podkarpackie"},
    "Tarnobrzeg": {"lat": 50.5734, "lon": 21.6794, "region": "podkarpackie"},
    "Leszno": {"lat": 51.8403, "lon": 16.5749, "region": "wielkopolskie"},

    "Płońsk": {"lat": 52.6235, "lon": 20.3755, "region": "mazowieckie"},
    "Pułtusk": {"lat": 52.7025, "lon": 21.0828, "region": "mazowieckie"},
    "Tłuszcz": {"lat": 52.4305, "lon": 21.4358, "region": "mazowieckie"},
}

POLLUTANTS = {
    "PM10": "pm10",
    "PM2.5": "pm2_5",
    "NO₂": "nitrogen_dioxide",
    "O₃": "ozone",
    "SO₂": "sulphur_dioxide",
    "CO": "carbon_monoxide",
}

NICE_NAMES = {v: k for k, v in POLLUTANTS.items()}


def format_number(value: float, suffix: str = "") -> str:
    if pd.isna(value):
        return "brak danych"
    return f"{value:,.1f}".replace(",", " ").replace(".", ",") + suffix


@st.cache_data(ttl=60 * 60)
def get_air_quality(city: str, start_date: dt.date, end_date: dt.date) -> pd.DataFrame:
    """Pobiera dane godzinowe Open-Meteo Air Quality dla jednego miasta."""
    meta = CITY_COORDS[city]
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": meta["lat"],
        "longitude": meta["lon"],
        "hourly": ",".join(POLLUTANTS.values()),
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "timezone": "Europe/Warsaw",
    }
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()
    hourly = data.get("hourly", {})
    if not hourly or "time" not in hourly:
        return pd.DataFrame()

    df = pd.DataFrame(hourly)
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df["city"] = city
    df["region"] = meta["region"]
    df["lat"] = float(meta["lat"])
    df["lon"] = float(meta["lon"])
    return df


@st.cache_data(ttl=60 * 60)
def load_data(cities: List[str], start_date: dt.date, end_date: dt.date) -> pd.DataFrame:
    frames = []
    errors = []
    for city in cities:
        try:
            city_df = get_air_quality(city, start_date, end_date)
            if not city_df.empty:
                frames.append(city_df)
        except Exception as exc:
            errors.append(f"{city}: {exc}")
    if errors:
        st.warning("Nie udało się pobrać części danych: " + "; ".join(errors[:3]))
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Czyszczenie i przygotowanie danych do analizy."""
    df = df.copy()
    df = df.dropna(subset=["time", "city"])

    for col in POLLUTANTS.values():
        df[col] = pd.to_numeric(df[col], errors="coerce")
        # Wartości ujemne w danych jakości powietrza traktujemy jako błędne.
        df.loc[df[col] < 0, col] = np.nan

    df["date"] = df["time"].dt.date
    df["hour"] = df["time"].dt.hour
    df["day_name"] = df["time"].dt.day_name()
    df["pm_ratio"] = df["pm2_5"] / df["pm10"]
    df["air_quality_level"] = pd.cut(
        df["pm10"],
        bins=[-np.inf, 20, 50, 100, np.inf],
        labels=["niski", "umiarkowany", "wysoki", "bardzo wysoki"],
    )
    return df


st.title("🌫️ Dashboard jakości powietrza w polskich miastach")
st.caption("Dane godzinowe z Open-Meteo Air Quality API. Aplikacja pobiera dane na żywo, czyści je i przelicza wizualizacje po zmianie filtrów.")

with st.sidebar:
    st.header("Filtry")
    today = dt.date.today()
    default_start = today - dt.timedelta(days=14)
    date_range = st.date_input(
        "Zakres dat",
        value=(default_start, today),
        max_value=today,
    )

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = default_start, today

    all_regions = sorted({str(v["region"]) for v in CITY_COORDS.values()})
    selected_regions = st.multiselect("Województwa", all_regions, default=all_regions)

    cities_for_regions = [
        city for city, meta in CITY_COORDS.items() if meta["region"] in selected_regions
    ]
    selected_cities = st.multiselect(
        "Miasta",
        sorted(cities_for_regions),
        default=sorted(cities_for_regions),
    )

    pollutant_label = st.selectbox("Główne zanieczyszczenie", list(POLLUTANTS.keys()), index=0)
    pollutant = POLLUTANTS[pollutant_label]

    min_value = st.slider("Minimalna wartość głównego wskaźnika", 0, 200, 0, 5)
    show_table = st.checkbox("Pokaż tabelę danych", value=False)

if start_date > end_date:
    st.error("Data początkowa nie może być późniejsza niż data końcowa.")
    st.stop()

if not selected_cities:
    st.error("Wybierz co najmniej jedno miasto.")
    st.stop()

raw_df = load_data(selected_cities, start_date, end_date)
if raw_df.empty:
    st.error("Nie udało się pobrać danych. Sprawdź połączenie internetowe albo wybierz krótszy zakres dat.")
    st.stop()

df = clean_data(raw_df)
df = df[df[pollutant].fillna(-1) >= min_value]

if df.empty:
    st.warning("Po zastosowaniu filtrów nie ma danych do pokazania.")
    st.stop()

latest_time = df["time"].max()
latest_df = df[df["time"] == latest_time]

avg_value = df[pollutant].mean()
max_row = df.loc[df[pollutant].idxmax()]
records_count = len(df)
city_count = df["city"].nunique()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric(f"Średnie {pollutant_label}", format_number(avg_value, " µg/m³"))
kpi2.metric("Maksimum", format_number(max_row[pollutant], " µg/m³"), f"{max_row['city']}")
kpi3.metric("Liczba obserwacji", f"{records_count:,}".replace(",", " "))
kpi4.metric("Liczba miast", city_count)

st.divider()

tab_map, tab_time, tab_compare, tab_distribution, tab_data = st.tabs(
    ["Mapa", "Czas", "Porównania", "Rozkłady", "Dane"]
)

with tab_map:
    st.subheader("Mapa aktualnych wartości")
    map_df = latest_df.groupby(["city", "region", "lat", "lon"], as_index=False)[pollutant].mean()
    fig_map = px.scatter_mapbox(
        map_df,
        lat="lat",
        lon="lon",
        color=pollutant,
        size=pollutant,
        hover_name="city",
        hover_data={"region": True, pollutant: ":.1f", "lat": False, "lon": False},
        zoom=4.8,
        height=560,
        title=f"{pollutant_label} — ostatni dostępny pomiar ({latest_time:%Y-%m-%d %H:%M})",
        mapbox_style="open-street-map",
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.info("Wniosek: mapa pozwala szybko porównać poziom zanieczyszczeń między miastami i wskazać lokalne różnice.")

with tab_time:
    st.subheader("Zmiany w czasie")
    daily = df.groupby(["date", "city"], as_index=False)[pollutant].mean()
    fig_line = px.line(
        daily,
        x="date",
        y=pollutant,
        color="city",
        markers=True,
        title=f"Średnie dzienne {pollutant_label} w wybranych miastach",
        labels={"date": "Data", pollutant: f"{pollutant_label} [µg/m³]", "city": "Miasto"},
    )
    st.plotly_chart(fig_line, use_container_width=True)

    hourly = df.groupby("hour", as_index=False)[pollutant].mean()
    fig_bar = px.bar(
        hourly,
        x="hour",
        y=pollutant,
        title=f"Średni poziom {pollutant_label} według godziny doby",
        labels={"hour": "Godzina", pollutant: f"{pollutant_label} [µg/m³]"},
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.info("Wniosek: wykres godzinowy pokazuje, w których porach dnia zanieczyszczenie jest przeciętnie najwyższe.")

with tab_compare:
    st.subheader("Porównanie miast i zależności")
    ranking = df.groupby("city", as_index=False)[pollutant].mean().sort_values(pollutant, ascending=False)
    fig_ranking = px.bar(
        ranking,
        x="city",
        y=pollutant,
        title=f"Ranking miast według średniego {pollutant_label}",
        labels={"city": "Miasto", pollutant: f"{pollutant_label} [µg/m³]"},
    )
    st.plotly_chart(fig_ranking, use_container_width=True)
    st.info(
        "Wniosek: ranking pozwala zidentyfikować miasta o najwyższym średnim poziomie zanieczyszczeń oraz wskazać obszary wymagające większej uwagi."
    )

    scatter_df = df.dropna(subset=["pm10", "pm2_5"])
    fig_scatter = px.scatter(
        scatter_df,
        x="pm10",
        y="pm2_5",
        color="city",
        size=pollutant,
        hover_data=["time", "region"],
        title="Zależność PM10 i PM2.5",
        labels={"pm10": "PM10 [µg/m³]", "pm2_5": "PM2.5 [µg/m³]", "city": "Miasto"},
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.info(
        "Wniosek: silna dodatnia zależność PM10 i PM2.5 sugeruje wspólne źródła emisji, takie jak transport lub ogrzewanie budynków."
    )

    corr_cols = list(POLLUTANTS.values())
    corr = df[corr_cols].corr(numeric_only=True)
    fig_heatmap = px.imshow(
        corr,
        text_auto=True,
        title="Heatmapa korelacji między zanieczyszczeniami",
        labels={"color": "Korelacja"},
        x=[NICE_NAMES.get(c, c) for c in corr.columns],
        y=[NICE_NAMES.get(c, c) for c in corr.index],
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    st.info(
        "Wniosek: analiza korelacji pozwala określić, które zanieczyszczenia najczęściej występują jednocześnie i mogą mieć wspólne źródło emisji."
    )

with tab_distribution:
    st.subheader("Rozkład wartości")
    fig_hist = px.histogram(
        df,
        x=pollutant,
        color="city",
        nbins=30,
        title=f"Histogram wartości {pollutant_label}",
        labels={pollutant: f"{pollutant_label} [µg/m³]", "city": "Miasto"},
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    fig_box = px.box(
        df,
        x="city",
        y=pollutant,
        points="outliers",
        title=f"Boxplot wartości {pollutant_label} według miasta",
        labels={"city": "Miasto", pollutant: f"{pollutant_label} [µg/m³]"},
    )
    st.plotly_chart(fig_box, use_container_width=True)
    st.info("Wniosek: boxplot pokazuje nie tylko średni poziom, ale też rozrzut i wartości odstające dla miast.")

with tab_data:
    st.subheader("Czyszczenie i dane")
    st.markdown(
        """
        W aplikacji wykonano przygotowanie danych: konwersję czasu do typu daty, konwersję kolumn liczbowych,
        oznaczenie wartości ujemnych jako braków, utworzenie kolumn pochodnych: data, godzina, udział PM2.5 w PM10
        oraz kategoria poziomu PM10.
        """
    )
    summary = df.groupby("city")[list(POLLUTANTS.values())].agg(["mean", "min", "max"]).round(2)
    st.dataframe(summary, use_container_width=True)

    if show_table:
        preview_cols = ["time", "city", "region"] + list(POLLUTANTS.values()) + ["pm_ratio", "air_quality_level"]
        st.dataframe(df[preview_cols].sort_values("time", ascending=False), use_container_width=True)

st.caption("Źródło danych: Open-Meteo Air Quality API. Jednostki większości zanieczyszczeń: µg/m³. Projekt edukacyjny.")
