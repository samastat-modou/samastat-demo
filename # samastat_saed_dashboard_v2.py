# ─────────────────────────────────────────────
# SamaStat SAED – Application Statistique v1.0
# Auteur : Ton Nom ou Organisation
# Description : Tableau de bord pour pilotage SAED
# ─────────────────────────────────────────────

import streamlit as st
import pandas as pd
import random
from fpdf import FPDF

# ─────────────────────────────────────────────
# 🖼️ SECTION 1 — Logo & Configuration
# ─────────────────────────────────────────────
st.set_page_config(page_title="SamaStat SAED", layout="wide")
st.sidebar.image("logo_samastat.png", use_column_width=True)
st.sidebar.title("🔐 Authentification")

# ─────────────────────────────────────────────
# 🔐 SECTION 2 — Authentification simple
# ─────────────────────────────────────────────
users = {"agent_saed": "pass123", "admin_saed": "admin456"}
username = st.sidebar.text_input("Nom d'utilisateur")
password = st.sidebar.text_input("Mot de passe", type="password")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.sidebar.button("Se connecter"):
    if username in users and users[username] == password:
        st.session_state.logged_in = True
        st.sidebar.success(f"✅ Bienvenue {username}")
    else:
        st.sidebar.error("Identifiants incorrects")

# ─────────────────────────────────────────────
# ✅ SECTION 3 — Application principale (si connecté)
# ─────────────────────────────────────────────
if st.session_state.logged_in:

    # 🎯 3A — Simulation des données agricoles
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

    # 📊 3B — Affichage du tableau de bord
    st.title("📊 Tableau de bord SamaStat – SAED")
    st.dataframe(agri_df)

    # 📈 3C — Visualisation simple
    st.subheader("📈 Rendement moyen par culture")
    st.bar_chart(agri_df.groupby("Culture")["Rendement_t_ha"].mean())

    # 📝 3D — Retour utilisateur
    st.subheader("🗣️ Votre avis sur SamaStat")
    note = st.slider("Satisfaction (0 à 10)", 0, 10, 7)
    commentaire = st.text_area("Vos suggestions, idées ou remarques")
    if st.button("📨 Soumettre"):
        st.success("✅ Merci pour votre retour (simulation enregistrée)")

    # 📄 3E — Génération du rapport PDF
    def generate_pdf(data):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Rapport SamaStat SAED", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Campagnes : {', '.join(data['Campagne'].unique())}", ln=True)
        pdf.cell(200, 10, txt=f"Superficie totale : {data['Superficie_ha'].sum():.2f} ha", ln=True)
        pdf.cell(200, 10, txt=f"Rendement moyen : {data['Rendement_t_ha'].mean():.2f} t/ha", ln=True)
        pdf.output("rapport_samastat.pdf")
        return "rapport_samastat.pdf"

    if st.button("📄 Générer rapport PDF"):
        path = generate_pdf(agri_df)
        with open(path, "rb") as f:
            st.download_button("📥 Télécharger le rapport", f, file_name="rapport_samastat.pdf")

else:
    st.warning("🔒 Veuillez vous connecter pour accéder au dashboard.")
