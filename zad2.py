import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ======================================
# GENEROWANIE BRUDNYCH DANYCH
# ======================================

np.random.seed(42)

n = 500

klienci = [
    "Anna Kowalska", "  Jan Nowak", "Anna Kowalska", "PIOTR WIŚNIEWSKI",
    "katarzyna lewandowska", "Tomasz Zieliński ", "Marta Wójcik",
    "anna kowalska ", "Krzysztof Kamiński", " Magdalena Dąbrowska"
]

produkty = [
    "Laptop", "Mysz", "Klawiatura", "Monitor", "laptop", "MYSZ",
    "Słuchawki", "Pendrive", "monitor", "Webcam"
]

kategorie = [
    "Elektronika", "elektronika", "ELEKTRONIKA", "Akcesoria",
    "akcesoria", "Akcesoria "
]

miasta = [
    "Warszawa", "Kraków", "warszawa", "Gdańsk", "WROCŁAW",
    "Poznań", "Łódź ", " Warszawa", "kraków"
]

start_date = datetime(2025, 1, 1)

daty_iso = [
    (start_date + timedelta(days=int(d))).strftime("%Y-%m-%d")
    for d in np.random.randint(0, 300, n // 2)
]

daty_pl = [
    (start_date + timedelta(days=int(d))).strftime("%d.%m.%Y")
    for d in np.random.randint(0, 300, n // 2)
]

daty = daty_iso + daty_pl
np.random.shuffle(daty)

df = pd.DataFrame({
    "order_id": range(1001, 1001 + n),
    "klient": np.random.choice(klienci, n),
    "produkt": np.random.choice(produkty, n),
    "kategoria": np.random.choice(kategorie, n),
    "miasto": np.random.choice(miasta, n),
    "ilosc": np.random.choice([1, 2, 3, 5, -1, 0], n, p=[0.5, 0.2, 0.15, 0.1, 0.025, 0.025]),
    "cena_jednostkowa": np.random.choice(
        ["199.99", "299,99", "1 499.00", "89.50", "2999", "399.00 zł", None, "abc"],
        n
    ),
    "data_zamowienia": daty,
    "email": np.random.choice(
        [
            "anna@gmail.com", "JAN@WP.PL", "piotr.w@onet",
            "marta@gmail.com", "tomasz@interia.pl", None,
            "krzysztof.k@gmail.com", "brak"
        ],
        n
    )
})

for col in ["miasto", "kategoria", "data_zamowienia"]:
    df.loc[df.sample(frac=0.05, random_state=1).index, col] = np.nan

df = pd.concat([df, df.sample(20, random_state=2)], ignore_index=True)

df.to_csv("zamowienia_messy.csv", index=False)

# ======================================
# CZĘŚĆ 1 — EKSPLORACJA
# ======================================

df = pd.read_csv("zamowienia_messy.csv")

print("Rozmiar danych:")
print(df.shape)

print("\nPierwsze wiersze:")
print(df.head())

print("\nInformacje o danych:")
print(df.info())

print("\nStatystyki:")
print(df.describe(include="all"))

print("\nBraki danych:")
print(df.isnull().sum())

print("\nKategorie produktów:")
print(df["produkt"].value_counts())

print("\nKategorie:")
print(df["kategoria"].value_counts())

print("\nMiasta:")
print(df["miasto"].value_counts())

print("""
Problemy zauważone w danych:
1. Występują brakujące wartości w kolumnach miasto, kategoria, data_zamowienia i email.
2. W danych znajdują się duplikaty wierszy.
3. Daty są zapisane w dwóch różnych formatach.
4. Kategorie, miasta i produkty mają różną wielkość liter oraz dodatkowe spacje.
5. Kolumna cena_jednostkowa zawiera tekst, przecinki, spacje, znak zł oraz błędne wartości typu abc.
6. W kolumnie ilosc występują wartości 0 i -1, które są błędne dla zamówień.
7. Niektóre adresy email są niepoprawne.
""")

# ======================================
# CZĘŚĆ 2 — CZYSZCZENIE
# ======================================

df = df.drop_duplicates()

df["klient"] = df["klient"].str.strip().str.title()
df["produkt"] = df["produkt"].str.strip().str.title()
df["miasto"] = df["miasto"].str.strip().str.title()
df["kategoria"] = df["kategoria"].str.strip().str.lower()

df["data_zamowienia"] = pd.to_datetime(
    df["data_zamowienia"],
    errors="coerce",
    format="mixed"
)

df["cena_jednostkowa"] = (
    df["cena_jednostkowa"]
    .astype(str)
    .str.replace("zł", "", regex=False)
    .str.replace(" ", "", regex=False)
    .str.replace(",", ".", regex=False)
)

df["cena_jednostkowa"] = pd.to_numeric(
    df["cena_jednostkowa"],
    errors="coerce"
)

df = df.dropna(subset=["cena_jednostkowa", "data_zamowienia"])

df["miasto"] = df["miasto"].fillna("Unknown")
df["kategoria"] = df["kategoria"].fillna("unknown")
df["email"] = df["email"].fillna("brak_emaila")

df = df[df["ilosc"] > 0]

# ======================================
# CZĘŚĆ 3 — TRANSFORMACJE
# ======================================

df["wartosc_zamowienia"] = df["ilosc"] * df["cena_jednostkowa"]

df["rok"] = df["data_zamowienia"].dt.year
df["miesiac"] = df["data_zamowienia"].dt.month
df["nazwa_dnia"] = df["data_zamowienia"].dt.day_name()

df["email_poprawny"] = df["email"].str.match(
    r"^[\w\.-]+@[\w\.-]+\.\w+$",
    na=False
)

# ======================================
# CZĘŚĆ 4 — ANALIZA
# ======================================

wartosc_miesiac = (
    df.groupby("miesiac")["wartosc_zamowienia"]
    .sum()
    .sort_index()
)

print("\nŁączna wartość zamówień w każdym miesiącu:")
print(wartosc_miesiac)

top_klienci = (
    df.groupby("klient")["wartosc_zamowienia"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print("\nTop 5 klientów:")
print(top_klienci)

srednia_kategoria = (
    df.groupby("kategoria")["wartosc_zamowienia"]
    .mean()
)

print("\nŚrednia wartość zamówienia w każdej kategorii:")
print(srednia_kategoria)

# ======================================
# CZĘŚĆ 5 — WYKRES
# ======================================

plt.figure(figsize=(10, 5))
plt.bar(wartosc_miesiac.index.astype(str), wartosc_miesiac.values)
plt.title("Łączna wartość zamówień w każdym miesiącu")
plt.xlabel("Miesiąc")
plt.ylabel("Wartość zamówień")
plt.tight_layout()
plt.show()

# ======================================
# CZĘŚĆ 6 — ZAPIS
# ======================================

df.to_csv("zamowienia_clean.csv", index=False)

print("\nZapisano oczyszczone dane do pliku zamowienia_clean.csv")

input("Naciśnij Enter, aby zakończyć...")
