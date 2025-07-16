import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- CONFIGURATION ---
st.set_page_config(page_title="SAED Dashboard", layout="wide")

# --- AUTHENTIFICATION ---
st.sidebar.header("🔐 Connexion sécurisée")
mdp = st.sidebar.text_input("Mot de passe :", type="password")
mdp_attendu = "SAED2025"

if mdp != mdp_attendu:
    st.warning("⛔ Accès refusé. Mot de passe incorrect.")
    st.stop()
else:
    st.sidebar.success("✅ Connecté")

# --- TITRE ---
st.markdown("<h1 style='text-align: center;'>🌾 SAED - Tableau de bord intelligent</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Suivi des indicateurs agricoles, hydriques et économiques</h4>", unsafe_allow_html=True)
st.markdown("---")

# --- DONNÉES SIMULÉES ---
regions = ["Podor", "Dagana", "Richard-Toll", "Bakel", "Matam", "Kanel"]

data = {
    "Région": regions,
    "Superficie cultivée (ha)": [56000, 42000, 38000, 24000, 18000, 15000],
    "Production (tonnes)": [152000, 110000, 98000, 64000, 45000, 39000],
    "Rendement (t/ha)": [2.71, 2.62, 2.58, 2.66, 2.50, 2.60],
    "Volume d’eau distribué (milliers m³)": [30000, 25000, 22000, 18000, 15000, 13000],
    "Taux d’irrigation (%)": [92, 85, 80, 76, 70, 68],
    "Budget régional (millions FCFA)": [7800, 6500, 5800, 4300, 3500, 3000],
    "Revenus agricoles (millions FCFA)": [11500, 9800, 8600, 6400, 4900, 4200],
    "Taux d’emploi agricole (%)": [66, 60, 58, 55, 52, 50]
}

df = pd.DataFrame(data)

# --- FILTRE ---
with st.sidebar:
    st.header("🎯 Filtrage")
    selected_regions = st.multiselect("Sélectionnez les régions :", options=df["Région"], default=regions)

df_filtered = df[df["Région"].isin(selected_regions)]

# --- ONGLETS ---
tab1, tab2, tab3 = st.tabs(["🌾 Agriculture", "💧 Ressources hydriques", "📉 Économie & prévisions"])

with tab1:
    st.subheader("Superficie & production par région")
    col1, col2 = st.columns(2)
    fig_surf = px.bar(df_filtered, x="Région", y="Superficie cultivée (ha)", color="Superficie cultivée (ha)", template="plotly_white")
    col1.plotly_chart(fig_surf, use_container_width=True)

    fig_prod = px.line(df_filtered, x="Région", y="Production (tonnes)", markers=True, template="plotly_white")
    col2.plotly_chart(fig_prod, use_container_width=True)

    st.subheader("📊 Rendement par hectare")
    fig_rend = px.scatter(df_filtered, x="Région", y="Rendement (t/ha)", size="Production (tonnes)", color="Rendement (t/ha)", template="plotly_white")
    st.plotly_chart(fig_rend, use_container_width=True)

with tab2:
    st.subheader("💧 Volume d’eau distribué & Irrigation")
    col3, col4 = st.columns(2)
    fig_eau = px.bar(df_filtered, x="Région", y="Volume d’eau distribué (milliers m³)", color="Volume d’eau distribué (milliers m³)", template="plotly_white")
    col3.plotly_chart(fig_eau, use_container_width=True)

    fig_irrig = px.line(df_filtered, x="Région", y="Taux d’irrigation (%)", markers=True, template="plotly_white")
    col4.plotly_chart(fig_irrig, use_container_width=True)

with tab3:
    st.subheader("💰 Budget & Revenus agricoles")
    col5, col6 = st.columns(2)
    fig_budget = px.bar(df_filtered, x="Région", y="Budget régional (millions FCFA)", color="Budget régional (millions FCFA)", template="plotly_white")
    col5.plotly_chart(fig_budget, use_container_width=True)

    fig_revenu = px.line(df_filtered, x="Région", y="Revenus agricoles (millions FCFA)", markers=True, template="plotly_white")
    col6.plotly_chart(fig_revenu, use_container_width=True)

    st.subheader("📉 Taux d’emploi agricole")
    fig_emploi = px.scatter(df_filtered, x="Région", y="Taux d’emploi agricole (%)", size="Budget régional (millions FCFA)", color="Région", template="plotly_white")
    st.plotly_chart(fig_emploi, use_container_width=True)

    # --- Prévision 2026 ---
    st.subheader("🔮 Prévision du taux d’emploi agricole (2026)")
    np.random.seed(42)
    df_prevision = df_filtered.copy()
    df_prevision["Prévision 2026 (%)"] = round(df_prevision["Taux d’emploi agricole (%)"] * np.random.uniform(0.98, 1.03, len(df_prevision)), 2)
    st.dataframe(df_prevision[["Région", "Taux d’emploi agricole (%)", "Prévision 2026 (%)"]], use_container_width=True)

    # --- Export CSV ---
    st.download_button(
        label="📥 Télécharger les indicateurs filtrés",
        data=df_filtered.to_csv(index=False).encode('utf-8'),
        file_name="indicateurs_SAED.csv",
        mime="text/csv"
    )

    st.download_button(
        label="🔮 Télécharger les prévisions 2026",
        data=df_prevision.to_csv(index=False).encode('utf-8'),
        file_name="previsions_SAED_2026.csv",
        mime="text/csv"
    )

# --- FOOTER ---
st.markdown("<p style='text-align: center; color: gray;'>✅ Données simulées à des fins de démonstration pour la SAED</p>", unsafe_allow_html=True)
