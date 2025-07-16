
import streamlit as st
import pandas as pd
import json
import bcrypt
import os

# --- PARAMÈTRES ---
LOGO_PATH = "logo.png"
USER_FILE = "users.json"
DATA_FILE = "samastat_mairie_donnees.csv"

# --- UTILISATEUR ---
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)

def verify_user(username, password):
    users = load_users()
    if username not in users:
        return False
    hashed = users[username].encode("utf-8")
    return check_password(password, hashed)

# --- PAGE D'ACCUEIL ---
def show_welcome_page():
    st.set_page_config(page_title="SamaStat Mairie", layout="centered")
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=250)
    st.title("Bienvenue sur SamaStat Mairie")
    st.markdown("### Votre plateforme de veille statistique au service des collectivités locales.")
    st.info("Veuillez vous connecter pour accéder aux données.")

# --- CONNEXION ---
def show_login():
    st.sidebar.subheader("🧑‍💻 Connexion")
    username = st.sidebar.text_input("Nom d'utilisateur", key="login_user")
    password = st.sidebar.text_input("Mot de passe", type="password", key="login_pass")
    if st.sidebar.button("Se connecter"):
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Bienvenue {username} ! Vous êtes connecté.")
            st.rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

# --- TABLEAU COMPLET ---
def show_full_dashboard():
    st.title("📊 Tableau de bord complet - SamaStat Mairie")
    df = pd.read_csv(DATA_FILE)

    commune = st.selectbox("🏙️ Choisissez une commune :", df["Commune"].unique())
    data = df[df["Commune"] == commune].iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Population", f"{data['Population Totale']:,}")
        st.metric("Croissance annuelle", f"{data['Croissance Annuelle (%)']} %")
        st.metric("Femmes (%)", f"{data['Femmes (%)']} %")
        st.metric("Taux de scolarisation", f"{data['Taux de Scolarisation (%)']} %")
        st.metric("Vaccination", f"{data['Taux de Vaccination (%)']} %")
    with col2:
        st.metric("Nombre d'écoles", int(data["Nombre d'Écoles"]))
        st.metric("Postes de sécurité", int(data["Postes de Sécurité"]))
        st.metric("Logements sociaux", int(data["Logements Sociaux Construits"]))
        st.metric("Budget participatif", f"{data['Budget Participatif (millions CFA)']} M CFA")
        st.metric("Incendies/an", int(data["Incendies/an"]))

    st.markdown("### 📌 Visualisations")
    chart_type = st.radio("Type de graphique :", ["Diagramme en barre", "Diagramme circulaire"])
    selected_fields = [
        "Taux de Scolarisation (%)", "Taux de Vaccination (%)", "Taux de Chômage (%)",
        "Accès à l'Eau Potable (%)", "Électricité (%)"
    ]
    chart_data = df[df["Commune"] == commune][selected_fields].T
    chart_data.columns = ["Valeur"]

    if chart_type == "Diagramme en barre":
        st.bar_chart(chart_data)
    else:
        st.pyplot(chart_data.plot.pie(y="Valeur", autopct="%1.1f%%", figsize=(5, 5)).get_figure())

    with st.expander("📄 Voir toutes les données"):
        st.dataframe(data.to_frame().rename(columns={data.name: commune}))

    st.download_button(
        label="📥 Télécharger les données (.csv)",
        data=data.to_frame().T.to_csv(index=False).encode("utf-8"),
        file_name=f"{commune.lower()}_samastat.csv",
        mime="text/csv"
    )

    st.markdown("### ✅ Donnez votre avis")
    st.slider("Niveau de satisfaction global", 0, 10, 5)
    st.text_area("Commentaires ou suggestions")

# --- APPLICATION PRINCIPALE ---
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if st.session_state.logged_in:
        st.sidebar.success(f"Connecté en tant que {st.session_state.username}")
        if st.sidebar.button("🔓 Se déconnecter"):
            st.session_state.logged_in = False
            st.rerun()
        show_full_dashboard()
    else:
        show_welcome_page()
        show_login()

if __name__ == "__main__":
    main()
