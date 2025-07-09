
import streamlit as st
from PIL import Image
# Charger et afficher le logo
logo = Image.open("assets/logo_samastat.png")  # place ton logo dans un dossier assets/
st.image(logo, width=120)

import pandas as pd
import numpy as np
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="SamaStat", layout="wide")

# En-tête
st.title("📊 SamaStat - Veille Statistique Locale")
st.markdown("Bienvenue sur SamaStat, la plateforme intelligente pour le suivi et la prévision des indicateurs territoriaux au Sénégal.")

# Sidebar - sélection
st.sidebar.header("🔎 Filtres")
region = st.sidebar.selectbox("Choisissez une région", ["Dakar", "Thiès", "Saint-Louis", "Diourbel", "Ziguinchor"])
indicateur = st.sidebar.selectbox("Indicateur", ["Taux de pauvreté", "Taux d'alphabétisation", "Accès à l'eau potable", "PIB local par habitant"])
annee = st.sidebar.slider("Année", 2000, 2023, 2023)

# Données fictives
np.random.seed(42)
data = pd.DataFrame({
    "Commune": [f"Commune {i}" for i in range(1, 11)],
    "Valeur": np.random.uniform(20, 80, 10),
})

# Affichage
st.subheader(f"Indicateur : {indicateur} en {region} ({annee})")
fig = px.bar(data, x="Commune", y="Valeur", title=f"{indicateur} par commune", labels={"Valeur": indicateur})
st.plotly_chart(fig, use_container_width=True)

# Section de prévision (fictive pour démo)
st.subheader("📈 Prévision à 5 ans")
future = pd.DataFrame({
    "Année": list(range(annee, annee + 6)),
    "Prévision": np.linspace(data["Valeur"].mean(), data["Valeur"].mean() + 10, 6)
})
fig2 = px.line(future, x="Année", y="Prévision", markers=True, title="Prévision de l'indicateur")
st.plotly_chart(fig2, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("© 2025 SamaStat | Prototype en cours de développement")
