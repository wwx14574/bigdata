import requests
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# pobieranie danych z API
url = "https://restcountries.com/v3.1/all?fields=name,capital,region,subregion,population,area,currencies"

res = requests.get(url)
data = res.json()

# listy
nazwy = []
stolice = []
regiony = []
subregiony = []
populacje = []
powierzchnie = []
waluty = []

for kraj in data:
    # nazwa
    nazwy.append(kraj.get("name", {}).get("common"))

    # stolica (lista - pierwszy element)
    if kraj.get("capital"):
        stolice.append(kraj.get("capital")[0])
    else:
        stolice.append(None)

    # region
    regiony.append(kraj.get("region"))

    # subregion
    subregiony.append(kraj.get("subregion"))

    # populacja
    populacje.append(kraj.get("population"))

    # powierzchnia
    powierzchnie.append(kraj.get("area"))

    # waluta
    curr = kraj.get("currencies")
    if curr:
        waluty.append(list(curr.keys())[0])
    else:
        waluty.append(None)

# DataFrame
df = pd.DataFrame({
    "nazwa": nazwy,
    "stolica": stolice,
    "region": regiony,
    "subregion": subregiony,
    "populacja": populacje,
    "powierzchnia": powierzchnie,
    "waluta": waluty
})

print(df.head())
print(df.shape)
print(df.dtypes)

# zapis do bazy
conn = sqlite3.connect("kraje_swiata.db")
df.to_sql("kraje", conn, if_exists="replace", index=False)

# zapytania SQL

# suma populacji
q1 = "SELECT SUM(populacja) FROM kraje"
print("\nSuma populacji świata:")
print(pd.read_sql_query(q1, conn))

# top 10 krajów
q2 = """
SELECT nazwa, populacja
FROM kraje
ORDER BY populacja DESC
LIMIT 10
"""
print("\nNajludniejsze kraje:")
print(pd.read_sql_query(q2, conn))

# regiony
q3 = """
SELECT region, COUNT(*) as ile_krajow, AVG(populacja) as srednia
FROM kraje
GROUP BY region
"""
print("\nRegiony:")
print(pd.read_sql_query(q3, conn))

# większe niż Polska
q4 = """
SELECT nazwa, powierzchnia
FROM kraje
WHERE powierzchnia > 312679
"""
print("\nWiększe niż Polska:")
print(pd.read_sql_query(q4, conn))

# gęstość zaludnienia
q5 = """
SELECT nazwa,
       populacja / powierzchnia as gestosc
FROM kraje
WHERE powierzchnia > 0
ORDER BY gestosc DESC
LIMIT 1
"""
print("\nNajwiększa gęstość:")
print(pd.read_sql_query(q5, conn))

# wykres
q_chart = """
SELECT region, SUM(populacja) as suma
FROM kraje
GROUP BY region
"""

df_chart = pd.read_sql_query(q_chart, conn)

plt.bar(df_chart["region"], df_chart["suma"])
plt.title("Populacja wg regionów")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

conn.close()
