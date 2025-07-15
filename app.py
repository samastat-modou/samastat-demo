import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="SamaStat", layout="wide")

# --- LOGO ---
logo = Image.open("assets/logo.png")
st.image(logo, width=200)

# --- TITRE ---
st.markdown("<h1 style='text-align: center;'>SamaStat - Veille statistique intelligente</h1>", unsafe_allow_html=True)

# --- MENU DE NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", ["Accueil", "Indicateurs", "Prévisions", "À propos"])

# --- ACCUEIL ---
if page == "Accueil":
    st.header("Vue d'ensemble")
    st.markdown("Bienvenue sur SamaStat, la plateforme citoyenne de données locales pour le Sénégal.")

# --- INDICATEURS ---
elif page == "Indicateurs":
    st.header("📊 Indicateurs par région")

    # Chargement des données Excel
    try:
        df = pd.read_excel("data/indicateurs_senegal.xlsx", sheet_name="Indicateurs")
        st.dataframe(df)

        # Graphique interactif : taux de pauvreté
        fig = px.bar(df, x="Région", y="Taux de pauvreté (%)",
                     color="Région", title="Taux de pauvreté par région")
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erreur de chargement des données : {e}")

# --- PRÉVISIONS ---
elif page == "Prévisions":
    st.header("📈 Prévisions statistiques")
    st.markdown("Cette section affichera bientôt des modèles de prévision par région.")

# --- À PROPOS ---
elif page == "À propos":
    st.header("ℹ️ À propos de SamaStat")
    st.markdown("""
    **SamaStat** est un projet citoyen visant à rendre les données locales plus accessibles, visualisables et utiles
    pour la prise de décision dans les collectivités territoriales au Sénégal.
    
    **Fondateur :** Modou Sène  
    **Objectifs :** Veille statistique, visualisation des indicateurs, appui à la gouvernance territoriale.
    """)
