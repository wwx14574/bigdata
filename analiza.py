import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("mieszkania_warszawa.csv")

print("\nCZĘŚĆ 1 — WSTĘPNA EKSPLORACJA\n")

print("Shape:")
print(df.shape)

print("\nInfo:")
df.info()

print("\nDescribe:")
print(df.describe())

print("\nBraki danych:")
print(df.isnull().sum())

print("""
Komentarz do części 1:
W statystykach opisowych widać podejrzane wartości. Maksymalna cena mieszkania
jest bardzo wysoka względem mediany, co może oznaczać obecność outlierów.
Maksymalny metraż jest znacznie większy od typowego mieszkania. W danych mogą
też występować nielogiczne lata budowy, np. przed 1900 rokiem lub po 2026 roku.
""")


print("\nCZĘŚĆ 2 — STATYSTYKI OPISOWE\n")

print("Statystyki dla cena_pln:")
print("Średnia:", df["cena_pln"].mean())
print("Mediana:", df["cena_pln"].median())
print("Odchylenie standardowe:", df["cena_pln"].std())
print("Skewness:", df["cena_pln"].skew())
print("Kurtosis:", df["cena_pln"].kurtosis())

print("""
Komentarz:
Dodatni skewness oznacza, że rozkład ceny jest skośny w prawo.
Większość ofert ma ceny z niższego lub średniego zakresu, ale pojedyncze
bardzo drogie mieszkania wydłużają prawy ogon rozkładu.
""")

Q1 = df["metraz_m2"].quantile(0.25)
Q3 = df["metraz_m2"].quantile(0.75)
IQR = Q3 - Q1

print("Q1 metraż:", Q1)
print("Q3 metraż:", Q3)
print("IQR metraż:", IQR)

print("\nLiczba unikalnych dzielnic:")
print(df["dzielnica"].nunique())

print("\nLiczba ofert w każdej dzielnicy:")
print(df["dzielnica"].value_counts())


print("\nCZĘŚĆ 3 — ANALIZA POJEDYNCZYCH ZMIENNYCH\n")

plt.figure(figsize=(10, 5))
sns.histplot(df["cena_pln"], kde=True, bins=50)
plt.title("Wykres 1. Histogram i KDE ceny mieszkań")
plt.xlabel("Cena [PLN]")
plt.ylabel("Liczba ofert")


print("""
Komentarz do Wykresu 1:
Histogram cen mieszkań pokazuje wyraźną prawostronną skośność rozkładu.
Większość ofert znajduje się w niższym zakresie cenowym, natomiast pojedyncze
bardzo drogie mieszkania tworzą długi ogon po prawej stronie wykresu.
""")
plt.show()



plt.figure(figsize=(10, 5))
sns.histplot(df["metraz_m2"], kde=True, bins=50)
plt.title("Wykres 2. Histogram i KDE metrażu mieszkań")
plt.xlabel("Metraż [m2]")
plt.ylabel("Liczba ofert")


print("""
Komentarz do Wykresu 2:
Histogram metrażu również pokazuje skośność prawostronną. Większość mieszkań
ma typowy metraż, ale pojawiają się pojedyncze bardzo duże wartości,
które mogą być outlierami.
""")
plt.show()


plt.figure(figsize=(10, 4))
sns.boxplot(x=df["cena_pln"])
plt.title("Wykres 3. Boxplot ceny mieszkań")
plt.xlabel("Cena [PLN]")


print("""
Komentarz do Wykresu 3:
Na boxplocie ceny widać wiele punktów odstających poza wąsami wykresu.
Szczególnie widoczne są bardzo wysokie ceny, które mogą oznaczać luksusowe
nieruchomości albo błędnie wprowadzone dane.
""")
plt.show()


order = df["dzielnica"].value_counts().index

plt.figure(figsize=(12, 5))
sns.countplot(data=df, x="dzielnica", order=order)
plt.title("Wykres 4. Liczba ofert według dzielnicy")
plt.xlabel("Dzielnica")
plt.ylabel("Liczba ofert")
plt.xticks(rotation=45)
plt.tight_layout()


print("""
Komentarz do Wykresu 4:
Wykres pokazuje, ile ofert przypada na każdą dzielnicę. Dzielnice zostały
posortowane malejąco według liczby ofert, dzięki czemu łatwo porównać,
gdzie w zbiorze znajduje się najwięcej ogłoszeń.
""")
plt.show()


print("\nCZĘŚĆ 4 — ANALIZA ZALEŻNOŚCI\n")

df_corr = df.copy()
df_corr["ma_balkon"] = df_corr["ma_balkon"].astype(int)
df_corr["ma_miejsce_parkingowe"] = df_corr["ma_miejsce_parkingowe"].astype(int)

corr = df_corr.select_dtypes(include="number").corr()

plt.figure(figsize=(12, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Wykres 5. Macierz korelacji zmiennych numerycznych")
plt.tight_layout()


print("\nKorelacja zmiennych z ceną:")
print(corr["cena_pln"].sort_values(ascending=False))

najsilniejsza = corr["cena_pln"].drop("cena_pln").abs().sort_values(ascending=False).index[0]

print("\nZmienna najsilniej korelująca z ceną:")
print(najsilniejsza)

print("""
Komentarz do Wykresu 5:
Macierz korelacji pokazuje zależności między zmiennymi numerycznymi.
Najsilniejsza korelacja z ceną występuje zwykle dla metrażu, ponieważ większe
mieszkania naturalnie mają wyższą cenę całkowitą.
""")
plt.show()


plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="metraz_m2", y="cena_pln", hue="dzielnica", alpha=0.7)
plt.title("Wykres 6. Zależność metrażu od ceny")
plt.xlabel("Metraż [m2]")
plt.ylabel("Cena [PLN]")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()


print("""
Komentarz do Wykresu 6:
Scatter plot pokazuje zależność między metrażem a ceną. Ogólnie większe
mieszkania mają wyższe ceny, ale widoczne są też punkty odstające,
czyli oferty o nietypowo wysokiej cenie lub bardzo dużym metrażu.
""")
plt.show()


df["cena_pln_per_m2"] = df["cena_pln"] / df["metraz_m2"]

mediany_m2 = df.groupby("dzielnica")["cena_pln_per_m2"].median().sort_values(ascending=False)

plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="dzielnica", y="cena_pln_per_m2", order=mediany_m2.index)
plt.title("Wykres 7. Cena za m2 według dzielnicy")
plt.xlabel("Dzielnica")
plt.ylabel("Cena za m2 [PLN]")
plt.xticks(rotation=45)
plt.tight_layout()


print("\nMediana ceny za m2 według dzielnicy:")
print(mediany_m2)

print("\nDzielnica z najwyższą medianą ceny za m2:")
print(mediany_m2.index[0])

print("""
Komentarz do Wykresu 7:
Cena za m2 pozwala lepiej porównywać dzielnice niż sama cena całkowita.
Na wykresie można zauważyć, które dzielnice mają najwyższe typowe ceny
za metr kwadratowy.
""")
plt.show()

print("\nCZĘŚĆ 5 — DETEKCJA OUTLIERÓW\n")

Q1_cena = df["cena_pln"].quantile(0.25)
Q3_cena = df["cena_pln"].quantile(0.75)
IQR_cena = Q3_cena - Q1_cena

dolna_granica = Q1_cena - 1.5 * IQR_cena
gorna_granica = Q3_cena + 1.5 * IQR_cena

outliers_iqr = df[
    (df["cena_pln"] < dolna_granica) |
    (df["cena_pln"] > gorna_granica)
]

z_score = (df["cena_pln"] - df["cena_pln"].mean()) / df["cena_pln"].std()
outliers_z = df[np.abs(z_score) > 3]

mediana_ceny = df["cena_pln"].median()
mad = np.median(np.abs(df["cena_pln"] - mediana_ceny))
modified_z_score = 0.6745 * (df["cena_pln"] - mediana_ceny) / mad
outliers_modified_z = df[np.abs(modified_z_score) > 3.5]

print("Liczba outlierów ceny metodą IQR:", len(outliers_iqr))
print("Liczba outlierów ceny metodą Z-score:", len(outliers_z))
print("Liczba outlierów ceny metodą Modified Z-score:", len(outliers_modified_z))

Q1_m = df["metraz_m2"].quantile(0.25)
Q3_m = df["metraz_m2"].quantile(0.75)
IQR_m = Q3_m - Q1_m

dolna_m = Q1_m - 1.5 * IQR_m
gorna_m = Q3_m + 1.5 * IQR_m

outliers_metraz = df[
    (df["metraz_m2"] < dolna_m) |
    (df["metraz_m2"] > gorna_m)
]

print("\nLiczba outlierów metrażu metodą IQR:", len(outliers_metraz))

print("\nTop 5 największych metraży:")
print(df.sort_values("metraz_m2", ascending=False).head(5))

bledne_lata = df[
    (df["rok_budowy"] < 1900) |
    (df["rok_budowy"] > 2026)
]

print("\nWiersze z błędnymi latami budowy:")
print(bledne_lata)


print("\nCZĘŚĆ 6 — DECYZJA I CZYSZCZENIE\n")

df_clean = df[
    (df["rok_budowy"] >= 1900) &
    (df["rok_budowy"] <= 2026)
].copy()

p1 = df_clean["cena_pln"].quantile(0.01)
p99 = df_clean["cena_pln"].quantile(0.99)

df_clean["cena_pln_capped"] = df_clean["cena_pln"].clip(lower=p1, upper=p99)
df_clean["cena_pln_log"] = np.log1p(df_clean["cena_pln"])

print("Liczba wierszy przed czyszczeniem:", len(df))
print("Liczba wierszy po usunięciu błędnych lat:", len(df_clean))
print("1 percentyl ceny:", p1)
print("99 percentyl ceny:", p99)

print("\nSkewness przed transformacją log:", df_clean["cena_pln"].skew())
print("Skewness po transformacji log1p:", df_clean["cena_pln_log"].skew())

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.histplot(df_clean["cena_pln"], kde=True, bins=50)
plt.title("Wykres 8. Cena przed transformacją log")
plt.xlabel("Cena [PLN]")

plt.subplot(1, 2, 2)
sns.histplot(df_clean["cena_pln_log"], kde=True, bins=50)
plt.title("Wykres 9. Cena po transformacji log1p")
plt.xlabel("log1p(cena)")

plt.tight_layout()


print("""
Komentarz do Wykresów 8 i 9:
Po transformacji logarytmicznej rozkład ceny jest mniej skośny.
Transformacja log1p ogranicza wpływ bardzo drogich mieszkań i sprawia,
że rozkład jest bardziej czytelny.
""")
plt.show()

print("\nCZĘŚĆ 7 — WNIOSKI\n")

print("""
Wnioski:

1. Rozkład cen mieszkań w Warszawie jest prawostronnie skośny, ponieważ występują
   pojedyncze bardzo drogie oferty.
2. Metraż jest jedną z najważniejszych zmiennych wpływających na cenę całkowitą.
3. Cena za m2 jest lepsza do porównywania dzielnic niż sama cena całkowita.
4. W zbiorze występują outliery: bardzo wysokie lub bardzo niskie ceny,
   ogromne metraże oraz błędne lata budowy.
5. Przed dalszą analizą warto oczyścić dane, usuwając nielogiczne lata budowy
   i ograniczając skrajne ceny przez winsoryzację.
""")

input("Naciśnij Enter, aby zakończyć...")