import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import plotly.express as px

# -------------------- CONFIG --------------------
st.set_page_config(page_title="SP95 vs Inflation", layout="wide")
st.title("📊 Comparaison : Prix SP95 vs Inflation (IPC, IPCH, ISJ)")

# -------------------- 1. Charger SP95 --------------------
CSV_SP95 = "prix_sp95_nettoye.csv"

@st.cache_data
def fetch_sp95_data():
    df = pd.read_csv(CSV_SP95)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Prix"] = pd.to_numeric(df["Prix"], errors="coerce")
    return df.dropna().sort_values("Date")

df_sp95 = fetch_sp95_data()

# -------------------- 2. Charger indices INSEE --------------------
@st.cache_data
def fetch_textual_inflation_data():
    URL = "https://www.insee.fr/fr/statistiques/8558558#tableau-ipc-g1-fr"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    raw_text = soup.get_text()

    pattern = re.compile(r'(\d{4}-\d{2})\s+([\d\.\-]+)\s+([\d\.\-]+)\s+([\d\.\-]+)')
    matches = pattern.findall(raw_text)

    df = pd.DataFrame(matches, columns=["Date", "IPCH", "ISJ", "IPC"])
    df["Date"] = pd.to_datetime(df["Date"])
    df[["IPCH", "ISJ", "IPC"]] = df[["IPCH", "ISJ", "IPC"]].astype(float)
    return df.sort_values("Date")

df_inflation = fetch_textual_inflation_data()

# -------------------- 3. Fusion --------------------
df_merged = pd.merge(df_inflation, df_sp95, on="Date", how="inner")

# -------------------- 4. Interface utilisateur --------------------
st.sidebar.header("🎛️ Options d'affichage")

selected_curves = st.sidebar.multiselect(
    "Courbes à afficher :",
    ["SP95", "IPC", "IPCH", "ISJ"],
    default=["SP95", "IPC"]
)

normalize = st.sidebar.checkbox("🔁 Normaliser en base 100", value=False)

graph_style = st.sidebar.radio("🖌️ Style de graphique :", ["📈 Interactif (Plotly)", "✏️ Style XKCD (matplotlib)"])

# 📆 Filtrage par années
all_years = sorted(df_merged["Date"].dt.year.unique())
selected_years = st.sidebar.multiselect(
    "📆 Filtrer par année(s) :",
    all_years,
    default=all_years[-5:]
)

# Appliquer le filtre année
df_plot = df_merged[df_merged["Date"].dt.year.isin(selected_years)].copy()

# -------------------- 5. Préparer les données --------------------
column_mapping = {
    "SP95": "Prix",
    "IPC": "IPC",
    "IPCH": "IPCH",
    "ISJ": "ISJ"
}

if normalize:
    for label, col in column_mapping.items():
        if col in df_plot:
            df_plot[f"{label}_norm"] = df_plot[col] / df_plot[col].iloc[0] * 100

# -------------------- 6. Affichage graphique --------------------
st.subheader("📈 Évolution des courbes sélectionnées")

if graph_style == "📈 Interactif (Plotly)":
    data_to_plot = []

    for label in selected_curves:
        col = f"{label}_norm" if normalize else column_mapping[label]
        if col in df_plot:
            temp_df = df_plot[["Date", col]].copy()
            temp_df.columns = ["Date", "Valeur"]
            temp_df["Indice"] = label
            data_to_plot.append(temp_df)

    df_long = pd.concat(data_to_plot)

    fig = px.line(
        df_long,
        x="Date",
        y="Valeur",
        color="Indice",
        markers=True,
        title="Évolution des indices et du SP95" + (" (base 100)" if normalize else "")
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Indice (base 100)" if normalize else "Taux / Prix (€)",
        legend_title="Courbes",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    with plt.xkcd():
        fig, ax = plt.subplots(figsize=(12, 5))
        for label in selected_curves:
            col = f"{label}_norm" if normalize else column_mapping[label]
            ax.plot(df_plot["Date"], df_plot[col], label=label)  # Sans marker
        ax.set_title("Évolution style XKCD (base 100)" if normalize else "Évolution style XKCD")
        ax.set_xlabel("Date")
        ax.set_ylabel("Indice (base 100)" if normalize else "Taux / Prix (€)")
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)

# -------------------- 7. Données et export --------------------
st.subheader("📋 Données utilisées")
cols_to_show = ["Date"] + [column_mapping[c] for c in selected_curves if c != "SP95"] + (["Prix"] if "SP95" in selected_curves else [])
st.dataframe(df_plot[cols_to_show], use_container_width=True)

csv = df_plot[cols_to_show].to_csv(index=False).encode("utf-8")
st.download_button("📥 Télécharger les données filtrées", data=csv, file_name="donnees_filtrees.csv", mime="text/csv")

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
