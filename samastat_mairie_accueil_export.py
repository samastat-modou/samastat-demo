
import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import bcrypt
import os
import pandas as pd

LOGO_PATH = "samastat_logo.jpg"
USER_FILE = "users.json"

COMMUNES = {
    "Dakar": {"Population": 1050000, "Taux Vaccination (%)": 75},
    "Thiès": {"Population": 320000, "Taux Vaccination (%)": 65},
    "Diourbel": {"Population": 250000, "Taux Vaccination (%)": 70},
}

COORDINATES = {
    "Dakar": [14.6928, -17.4467],
    "Thiès": [14.7928, -16.9190],
    "Diourbel": [14.6550, -16.2425],
}

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

def show_welcome_page():
    st.set_page_config(page_title="SamaStat Mairie", layout="centered")
    st.image(LOGO_PATH, width=250)
    st.title("Bienvenue sur SamaStat Mairie")
    st.markdown(
        "### Votre plateforme de veille statistique au service des collectivités locales.\n"
        "Accédez à des indicateurs clés, cartes interactives et rapports pour mieux piloter vos actions à Dakar, Thiès et Diourbel."
    )
    st.info("Veuillez vous connecter pour accéder aux données.")

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

def show_main_app():
    st.title("Tableau de bord SamaStat Mairie")
    st.write(f"Connecté en tant que : {st.session_state.username}")

    m = folium.Map(location=[14.7, -17.4], zoom_start=7)
    for commune, coords in COORDINATES.items():
        data = COMMUNES[commune]
        popup_text = f"{commune} <br> Population : {data['Population']:,} <br> Taux Vaccination : {data['Taux Vaccination (%)']}%"
        folium.Marker(location=coords, popup=popup_text).add_to(m)
    st_folium(m, width=700, height=500)

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

    if st.button("Se déconnecter"):
        st.session_state.logged_in = False
        st.experimental_rerun()

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
