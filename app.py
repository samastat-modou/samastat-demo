import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="SamaStat - Veille statistique", layout="wide")

# --- AUTHENTIFICATION ---
st.sidebar.header("🔐 Accès sécurisé")
mdp = st.sidebar.text_input("Entrez le mot de passe :", type="password")
mdp_attendu = "Samastat2025"  # Modifie ce mot de passe selon ton besoin

if mdp != mdp_attendu:
    st.warning("⛔ Accès refusé. Mot de passe incorrect.")
    st.stop()
else:
    st.sidebar.success("✅ Authentifié")

# --- TITRE ---
st.markdown("<h1 style='text-align: center;'>📊 SamaStat - Veille statistique intelligente</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Indicateurs sociaux & économiques des régions du Sénégal 🇸🇳</h4>", unsafe_allow_html=True)
st.markdown("---")

# --- DONNÉES SIMULÉES ---
regions = [
    "Dakar", "Thiès", "Saint-Louis", "Diourbel", "Kaolack",
    "Ziguinchor", "Fatick", "Kédougou", "Tambacounda", "Matam"
]

data = {
    "Région": regions,
    "Population": [3400000, 1800000, 980000, 1100000, 1030000, 860000, 720000, 320000, 700000, 650000],
    "Taux de scolarisation (%)": [90, 82, 79, 77, 75, 74, 76, 65, 68, 70],
    "Accès à l’eau potable (%)": [94, 88, 85, 83, 84, 81, 86, 70, 73, 75],
    "Taux de chômage (%)": [14, 12, 10, 11, 13, 9, 10, 8, 7, 6],
    "PIB régional (milliards FCFA)": [5200, 3600, 2300, 1800, 1700, 1600, 1400, 700, 900, 850],
    "Revenu moyen annuel (FCFA)": [1400000, 1100000, 950000, 870000, 820000, 780000, 770000, 600000, 620000, 640000],
    "Taux d’accès aux soins (%)": [93, 88, 84, 81, 79, 76, 78, 66, 70, 72],
    "Taux de pauvreté (%)": [18, 25, 30, 32, 34, 29, 28, 41, 39, 37]
}

df = pd.DataFrame(data)

# --- FILTRE ---
with st.sidebar:
    st.header("🔎 Filtrer par région")
    selected_regions = st.multiselect("Choisissez les régions :", options=df["Région"], default=df["Région"])

df_filtered = df[df["Région"].isin(selected_regions)]

# --- ONGLET PRINCIPAL ---
tab1, tab2, tab3 = st.tabs([
    "📈 Indicateurs sociaux",
    "💰 Indicateurs économiques",
    "📉 Tendance & prévisions"
])

with tab1:
    st.subheader("👥 Population et Éducation")
    col1, col2 = st.columns(2)
    fig_pop = px.bar(df_filtered, x="Région", y="Population", color="Population", template="plotly_white")
    col1.plotly_chart(fig_pop, use_container_width=True)

    fig_sco = px.line(df_filtered, x="Région", y="Taux de scolarisation (%)", markers=True, template="plotly_white")
    col2.plotly_chart(fig_sco, use_container_width=True)

    st.subheader("🚰 Eau potable vs 💼 Chômage")
    col3, col4 = st.columns(2)
    fig_eau = px.bar(df_filtered, x="Région", y="Accès à l’eau potable (%)", color="Accès à l’eau potable (%)", template="plotly_white")
    col3.plotly_chart(fig_eau, use_container_width=True)

    fig_chom = px.scatter(df_filtered, x="Région", y="Taux de chômage (%)", size="Population", color="Taux de chômage (%)", template="plotly_white")
    col4.plotly_chart(fig_chom, use_container_width=True)

with tab2:
    st.subheader("🏦 Indicateurs économiques")
    fig_pib = px.bar(df_filtered, x="Région", y="PIB régional (milliards FCFA)", color="PIB régional (milliards FCFA)", template="plotly_white")
    st.plotly_chart(fig_pib, use_container_width=True)

    fig_rev = px.line(df_filtered, x="Région", y="Revenu moyen annuel (FCFA)", markers=True, template="plotly_white")
    st.plotly_chart(fig_rev, use_container_width=True)

    fig_corr = px.scatter(df_filtered, x="Taux d’accès aux soins (%)", y="Taux de pauvreté (%)", size="Population", color="Région", template="plotly_white",
                          title="💡 Accès aux soins vs Taux de pauvreté")
    st.plotly_chart(fig_corr, use_container_width=True)

with tab3:
    st.subheader("📉 Tendance du chômage (2021–2025)")
    # --- SIMULATION DE DONNÉES TEMPORAIRES ---
    annees = list(range(2021, 2026))
    data_tendance = []
    np.random.seed(42)

    for region in selected_regions:
        base_chomage = df[df["Région"] == region]["Taux de chômage (%)"].values[0]
        for annee in annees:
            evolution = base_chomage + np.random.normal(0, 0.5)
            data_tendance.append({
                "Région": region,
                "Année": annee,
                "Taux de chômage (%)": round(evolution, 2)
            })

    df_tendance = pd.DataFrame(data_tendance)
    fig_tendance = px.line(df_tendance, x="Année", y="Taux de chômage (%)", color="Région", markers=True, template="plotly_white")
    st.plotly_chart(fig_tendance, use_container_width=True)

    st.subheader("🔮 Prévision du taux de chômage en 2026")
    df_prevision = df_tendance[df_tendance["Année"] == 2025].copy()
    df_prevision["Prévision 2026 (%)"] = round(df_prevision["Taux de chômage (%)"] * np.random.uniform(0.97, 1.03, len(df_prevision)), 2)
    st.dataframe(df_prevision[["Région", "Taux de chômage (%)", "Prévision 2026 (%)"]], use_container_width=True)

# --- NOTE ---
st.markdown("<p style='text-align: center; color: gray;'>✅ Données simulées à des fins de démonstration</p>", unsafe_allow_html=True)
