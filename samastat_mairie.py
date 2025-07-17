import streamlit as st
import json
import bcrypt
import os
import pandas as pd

# --- PARAMÈTRES ---
LOGO_PATH = "logo.png"
USER_FILE = "users.json"

COMMUNES = {
    "Dakar": {"Population": 1050000, "Taux Vaccination (%)": 75},
    "Thiès": {"Population": 320000, "Taux Vaccination (%)": 65},
    "Diourbel": {"Population": 250000, "Taux Vaccination (%)": 70},
}

# --- GESTION UTILISATEURS ---
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
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=250)
    st.title("Bienvenue sur SamaStat Mairie")
    st.markdown(
        "### Plateforme de veille statistique pour les collectivités locales.\n"
        "Suivez les indicateurs à Dakar, Thiès et Diourbel."
    )
    st.info("Veuillez vous connecter pour accéder au tableau de bord.")

# --- CONNEXION ---
def show_login():
    st.sidebar.header("🔐 Connexion")
    username = st.sidebar.text_input("Nom d'utilisateur", key="login_user")
    password = st.sidebar.text_input("Mot de passe", type="password", key="login_pass")
    if st.sidebar.button("Se connecter", key="login_btn"):
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Bienvenue {username} !")
            st.rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

# --- APPLICATION PRINCIPALE ---
def show_main_app():
    st.title("📊 Tableau de bord SamaStat Mairie")
    st.write(f"👤 Connecté en tant que **{st.session_state.username}**")

    selected_commune = st.selectbox("📍 Choisissez une commune :", options=list(COMMUNES.keys()))
    data = COMMUNES[selected_commune]

    st.markdown(f"### Données pour {selected_commune}")
    st.write(f"👥 Population : {data['Population']:,}")
    st.write(f"💉 Taux de vaccination : {data['Taux Vaccination (%)']}%")

    df = pd.DataFrame(COMMUNES).T
    st.markdown("### 📋 Données globales")
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
    Taux de vaccination moyen : {df['Taux Vaccination (%)'].mean():.2f} %"""
    
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

    if st.button("🔓 Se déconnecter", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# --- ADMINISTRATION ---
def show_admin_panel():
    st.sidebar.markdown("---")
    with st.sidebar.expander("🔧 Zone Admin"):
        action = st.radio("Action :", ["Créer un compte", "Modifier mot de passe", "Supprimer utilisateur"], key="admin_action")
        users = load_users()

        if action == "Créer un compte":
            new_user = st.text_input("Nom d'utilisateur", key="create_user")
            new_pass = st.text_input("Mot de passe", type="password", key="create_pass")
            if st.button("Créer", key="btn_create"):
                if new_user in users:
                    st.warning("Ce nom d'utilisateur existe déjà.")
                elif not new_user or not new_pass:
                    st.error("Champs obligatoires.")
                else:
                    users[new_user] = hash_password(new_pass).decode()
                    save_users(users)
                    st.success("Compte créé ✅")

        elif action == "Modifier mot de passe":
            user = st.text_input("Utilisateur", key="mod_user")
            old_pass = st.text_input("Ancien mot de passe", type="password", key="mod_old_pass")
            new_pass = st.text_input("Nouveau mot de passe", type="password", key="mod_new_pass")
            if st.button("Mettre à jour", key="btn_update"):
                if user not in users:
                    st.error("Utilisateur introuvable.")
                elif not check_password(old_pass, users[user].encode()):
                    st.error("Mot de passe actuel incorrect.")
                elif not new_pass:
                    st.error("Nouveau mot de passe vide.")
                else:
                    users[user] = hash_password(new_pass).decode()
                    save_users(users)
                    st.success("Mot de passe mis à jour ✅")

        elif action == "Supprimer utilisateur":
            user = st.text_input("Utilisateur à supprimer", key="del_user")
            if st.button("Supprimer", key="btn_delete"):
                if user in users:
                    del users[user]
                    save_users(users)
                    st.success("Utilisateur supprimé ✅")
                else:
                    st.error("Utilisateur non trouvé.")

# --- FONCTION PRINCIPALE ---
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        show_main_app()
    else:
        show_welcome_page()
        show_login()

    show_admin_panel()

# --- EXÉCUTION ---
if __name__ == "__main__":
    main()
