# 📊 Visualisation de l'inflation en France (IPCH, IPC, ISJ)

Ce projet Streamlit permet de visualiser l'évolution de l'inflation en France à partir des données publiées par l'[INSEE](https://www.insee.fr/fr/statistiques/8558558), via un scraping automatique des indices **IPCH**, **ISJ** et **IPC**.

---

## 🚀 Fonctionnalités

- 📈 Graphique de l’inflation en **style XKCD** (dessiné à la main)
- 🔎 **Filtrage par année**
- ✅ Sélection des **indices à afficher** (IPCH, ISJ, IPC)
- 📋 Affichage des données sous forme de tableau
- 💾 Export des données **filtrées en CSV**
- ℹ️ Description claire des **cycles de l’inflation** et des **indices**

---

## 🛠️ Technologies

- [Streamlit](https://streamlit.io/)
- [Matplotlib](https://matplotlib.org/)
- [Pandas](https://pandas.pydata.org/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://docs.python-requests.org/)

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

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://riaaz-btc.streamlit.app/)
