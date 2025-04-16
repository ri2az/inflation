import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Inflation France – IPCH / ISJ / IPC", layout="wide")
st.title("📊 Inflation en France (IPCH, ISJ, IPC) – Graph XKCD")

URL = "https://www.insee.fr/fr/statistiques/8558558#tableau-ipc-g1-fr"

@st.cache_data
def fetch_textual_inflation_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    raw_text = soup.get_text()

    pattern = re.compile(r'(\d{4}-\d{2})\s+([\d\.\-]+)\s+([\d\.\-]+)\s+([\d\.\-]+)')
    matches = pattern.findall(raw_text)

    df = pd.DataFrame(matches, columns=["Date", "IPCH", "ISJ", "IPC"])
    df["Date"] = pd.to_datetime(df["Date"])
    df[["IPCH", "ISJ", "IPC"]] = df[["IPCH", "ISJ", "IPC"]].astype(float)
    df = df.sort_values("Date")
    return df

df = fetch_textual_inflation_data()

if df is not None and not df.empty:
    # ---- FILTRE ----
    st.sidebar.header("🔎 Filtrer les données")
    all_years = df["Date"].dt.year.unique()
    selected_years = st.sidebar.multiselect("Choisir l'année(s) :", sorted(all_years, reverse=True), default=all_years[-3:])

    filtered_df = df[df["Date"].dt.year.isin(selected_years)]

    # ---- COURBES ----
    st.subheader("📈 Évolution IPCH / ISJ / IPC")
    selected_curves = st.multiselect("Afficher les indices :", ["IPCH", "ISJ", "IPC"], default=["IPCH", "IPC"])

    with plt.xkcd():
        fig, ax = plt.subplots(figsize=(12, 5))
        for col in selected_curves:
            ax.plot(filtered_df["Date"], filtered_df[col], label=col, marker='o')
        ax.set_title("Évolution des indices d'inflation")
        ax.set_xlabel("Date")
        ax.set_ylabel("Taux (%)")
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # ---- DONNÉES & EXPORT ----
    st.subheader("📋 Données filtrées")
    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Télécharger en CSV", data=csv, file_name="inflation_france_filtrée.csv", mime="text/csv")

else:
    st.error("❌ Échec du chargement des données.")

# ---- DESCRIPTION DES INDICES ----
st.subheader("ℹ️ Description des indices IPCH, IPC, ISJ")

with st.expander("📘 Qu’est-ce que IPCH, IPC et ISJ ?", expanded=True):
    st.markdown("""
#### 🔸 **IPCH – Indice des Prix à la Consommation Harmonisé**
- Indice **européen** permettant de comparer l'inflation entre pays de l'UE.
- Calculé selon une méthode commune à tous les États membres.
- N’inclut pas certains éléments propres à chaque pays (ex : loyers imputés).

#### 🔸 **IPC – Indice des Prix à la Consommation**
- Indice **national français**, utilisé comme référence officielle.
- Mesure l'évolution des prix d’un panier moyen de consommation en France.
- Sert à l’**indexation des salaires, retraites, loyers**, etc.

#### 🔸 **ISJ – Indice Spécifique des Jeunes**
- Variante de l'IPC adaptée au **mode de vie des jeunes de moins de 30 ans**.
- Panier spécifique : plus orienté vers le **logement, les transports, la technologie et l’alimentation**.
- Utile pour comprendre l’impact de l’inflation sur cette tranche d’âge.
""")