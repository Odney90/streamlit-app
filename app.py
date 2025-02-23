import streamlit as st  
import numpy as np  
from sklearn.linear_model import LogisticRegression  
from sklearn.ensemble import RandomForestClassifier  
from scipy.stats import poisson  

# Fonctions utilitaires pour convertir les valeurs en entiers ou flottants de manière sécurisée  
def safe_int(value):  
    try:  
        return int(value)  
    except (ValueError, TypeError):  
        return 0  

def safe_float(value):  
    try:  
        return float(value)  
    except (ValueError, TypeError):  
        return 0.0  

# Initialisation des variables de prédiction  
prediction_lr = None  
prediction_rf = None  
prediction_poisson = None  

# Titre de l'application  
st.title("📊 Prédictions de Matchs de Football")  

# Formulaire pour les données des équipes  
with st.form("Données des Équipes"):  
    st.subheader("⚽ Données de l'Équipe A")  
    st.session_state.data = {  
        "score_rating_A": st.number_input("📊 Score Rating (A)", value=0.0, key="score_rating_A_input"),  
        "motivation_A": st.number_input("💪 Motivation (A)", value=0, key="motivation_A_input"),  
        "buts_marques_A": st.number_input("⚽ Buts Marqués par Match (A)", value=0.0, key="buts_marques_A_input"),  
        "tirs_par_match_A": st.number_input("🎯 Tirs par Match (A)", value=0.0, key="tirs_par_match_A_input"),  
        "possession_moyenne_A": st.number_input("⏳ Possession (%) (A)", value=0.0, key="possession_moyenne_A_input"),  
        "corners_par_match_A": st.number_input("🔄 Corners par Match (A)", value=0.0, key="corners_par_match_A_input"),  
        "forme_recente_A_victoires": st.number_input("✅ Victoires (A) sur les 5 derniers matchs", value=0, key="forme_recente_A_victoires_input"),  
        "forme_recente_A_nuls": st.number_input("➖ Nuls (A) sur les 5 derniers matchs", value=0, key="forme_recente_A_nuls_input"),  
        "forme_recente_A_defaites": st.number_input("❌ Défaites (A) sur les 5 derniers matchs", value=0, key="forme_recente_A_defaites_input"),  
    }  

    st.subheader("⚽ Données de l'Équipe B")  
    st.session_state.data.update({  
        "score_rating_B": st.number_input("📊 Score Rating (B)", value=0.0, key="score_rating_B_input"),  
        "motivation_B": st.number_input("💪 Motivation (B)", value=0, key="motivation_B_input"),  
        "buts_marques_B": st.number_input("⚽ Buts Marqués par Match (B)", value=0.0, key="buts_marques_B_input"),  
        "tirs_par_match_B": st.number_input("🎯 Tirs par Match (B)", value=0.0, key="tirs_par_match_B_input"),  
        "possession_moyenne_B": st.number_input("⏳ Possession (%) (B)", value=0.0, key="possession_moyenne_B_input"),  
        "corners_par_match_B": st.number_input("🔄 Corners par Match (B)", value=0.0, key="corners_par_match_B_input"),  
        "forme_recente_B_victoires": st.number_input("✅ Victoires (B) sur les 5 derniers matchs", value=0, key="forme_recente_B_victoires_input"),  
        "forme_recente_B_nuls": st.number_input("➖ Nuls (B) sur les 5 derniers matchs", value=0, key="forme_recente_B_nuls_input"),  
        "forme_recente_B_defaites": st.number_input("❌ Défaites (B) sur les 5 derniers matchs", value=0, key="forme_recente_B_defaites_input"),  
    })  

    submitted = st.form_submit_button("💾 Enregistrer les Données")  

# Bouton pour lancer les prédictions  
if st.button("🔮 Lancer les Prédictions"):  
    try:  
        # Calcul du score de forme récente  
        score_forme_A = (st.session_state.data["forme_recente_A_victoires"] * 3 +  
                         st.session_state.data["forme_recente_A_nuls"] * 1)  
        score_forme_B = (st.session_state.data["forme_recente_B_victoires"] * 3 +  
                         st.session_state.data["forme_recente_B_nuls"] * 1)  

        # Préparation des données pour les modèles  
        X_lr = np.array([  
            [  
                safe_float(st.session_state.data["score_rating_A"]),  
                safe_float(st.session_state.data["score_rating_B"]),  
                safe_float(st.session_state.data["possession_moyenne_A"]),  
                safe_float(st.session_state.data["possession_moyenne_B"]),  
                safe_int(st.session_state.data["motivation_A"]),  
                safe_int(st.session_state.data["motivation_B"]),  
                safe_float(st.session_state.data["tirs_par_match_A"]),  
                safe_float(st.session_state.data["tirs_par_match_B"]),  
                safe_float(st.session_state.data["corners_par_match_A"]),  
                safe_float(st.session_state.data["corners_par_match_B"]),  
                score_forme_A,  
                score_forme_B,  
            ]  
        ])  

        # Modèle de Régression Logistique  
        try:  
            # Exemple de données d'entraînement (à remplacer par vos données réelles)  
            X_train = np.array([  
                [1.0, 2.0, 50.0, 50.0, 5, 5, 5.0, 5.0, 3.0, 3.0, 10, 10],  
                [2.0, 1.0, 60.0, 40.0, 4, 6, 6.0, 4.0, 4.0, 2.0, 8, 12],  
            ])  
            y_train = np.array([1, 0])  # Exemple de labels (à remplacer par vos vraies étiquettes)  

            model_lr = LogisticRegression()  
            model_lr.fit(X_train, y_train)  # Entraînement du modèle  
            prediction_lr = model_lr.predict(X_lr.reshape(1, -1))[0]  # Prédiction  
        except Exception as e:  
            prediction_lr = "Erreur"  
            st.error(f"Erreur dans le modèle de régression logistique : {e}")  

        # Modèle Random Forest  
        try:  
            model_rf = RandomForestClassifier()  
            model_rf.fit(X_train, y_train)  # Entraînement du modèle  
            prediction_rf = model_rf.predict(X_lr.reshape(1, -1))[0]  # Prédiction  
        except Exception as e:  
            prediction_rf = "Erreur"  
            st.error(f"Erreur dans le modèle Random Forest : {e}")  

        # Modèle de Poisson  
        try:  
            # Calcul des buts attendus avec la distribution de Poisson  
            lambda_A = safe_float(st.session_state.data["buts_marques_A"])  
            lambda_B = safe_float(st.session_state.data["buts_marques_B"])  

            # Prédiction des buts avec la distribution de Poisson  
            prediction_poisson = [  
                poisson.pmf(k, lambda_A) for k in range(5)  # Probabilité de 0 à 4 buts pour l'équipe A  
            ], [  
                poisson.pmf(k, lambda_B) for k in range(5)  # Probabilité de 0 à 4 buts pour l'équipe B  
            ]  
        except Exception as e:  
            prediction_poisson = "Erreur"  
            st.error(f"Erreur dans le modèle de Poisson : {e}")  

        # Affichage des prédictions  
        st.subheader("📈 Résultats des Prédictions")  
        if prediction_lr != "Erreur":  
            st.write(f"Régression Logistique : Équipe A {prediction_lr} - Équipe B {1 - prediction_lr}")  
        if prediction_rf != "Erreur":  
            st.write(f"Random Forest : Équipe A {prediction_rf} - Équipe B {1 - prediction_rf}")  
        if prediction_poisson != "Erreur":  
            st.write("Modèle de Poisson :")  
            st.write(f"Probabilité de buts pour l'Équipe A : {prediction_poisson[0]}")  
            st.write(f"Probabilité de buts pour l'Équipe B : {prediction_poisson[1]}")  

    except Exception as e:  
        st.error(f"Une erreur s'est produite lors de la préparation des données ou de l'exécution des modèles : {e}")  

# Vérification des prédictions avant d'utiliser les variables  
if prediction_lr is not None and prediction_poisson is not None and prediction_lr != "Erreur" and prediction_poisson != "Erreur":  
    try:  
        # Calcul des value bets  
        proba_victoire_A = prediction_poisson[0][1]  # Probabilité de 1 but pour l'équipe A  
        proba_victoire_B = prediction_poisson[1][1]  # Probabilité de 1 but pour l'équipe B  
        proba_nul = 1 - (proba_victoire_A + proba_victoire_B)  

        # Calcul des value bets  
        value_bet_A = (proba_victoire_A * st.session_state.data["cote_victoire_X"]) - 1  
        value_bet_nul = (proba_nul * st.session_state.data["cote_nul"]) - 1  
        value_bet_B = (proba_victoire_B * st.session_state.data["cote_victoire_Z"]) - 1  

        # Affichage des value bets  
        st.subheader("💎 Value Bets")  
        st.write(f"Value Bet Équipe A : {value_bet_A:.2f}")  
        st.write(f"Value Bet Match Nul : {value_bet_nul:.2f}")  
        st.write(f"Value Bet Équipe B : {value_bet_B:.2f}")  

        # Recommandation de value bet  
        if value_bet_A > 0:  
            st.success("✅ Value Bet détectée pour l'Équipe A !")  
        if value_bet_nul > 0:  
            st.success("✅ Value Bet détectée pour le Match Nul !")  
        if value_bet_B > 0:  
            st.success("✅ Value Bet détectée pour l'Équipe B !")  

    except Exception as e:  
        st.error(f"Une erreur s'est produite lors du calcul des value bets : {e}")  
else:  
    st.warning("⚠️ Les prédictions ne sont pas encore disponibles ou une erreur s'est produite. Veuillez lancer les prédictions d'abord.")
