import streamlit as st
import json
import bcrypt
import os
import pandas as pd
import matplotlib.pyplot as plt

# --- PARAMÈTRES ---
LOGO_PATH = "logo.png"
USER_FILE = "users.json"
COMMUNE_FILE = "communes.json"

# --- UTILISATEURS ---
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

# --- COMMUNES ---
def load_communes():
    if os.path.exists(COMMUNE_FILE):
        with open(COMMUNE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_communes(data):
    with open(COMMUNE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- PAGE D'ACCUEIL ---
def show_welcome_page():
    st.set_page_config(page_title="SamaStat Mairie", layout="centered")
    st.image(LOGO_PATH, width=250)
    st.title("Bienvenue sur SamaStat Mairie")
    st.markdown(
        "### Votre plateforme de veille statistique au service des collectivités locales.\n"
        "Accédez à des indicateurs clés et rapports pour mieux piloter vos actions à Dakar, Thiès, Diourbel, Mbour et Louga."
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

    if st.sidebar.button("Mot de passe oublié ?"):
        new_pass = st.sidebar.text_input("Nouveau mot de passe", type="password")
        if username and new_pass:
            users = load_users()
            users[username] = hash_password(new_pass).decode('utf-8')
            save_users(users)
            st.sidebar.success("Mot de passe réinitialisé avec succès !")

# --- APPLICATION PRINCIPALE ---
def show_main_app():
    st.title("📊 Tableau de bord SamaStat Mairie")
    st.write(f"Connecté en tant que **{st.session_state.username}**")

    # --- Chargement des données communes
    communes_data = load_communes()
    df = pd.DataFrame(communes_data).T
    df['Commune'] = df.index
    df.reset_index(drop=True, inplace=True)

    # --- Filtrage Domaine
    domaines = df['Domaine'].unique().tolist()
    selected_domaine = st.selectbox("📂 Choisir un domaine :", options=["Tous"] + domaines)
    if selected_domaine != "Tous":
        df = df[df['Domaine'] == selected_domaine]

    # --- Tableau des données principales
    st.dataframe(df[["Commune", "Population", "Taux Vaccination (%)", "Domaine"]])

    st.download_button(
        label="📥 Télécharger ce tableau (.csv)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="communes_filtres.csv",
        mime="text/csv"
    )

    # --- Graphique Population
    domaine_stats = df.groupby("Domaine").agg({
        "Population": "sum",
        "Taux Vaccination (%)": "mean"
    }).reset_index()

    st.markdown("### 📈 Population par domaine")
    st.bar_chart(domaine_stats.set_index("Domaine")["Population"])

    st.markdown("### 🧩 Répartition de la population")
    fig, ax = plt.subplots()
    ax.pie(domaine_stats["Population"], labels=domaine_stats["Domaine"], autopct="%1.1f%%")
    st.pyplot(fig)

    # --- ÉTAT CIVIL ---
    st.markdown("## 📑 Statistiques d'État Civil")
    etat_civil_cols = ["Commune", "Naissances", "Décès", "Mariages", "Divorces"]
    st.dataframe(df[etat_civil_cols])

    st.download_button(
        label="📥 Télécharger les données d'état civil (.csv)",
        data=df[etat_civil_cols].to_csv(index=False).encode("utf-8"),
        file_name="etat_civil.csv",
        mime="text/csv"
    )

    st.markdown("### 👶 Naissances par commune")
    st.bar_chart(df.set_index("Commune")["Naissances"])

    st.markdown("### ⚰️ Décès par commune")
    st.bar_chart(df.set_index("Commune")["Décès"])

    # --- Saisie manuelle état civil
    st.markdown("## ➕ Ajouter un événement d'état civil")
    with st.form("form_etat_civil"):
        selected_commune = st.selectbox("Commune concernée", df["Commune"].unique())
        event_type = st.selectbox("Type d'événement", ["Naissance", "Décès", "Mariage", "Divorce"])
        nombre = st.number_input("Nombre de cas", min_value=1, step=1)
        submitted = st.form_submit_button("Enregistrer")
        if submitted:
            communes_data[selected_commune][event_type + "s"] += int(nombre)
            save_communes(communes_data)
            st.success(f"{nombre} {event_type.lower()}(s) ajouté(s) à {selected_commune}.")
            st.experimental_rerun()

    # --- Satisfaction
    st.markdown("### ✨ Votre satisfaction")
    satisfaction = st.slider("Notez votre satisfaction :", 1, 5, step=1)
    st.write(f"Merci pour votre note : {satisfaction} ⭐")

    # --- Déconnexion
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
