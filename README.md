# 📊 Visualisation de l'inflation en France (IPCH, IPC, ISJ)

Ce projet Streamlit permet de visualiser l'évolution du **prix du supercarburant sans plomb 95 (SP95)** en France et de le comparer aux **indices d'inflation officiels** : **IPC**, **IPCH**, et **ISJ**.

---

## 🚀 Fonctionnalités

- 📈 **Graphique interactif (Plotly)** ou ✏️ **style XKCD dessiné à la main**
- 🎛️ Filtrage dynamique :
- Sélection des courbes à afficher
- Normalisation (base 100) pour comparaison relative
- Sélection d'années spécifiques
- 📥 Export CSV des données filtrées
- 📆 Données à jour directement depuis l’INSEE

---

## 🔢 Données utilisées

- **Prix SP95** : fichier CSV nettoyé à partir des séries INSEE ([série 000849411](https://www.insee.fr/fr/statistiques/serie/000849411))
- **Indices d’inflation** :
  - IPC : Indice des prix à la consommation (France)
  - IPCH : Indice européen harmonisé
  - ISJ : Indice spécifique des jeunes
  - Source INSEE : [Statistiques inflation](https://www.insee.fr/fr/statistiques/8558558)

---

## 🛠️ Technologies

- [Streamlit](https://streamlit.io/)
- [Matplotlib](https://matplotlib.org/)
- [Pandas](https://pandas.pydata.org/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://docs.python-requests.org/)
- [plotly](https://plotly.com//)

---


## 🛠️ Installation
### 1️⃣ Cloner le dépôt
```sh
git clone https://github.com/ri2az/inflation.git
cd inflation
```

### 2️⃣ Installer les dépendances
Assurez-vous d'avoir Python 3 installé, puis exécutez :
```sh
pip install -r requirements.txt
```

### 3️⃣ Lancer l'application
```sh
streamlit run app.py
```

### 4️⃣ Lancer l'application sur Streamlit !

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://riaaz-inflation.streamlit.app//)
