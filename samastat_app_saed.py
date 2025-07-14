# SamaStat SAED v1.0 — Application de pilotage agricole
# Auteur : Ton Nom / Organisation
# Description : Dashboard Streamlit avec logo, PDF, filtres, feedback et graphiques

import streamlit as st
import pandas as pd
import random
from fpdf import FPDF
import plotly.graph_objects as go

# 🔧 Configuration Streamlit
st.set_page_config(page_title="SamaStat SAED", layout="wide")

# 🖼️ Affichage du logo dans la sidebar
st.sidebar.image("logo.png", width=220)
st.sidebar.title("🔐 Connexion sécurisée")

# 🔐 Authentification basique
users = {"agent_saed": "pass123", "admin_saed": "admin456"}
username = st.sidebar.text_input("Nom d’utilisateur")
password = st.sidebar.text_input("Mot de passe", type="password")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.sidebar.button("Se connecter"):
    if username in users and users[username] == password:
        st.session_state.logged_in = True
        st.sidebar.success(f"✅ Bienvenue {username}")
    else:
        st.sidebar.error("❌ Identifiants incorrects")

# 🎯 Accès au tableau de bord
if st.session_state.logged_in:

    # 🌾 Simuler les données agricoles
    cultures = ["Riz", "Maïs", "Tomate", "Oignon"]
    regions = ["Saint-Louis", "Dagana", "Podor", "Matam"]

    def simulate_agriculture(n):
        data = []
        for _ in range(n):
            data.append({
                "Campagne": random.choice(["2022", "2023", "2024"]),
                "Région": random.choice(regions),
                "Culture": random.choice(cultures),
                "Superficie_ha": round(random.uniform(10, 100), 2),
                "Rendement_t_ha": round(random.uniform(2.5, 6), 2),
                "Technique": random.choice(["traditionnelle", "intensive"])
            })
        return pd.DataFrame(data)

    agri_df = simulate_agriculture(50)

    # 📊 Interface principale
    st.title("📊 Tableau de bord SamaStat – SAED")

    # 🔽 Filtrer par campagne
    campagnes = agri_df["Campagne"].unique()
    selected_campagne = st.selectbox("📆 Sélectionnez la campagne agricole", campagnes)

    filtered_df = agri_df[agri_df["Campagne"] == selected_campagne]
    st.dataframe(filtered_df)

    # 📈 Graphique bar : rendements moyens
    st.subheader("📈 Rendement moyen par culture")
    st.bar_chart(filtered_df.groupby("Culture")["Rendement_t_ha"].mean())

    # 🥧 Diagramme circulaire : répartition des cultures
    st.subheader("🥧 Répartition des cultures")
    pie_data = filtered_df["Culture"].value_counts()
    pie_chart = go.Figure(data=[go.Pie(labels=pie_data.index, values=pie_data.values, hole=0.3)])
    st.plotly_chart(pie_chart)

    # 🗣️ Retour utilisateur
    st.subheader("📝 Votre avis sur SamaStat")
    note = st.slider("Note de satisfaction (0 à 10)", 0, 10, 8)
    commentaire = st.text_area("Suggestions ou remarques ?")
    if st.button("📨 Envoyer le retour"):
        st.success("✅ Merci pour votre contribution ! (stockage simulé)")

    # 📄 Rapport PDF avec logo et slogan
    def generate_pdf(data):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        try:
            pdf.image("logo_samastat.png", x=10, y=8, w=35)
        except:
            pass  # Ignore si image non trouvée
        pdf.ln(40)

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=f"Rapport SamaStat SAED – Campagne {selected_campagne}", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Nombre de producteurs : {len(data)}", ln=True)
        pdf.cell(200, 10, txt=f"Superficie totale : {data['Superficie_ha'].sum():.2f} ha", ln=True)
        pdf.cell(200, 10, txt=f"Rendement moyen : {data['Rendement_t_ha'].mean():.2f} t/ha", ln=True)

        # 🖋️ Slogan en pied de page
        pdf.set_y(-20)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 10, "SamaStat : La plateforme du futur pour la souveraineté agricole 🇸🇳", ln=True, align='C')

        filename = "rapport_samastat.pdf"
        pdf.output(filename)
        return filename

    if st.button("📄 Générer le rapport PDF"):
        file_path = generate_pdf(filtered_df)
        with open(file_path, "rb") as f:
            st.download_button("📥 Télécharger le rapport PDF", f, file_name="rapport_samastat.pdf")

else:
    st.warning("🔒 Veuillez vous connecter pour accéder au tableau de bord.")
