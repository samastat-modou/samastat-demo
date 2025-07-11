import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# Configuration générale
st.set_page_config(page_title="Analyse des Données Scolaires", page_icon="📊", layout="wide")

# Affichage du logo
logo = Image.open("logo.png")
st.image(logo, width=120)

# Chargement des données
@st.cache_data
def load_data():
    return pd.read_csv("data_student.csv")

df = load_data()

# Titre principal
st.title("📊 Module de Statistiques Scolaires - SamaStat")

# Filtres interactifs
departments = df['Department'].unique()
selected_departments = st.multiselect("Choisir les départements :", options=departments, default=list(departments))
filtered_df = df[df['Department'].isin(selected_departments)]

# Conversion utile pour éviter les erreurs
filtered_df["Semester"] = filtered_df["Semester"].astype(str)

# Colonnes pour mise en page
col1, col2 = st.columns(2)

with col1:
    st.subheader("Répartition des notes finales")

    # Histogramme des notes par genre
    fig_grade = px.histogram(
        filtered_df,
        x="Grade",
        color="Gender",
        barmode="group",
        title="Distribution des notes",
        template="plotly_white"
    )
    st.plotly_chart(fig_grade, use_container_width=True)

    # Boxplot par département
    fig_box = px.box(
        filtered_df,
        x="Department",
        y="Final_Score",
        color="Gender",
        title="Dispersion des scores par département",
        template="ggplot2"
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # Violin plot par genre
    fig_violin = px.violin(
        filtered_df,
        y="Final_Score",
        x="Gender",
        box=True,
        points="all",
        title="Distribution des scores par genre"
    )
    st.plotly_chart(fig_violin, use_container_width=True)

    # Graphique animé selon le semestre
    fig_line = px.line(
        filtered_df,
        x="Semester",
        y="Final_Score",
        animation_frame="Semester",
        color="Department",
        title="Évolution des scores par semestre"
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.subheader("Moyenne des scores finaux par département")

    # Moyenne des scores
    avg_scores = filtered_df.groupby("Department")["Final_Score"].mean().reset_index()
    fig_avg = px.bar(
        avg_scores,
        x="Department",
        y="Final_Score",
        title="Score final moyen par département",
        template="plotly_dark"
    )
    st.plotly_chart(fig_avg, use_container_width=True)

# Corrélation : étude, stress, résultats
st.markdown("---")
st.subheader("📈 Corrélation : Stress, Études et Résultats")

fig_corr = px.scatter(
    filtered_df,
    x="Study_Hours_per_Week",
    y="Final_Score",
    size="Stress_Level (1-10)",
    color="Gender",
    hover_data=["Department", "Sleep_Hours_per_Night"],
    title="Effet des heures d'étude sur le score final (taille = stress)",
    template="plotly_white"
)
st.plotly_chart(fig_corr, use_container_width=True)

# Affichage des données brutes
st.markdown("---")
st.subheader("💡 Tableau de données brutes")
st.data