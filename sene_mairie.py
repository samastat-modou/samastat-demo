import streamlit as st
import json
import bcrypt
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# --- PARAMÈTRES ---
LOGO_PATH = "logo.png"
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
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        st.error("Erreur: Le fichier des utilisateurs est corrompu. Supprimez-le ou corrigez-le.")
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password: str) -> str:
    """Hache un mot de passe et le retourne en chaîne de caractères."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    """Vérifie un mot de passe par rapport à son hachage."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def verify_user(username, password):
    users = load_users()
    if username not in users:
        return False
    return check_password(password, users[username])

# --- PAGE D'ACCUEIL ---
def show_welcome_page():
    st.set_page_config(page_title="SamaStat Mairie", layout="centered")
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=250)
    st.title("Bienvenue sur SamaStat Mairie")
    st.markdown(
        "### Votre plateforme de veille statistique au service des collectivités locales.\n"
        "Accédez à des indicateurs clés, rapports et prévisions pour mieux piloter vos actions."
    )
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

# --- ADMINISTRATION ---
def show_admin_panel():
    st.sidebar.header("🔧 Administration des comptes")
    action = st.sidebar.radio("Choisir une action :", [
        "Créer un compte", "Modifier le mot de passe", "Supprimer un utilisateur"])
    users = load_users()

    if action == "Créer un compte":
        new_user = st.sidebar.text_input("🔤 Nouveau nom d'utilisateur", key="create_user")
        new_pass = st.sidebar.text_input("🔑 Nouveau mot de passe", type="password", key="create_pass")
        if st.sidebar.button("Créer le compte"):
            if new_user in users:
                st.sidebar.warning("Ce nom d'utilisateur existe déjà.")
            elif new_user == "" or new_pass == "":
                st.sidebar.error("Veuillez remplir tous les champs.")
            else:
                users[new_user] = hash_password(new_pass)
                save_users(users)
                st.sidebar.success(f"Compte '{new_user}' créé ✅")

    elif action == "Modifier le mot de passe":
        user = st.sidebar.text_input("Nom d'utilisateur existant", key="mod_user")
        old_pass = st.sidebar.text_input("Mot de passe actuel", type="password", key="mod_old")
        new_pass = st.sidebar.text_input("Nouveau mot de passe", type="password", key="mod_new")
        if st.sidebar.button("Mettre à jour le mot de passe"):
            if user not in users:
                st.sidebar.error("Utilisateur introuvable.")
            elif not check_password(old_pass, users[user]):
                st.sidebar.error("Mot de passe actuel incorrect.")
            elif new_pass == "":
                st.sidebar.error("Nouveau mot de passe vide.")
            else:
                users[user] = hash_password(new_pass)
                save_users(users)
                st.sidebar.success("Mot de passe mis à jour ✅")

    elif action == "Supprimer un utilisateur":
        user_to_delete = st.sidebar.text_input("Nom d'utilisateur à supprimer", key="del_user")
        if st.sidebar.button("Supprimer le compte"):
            if user_to_delete in users:
                del users[user_to_delete]
                save_users(users)
                st.sidebar.success(f"Compte '{user_to_delete}' supprimé ✅")
            else:
                st.sidebar.error("Utilisateur non trouvé.")

# --- PRÉVISIONS ---
def generate_forecast_data():
    years = list(range(2015, 2025))
    np.random.seed(42)
    data = {
        "Année": years,
        "Naissances": np.round(np.linspace(1500, 1800, len(years)) + np.random.normal(0, 50, len(years))),
        "Décès": np.round(np.linspace(400, 500, len(years)) + np.random.normal(0, 20, len(years))),
        "Budget Municipal (M CFA)": np.round(np.linspace(900, 1300, len(years)) + np.random.normal(0, 80, len(years))),
        "Permis de construire": np.round(np.linspace(100, 250, len(years)) + np.random.normal(0, 10, len(years))),
        "Zones inondables recensées": np.round(np.linspace(60, 30, len(years)) + np.random.normal(0, 5, len(years)))
    }
    df = pd.DataFrame(data)
    future_years = np.array([[2025], [2026], [2027]])
    predictions = {}
    for col in df.columns[1:]:
        model = LinearRegression()
        model.fit(df[["Année"]], df[[col]])
        pred_values = model.predict(future_years).flatten()
        predictions[col] = np.round(pred_values)
    df_preds = pd.DataFrame({"Année": [2025, 2026, 2027], **{k: v for k, v in predictions.items()}})
    df_all = pd.concat([df, df_preds], ignore_index=True)
    return df_all

# --- TABLEAUX DE BORD ---
def show_full_dashboard():
    st.title("📈 Prévisions Communales")
    df = generate_forecast_data()
    st.dataframe(df, use_container_width=True)
    
    st.subheader("Prévisions par indicateur")
    for col in df.columns[1:]:
        st.markdown(f"**{col}**")
        
        # Graphique en ligne pour la tendance
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df["Année"], df[col], marker='o', label="Données")
        ax.set_xlabel("Année")
        ax.set_ylabel(col)
        ax.set_title(f"Évolution de {col}")
        
        # Séparez les données réelles des prévisions pour une meilleure visualisation
        real_data = df[df['Année'] < 2025]
        forecast_data = df[df['Année'] >= 2025]
        
        ax.plot(forecast_data["Année"], forecast_data[col], marker='o', linestyle='--', color='red', label="Prévisions")
        ax.legend()
        st.pyplot(fig)

# --- LOGIQUE PRINCIPALE ---
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.sidebar.markdown(f"👤 Connecté en tant que **{st.session_state.username}**")
        if st.sidebar.button("🔓 Se déconnecter"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
        show_full_dashboard()
    else:
        show_welcome_page()
        show_login()

    st.sidebar.markdown("---")
    with st.sidebar.expander("🔐 Zone Admin (facultative)"):
        show_admin_panel()

if __name__ == "__main__":
    main()