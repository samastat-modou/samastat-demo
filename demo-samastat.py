import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image

# Configuration
st.set_page_config(page_title="SamaStat", layout="wide")

# Logo
logo = Image.open("logo.png")
st.image(logo, width=100)

# Titre
st.title("📊 SamaStat – Veille Statistique Locale")
st.markdown("Analyse interactive des indicateurs territoriaux au Sénégal")

# Sidebar – filtres
st.sidebar.header("🎛️ Filtres")
regions = st.sidebar.multiselect("Choisissez les régions", ["Dakar", "Thiès", "Saint-Louis", "Diourbel", "Ziguinchor"], default=["Dakar", "Thiès"])
indicateur = st.sidebar.selectbox("Indicateur", ["Taux de pauvreté", "Taux d'alphabétisation", "Accès à l'eau potable", "PIB local par habitant"])
annee = st.sidebar.slider("Année", 2000, 2023, 2023)

# Génération de données fictives
communes = [f"Commune {i}" for i in range(1, 11)]
np.random.seed(42)
data = pd.DataFrame({
    "Commune": np.tile(communes, len(regions)),
    "Région": np.repeat(regions, len(communes)),
    "Valeur": np.random.uniform(20, 80, len(communes) * len(regions))
})

# Filtres supplémentaires
selected_communes = st.multiselect("Filtrer par commune", options=communes, default=communes)
filtered_data = data[data["Commune"].isin(selected_communes)]

# Affichage tableau interactif
st.subheader(f"📋 Données filtrées pour {indicateur} ({annee})")
st.dataframe(filtered_data.sort_values(by="Valeur", ascending=False), use_container_width=True)

# Diagramme circulaire
st.subheader("🔘 Répartition des valeurs (Diagramme circulaire)")
fig_pie = px.pie(filtered_data, names="Commune", values="Valeur", color_discrete_sequence=px.colors.sequential.RdBu, hole=0.3)
st.plotly_chart(fig_pie, use_container_width=True)

# Diagramme à barres
st.subheader("📊 Répartition par commune")
fig_bar = px.bar(filtered_data, x="Commune", y="Valeur", color="Région", barmode="group")
st.plotly_chart(fig_bar, use_container_width=True)

# Prévision simple
st.subheader("📈 Prévision à 5 ans")
future_years = list(range(annee, annee + 6))
future_values = np.linspace(filtered_data["Valeur"].mean(), filtered_data["Valeur"].mean() + 10, 6)
forecast_df = pd.DataFrame({"Année": future_years, "Prévision": future_values})
fig_line = px.line(forecast_df, x="Année", y="Prévision", markers=True)
st.plotly_chart(fig_line, use_container_width=True)

# Pied de page
st.markdown("---")
st.markdown("© 2025 SamaStat | Démo interactive")
