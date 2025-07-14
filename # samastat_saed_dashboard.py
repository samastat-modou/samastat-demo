# samastat_dashboard.py

import streamlit as st
import pandas as pd
import random

# 🎯 LISTES DE BASE
cultures = ["Riz", "Maïs", "Tomate", "Oignon"]
regions = ["Saint-Louis", "Dagana", "Podor", "Matam"]
techniques = ["traditionnelle", "semi-intensive", "intensive"]

# 🌾 AGRICULTURE
def simulate_agriculture(n):
    data = []
    for _ in range(n):
        data.append({
            "Campagne": random.choice(["2022", "2023", "2024"]),
            "Région": random.choice(regions),
            "Culture": random.choice(cultures),
            "Superficie_ha": round(random.uniform(10, 100), 2),
            "Rendement_t_ha": round(random.uniform(2.5, 6), 2),
            "Technique": random.choice(techniques)
        })
    return pd.DataFrame(data)

# 💧 IRRIGATION
def simulate_irrigation(n):
    types = ["gravitaire", "goutte-à-goutte", "aspersion"]
    états = ["fonctionnelle", "endommagée", "à réhabiliter"]
    freq = ["quotidienne", "hebdomadaire", "mensuelle"]
    data = []
    for _ in range(n):
        data.append({
            "Campagne": random.choice(["2022", "2023", "2024"]),
            "Zone_irriguee": random.choice(regions),
            "Type_irrigation": random.choice(types),
            "État_infrastructure": random.choice(états),
            "Fréquence_irrigation": random.choice(freq)
        })
    return pd.DataFrame(data)

# 👥 PRODUCTEURS
def simulate_producteurs(n):
    statuts = ["individuel", "coopérative", "GIE"]
    data = []
    for _ in range(n):
        data.append({
            "Nom": f"Producteur_{random.randint(1,999)}",
            "Sexe": random.choice(["H", "F"]),
            "Âge": random.randint(20, 65),
            "Statut": random.choice(statuts),
            "Région": random.choice(regions),
            "Culture": random.choice(cultures)
        })
    return pd.DataFrame(data)

# 💰 FINANCEMENT
def simulate_financement(n):
    sources = ["SAED", "Bailleur A", "Fonds coopératif"]
    types = ["crédit", "subvention", "appui technique"]
    data = []
    for _ in range(n):
        data.append({
            "Année": random.choice(["2022", "2023", "2024"]),
            "Source": random.choice(sources),
            "Type_financement": random.choice(types),
            "Montant": random.randint(500000, 5000000)
        })
    return pd.DataFrame(data)

# 🔢 GÉNÉRATION DES DONNÉES
agri_df = simulate_agriculture(50)
irrig_df = simulate_irrigation(50)
prod_df = simulate_producteurs(50)
fin_df = simulate_financement(50)

# 🎛️ INTERFACE STREAMLIT
st.set_page_config(page_title="SamaStat SAED", layout="wide")
st.title("📊 Tableau de bord SamaStat – SAED")

st.markdown("Bienvenue sur la plateforme statistique interactive dédiée à la SAED. Explorez, filtrez, téléchargez et donnez votre avis ! 💼")

# 🌾 AGRICULTURE
st.subheader("🌾 Données agricoles")
st.dataframe(agri_df)

# 💧 IRRIGATION
st.subheader("💧 Données d'irrigation")
st.dataframe(irrig_df)

# 👥 PRODUCTEURS
st.subheader("👥 Données des producteurs")
st.dataframe(prod_df)

# 💰 FINANCEMENT
st.subheader("💰 Données de financement")
st.dataframe(fin_df)

# 📊 GRAPHIQUE FINANCEMENT
st.subheader("📈 Financement par année")
st.bar_chart(fin_df.groupby("Année")["Montant"].sum())

# 📦 FUSION POUR EXPORT CSV
merged_df = agri_df.merge(irrig_df, left_on=["Campagne", "Région"], right_on=["Campagne", "Zone_irriguee"], how="left")
merged_df = merged_df.merge(fin_df, left_on="Campagne", right_on="Année", how="left")

csv = merged_df.to_csv(index=False).encode('utf-8')

# 📤 EXPORT CSV
st.subheader("📥 Export des données consolidées")
st.download_button("Télécharger le fichier CSV", data=csv, file_name="samastat_saed.csv", mime="text/csv")

# 🗣️ COMMENTAIRE UTILISATEUR
st.subheader("📝 Votre avis sur SamaStat")
satisfaction = st.radio("Quel est votre niveau de satisfaction ?", ["Très satisfait", "Satisfait", "Moyennement satisfait", "Pas satisfait du tout"])
commentaire = st.text_area("Comment améliorer cette application ?")

if st.button("📨 Soumettre votre avis"):
    st.success("Merci pour votre retour, il a bien été enregistré (simulation). 🙏")

