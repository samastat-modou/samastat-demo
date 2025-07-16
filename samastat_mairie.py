import streamlit as st
import json
import bcrypt
import os
import pandas as pd

# --- PARAMÈTRES ---
LOGO_PATH = "samastat_logo.jpg"
USER_FILE = "users.json"

COMMUNES = {
    "Dakar": {"Population": 1050000, "Taux Vaccination (%)": 75},
    "Thiès": {"Population": 320000, "Taux Vaccination (%)": 65},
    "Diourbel": {"Population": 250000, "Taux Vaccination (%)": 70},
}

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
    hashed = users[username].encode('utf-8')
    return check_password(password, hashed)

# --- PAGE D'ACCUEIL ---
def show_welcome_page():
    st.set_page_config(page_title="SamaStat Mairie", layout="centered")
    st.image(LOGO_PATH, width=250)
    st.title("Bienvenue sur SamaStat Mairie")
    st.markdown(
        "### Votre plateforme de veille statistique au service des collectivités locales.\n"
        "Accédez à des indicateurs clés et rapports pour mieux piloter vos actions à Dakar, Thiès et Diourbel."
    )
    st.info("Veuillez vous connecter pour accéder aux données.")

# --- CONNEXION ---
def show_login():
    st.sidebar.header("Connexion")
    username = st.sidebar.text_input("Nom d'utilisateur")
    password = st.sidebar.text_input("Mot de passe", type="password")
    if st.sidebar.button("Se connecter"):
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Bienvenue {username} ! Vous êtes connecté.")
            st.experimental_rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

# --- APPLICATION PRINCIPALE ---
def show_main_app():
    st.title("📊 Tableau de bord SamaStat Mairie")
    st.write(f"Connecté en tant que **{st.session_state.username}**")

    selected_commune = st.selectbox("📍 Choisissez une commune :", options=list(COMMUNES.keys()))
    data = COMMUNES[selected_commune]

    st.markdown(f"### Données pour {selected_commune}")
    st.write(f"👥 Population : {data['Population']:,}")
    st.write(f"💉 Taux de vaccination : {data['Taux Vaccination (%)']}%")

    # --- TABLE + EXPORT CSV ---
    df = pd.DataFrame(COMMUNES).T
    st.table(df)

    st.markdown("### 📥 Télécharger les données")
    csv_data = df.to_csv(index=True).encode('utf-8')
    st.download_button(
        label="📊 Télécharger les données des communes (.csv)",
        data=csv_data,
        file_name='donnees_communes.csv',
        mime='text/csv'
    )

    # --- RAPPORT SYNTHÉTIQUE ---
    st.markdown("### 🧾 Télécharger un rapport synthétique")
    rapport = f"""\n
    RAPPORT SAMAStat Mairie - Zones Ciblées\n
    Nombre de communes : {len(df)}\n
    Population totale : {df['Population'].sum():,}\n
    Taux de vaccination moyen : {df['Taux Vaccination (%)'].mean():.2f} %
    """
    rapport_csv = "Indicateur,Valeur\n"
    rapport_csv += f"Nombre de communes,{len(df)}\n"
    rapport_csv += f"Population totale,{df['Population'].sum()}\n"
    rapport_csv += f"Taux vaccination moyen,{df['Taux Vaccination (%)'].mean():.2f} %\n"

    st.download_button(
        label="📄 Télécharger rapport synthétique (.csv)",
        data=rapport_csv.encode('utf-8'),
        file_name="rapport_samastat.csv",
        mime="text/csv"
    )

    st.text_area("Aperçu du rapport :", rapport.strip(), height=150)

    # --- DÉCONNEXION ---
    if st.button("Se déconnecter"):
        st.session_state.logged_in = False
        st.experimental_rerun()

# --- FONCTION PRINCIPALE ---
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if not st.session_state.logged_in:
        show_welcome_page()
        show_login()
    else:
        show_main_app()

if __name__ == "__main__":
    main()
