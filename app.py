import streamlit as st  
import numpy as np  
import pandas as pd  
from scipy.stats import poisson  
from sklearn.linear_model import LogisticRegression  
from sklearn.ensemble import RandomForestClassifier  
import matplotlib.pyplot as plt  

# Initialisation des données dans session_state  
if "data" not in st.session_state:  
    st.session_state.data = {  
        # Équipe A  
        "score_rating_A": 70.0,  
        "buts_par_match_A": 1.5,  
        "buts_concedes_par_match_A": 1.0,  
        "possession_moyenne_A": 55.0,  
        "expected_but_A": 1.8,  
        "expected_concedes_A": 1.2,  
        "tirs_cadres_A": 120.0,  
        "grandes_chances_A": 25.0,  
        "passes_reussies_A": 400.0,  
        "corners_A": 60.0,  
        "interceptions_A": 50.0,  
        "tacles_reussis_A": 40.0,  
        "fautes_A": 15.0,  
        "cartons_jaunes_A": 5.0,  
        "cartons_rouges_A": 1.0,  
        "joueurs_cles_absents_A": 0,  
        "motivation_A": 3,  
        "clean_sheets_gardien_A": 2.0,  
        "ratio_tirs_arretes_A": 0.75,  
        "victoires_domicile_A": 60.0,  
        "passes_longues_A": 50.0,  
        "dribbles_reussis_A": 10.0,  
        "ratio_tirs_cadres_A": 0.4,  
        "grandes_chances_manquees_A": 5.0,  
        "fautes_zones_dangereuses_A": 3.0,  
        "buts_corners_A": 2.0,  
        "jours_repos_A": 4.0,  
        "matchs_30_jours_A": 8.0,  
        
        # Équipe B  
        "score_rating_B": 65.0,  
        "buts_par_match_B": 1.0,  
        "buts_concedes_par_match_B": 1.5,  
        "possession_moyenne_B": 45.0,  
        "expected_but_B": 1.2,  
        "expected_concedes_B": 1.8,  
        "tirs_cadres_B": 100.0,  
        "grandes_chances_B": 20.0,  
        "passes_reussies_B": 350.0,  
        "corners_B": 50.0,  
        "interceptions_B": 40.0,  
        "tacles_reussis_B": 35.0,  
        "fautes_B": 20.0,  
        "cartons_jaunes_B": 6.0,  
        "cartons_rouges_B": 2.0,  
        "joueurs_cles_absents_B": 0,  
        "motivation_B": 3,  
        "clean_sheets_gardien_B": 1.0,  
        "ratio_tirs_arretes_B": 0.65,  
        "victoires_exterieur_B": 40.0,  
        "passes_longues_B": 40.0,  
        "dribbles_reussis_B": 8.0,  
        "ratio_tirs_cadres_B": 0.35,  
        "grandes_chances_manquees_B": 6.0,  
        "fautes_zones_dangereuses_B": 4.0,  
        "buts_corners_B": 1.0,  
        "jours_repos_B": 3.0,  
        "matchs_30_jours_B": 9.0,  
        
        # Conditions du match  
        "conditions_match": "",  
    }  

# Titre de l'application  
st.title("⚽ Analyse de Prédiction de Matchs de Football")  
st.markdown("Renseignez les critères suivants pour prédire le résultat du match :")  

# Section 1 : Statistiques des Équipes  
st.header("📊 Statistiques des Équipes")  

col_a, col_b = st.columns(2)  

# Équipe A  
with col_a:  
    st.subheader("Équipe A 🟡")  
    st.session_state.data["score_rating_A"] = st.number_input(  
        "⭐ Score Rating (Équipe A)",  
        min_value=0.0,  
        value=float(st.session_state.data["score_rating_A"]),  
        key="score_rating_A_input"  
    )  
    st.session_state.data["buts_par_match_A"] = st.number_input(  
        "⚽ Buts par match (Équipe A)",  
        min_value=0.0,  
        value=float(st.session_state.data["buts_par_match_A"]),  
        key="buts_par_match_A_input"  
    )  
    st.session_state.data["buts_concedes_par_match_A"] = st.number_input(  
        "🥅 Buts concédés par match (Équipe A)",  
        min_value=0.0,  
        value=float(st.session_state.data["buts_concedes_par_match_A"]),  
        key="buts_concedes_par_match_A_input"  
    )  
    st.session_state.data["possession_moyenne_A"] = st.number_input(  
        "🔄 Possession moyenne (Équipe A)",  
        min_value=0.0,  
        max_value=100.0,  
        value=float(st.session_state.data["possession_moyenne_A"]),  
        key="possession_moyenne_A_input"  
    )  
    st.session_state.data["joueurs_cles_absents_A"] = st.number_input(  
        "🚑 Joueurs clés absents (Équipe A)",  
        min_value=0,  
        value=int(st.session_state.data["joueurs_cles_absents_A"]),  
        key="joueurs_cles_absents_A_input"  
    )  

# Équipe B  
with col_b:  
    st.subheader("Équipe B 🔴")  
    st.session_state.data["score_rating_B"] = st.number_input(  
        "⭐ Score Rating (Équipe B)",  
        min_value=0.0,  
        value=float(st.session_state.data["score_rating_B"]),  
        key="score_rating_B_input"  
    )  
    st.session_state.data["buts_par_match_B"] = st.number_input(  
        "⚽ Buts par match (Équipe B)",  
        min_value=0.0,  
        value=float(st.session_state.data["buts_par_match_B"]),  
        key="buts_par_match_B_input"  
    )  
    st.session_state.data["buts_concedes_par_match_B"] = st.number_input(  
        "🥅 Buts concédés par match (Équipe B)",  
        min_value=0.0,  
        value=float(st.session_state.data["buts_concedes_par_match_B"]),  
        key="buts_concedes_par_match_B_input"  
    )  
    st.session_state.data["possession_moyenne_B"] = st.number_input(  
        "🔄 Possession moyenne (Équipe B)",  
        min_value=0.0,  
        max_value=100.0,  
        value=float(st.session_state.data["possession_moyenne_B"]),  
        key="possession_moyenne_B_input"  
    )  
    st.session_state.data["joueurs_cles_absents_B"] = st.number_input(  
        "🚑 Joueurs clés absents (Équipe B)",  
        min_value=0,  
        value=int(st.session_state.data["joueurs_cles_absents_B"]),  
        key="joueurs_cles_absents_B_input"  
    )  

# Section 2 : Conditions du Match et Motivation  
st.header("🌦️ Conditions du Match et Motivation")  
col_a, col_b = st.columns(2)  

# Conditions du Match  
with col_a:  
    st.session_state.data["conditions_match"] = st.text_input(  
        "🌧️ Conditions du Match (ex : pluie, terrain sec, etc.)",  
        value=st.session_state.data["conditions_match"],  
        key="conditions_match_input"  
    )  

# Motivation  
with col_b:  
    st.session_state.data["motivation_A"] = st.slider(  
        "💪 Motivation de l'Équipe A (1 à 5)",  
        min_value=1,  
        max_value=5,  
        value=int(st.session_state.data["motivation_A"]),  
        key="motivation_A_slider"  
    )  
    st.session_state.data["motivation_B"] = st.slider(  
        "💪 Motivation de l'Équipe B (1 à 5)",  
        min_value=1,  
        max_value=5,  
        value=int(st.session_state.data["motivation_B"]),  
        key="motivation_B_slider"  
    )  

# Section 3 : Prédictions  
st.header("🔮 Prédictions")  
if st.button("Prédire le résultat"):  
    # Prédiction des Buts avec Poisson  
    avg_goals_A = st.session_state.data["buts_par_match_A"]  
    avg_goals_B = st.session_state.data["buts_par_match_B"]  
    prob_0_0 = poisson.pmf(0, avg_goals_A) * poisson.pmf(0, avg_goals_B)  
    prob_1_1 = poisson.pmf(1, avg_goals_A) * poisson.pmf(1, avg_goals_B)  
    prob_2_2 = poisson.pmf(2, avg_goals_A) * poisson.pmf(2, avg_goals_B)  

    # Génération de données d'entraînement factices pour la régression logistique  
    np.random.seed(42)  
    X_lr = np.random.rand(100, 6) * 100  # 100 échantillons, 6 caractéristiques  
    y_lr = np.random.randint(0, 2, 100)  # 100 labels binaires (0 ou 1)  

    # Régression Logistique  
    model_lr = LogisticRegression()  
    model_lr.fit(X_lr, y_lr)  
    X_lr_pred = np.array([  
        [  
            st.session_state.data["score_rating_A"],  
            st.session_state.data["score_rating_B"],  
            st.session_state.data["possession_moyenne_A"],  
            st.session_state.data["possession_moyenne_B"],  
            st.session_state.data["motivation_A"],  
            st.session_state.data["motivation_B"],  
        ]  
    ])  
    prediction_lr = model_lr.predict(X_lr_pred)  

    # Génération de données d'entraînement factices pour Random Forest  
    X_rf = np.random.rand(100, 50) * 100  # 100 échantillons, 50 caractéristiques  
    y_rf = np.random.randint(0, 2, 100)  # 100 labels binaires (0 ou 1)  

    # Random Forest  
    model_rf = RandomForestClassifier()  
    model_rf.fit(X_rf, y_rf)  
    X_rf_pred = np.array([  
        [  
            st.session_state.data["score_rating_A"],  
            st.session_state.data["score_rating_B"],  
            st.session_state.data["buts_par_match_A"],  
            st.session_state.data["buts_par_match_B"],  
            st.session_state.data["possession_moyenne_A"],  
            st.session_state.data["possession_moyenne_B"],  
            st.session_state.data["joueurs_cles_absents_A"],  
            st.session_state.data["joueurs_cles_absents_B"],  
            st.session_state.data["motivation_A"],  
            st.session_state.data["motivation_B"],  
            st.session_state.data["expected_but_A"],  
            st.session_state.data["expected_but_B"],  
            st.session_state.data["tirs_cadres_A"],  
            st.session_state.data["tirs_cadres_B"],  
            st.session_state.data["grandes_chances_A"],  
            st.session_state.data["grandes_chances_B"],  
            st.session_state.data["passes_reussies_A"],  
            st.session_state.data["passes_reussies_B"],  
            st.session_state.data["corners_A"],  
            st.session_state.data["corners_B"],  
            st.session_state.data["interceptions_A"],  
            st.session_state.data["interceptions_B"],  
            st.session_state.data["tacles_reussis_A"],  
            st.session_state.data["tacles_reussis_B"],  
            st.session_state.data["fautes_A"],  
            st.session_state.data["fautes_B"],  
            st.session_state.data["cartons_jaunes_A"],  
            st.session_state.data["cartons_jaunes_B"],  
            st.session_state.data["cartons_rouges_A"],  
            st.session_state.data["cartons_rouges_B"],  
            st.session_state.data["clean_sheets_gardien_A"],  
            st.session_state.data["clean_sheets_gardien_B"],  
            st.session_state.data["ratio_tirs_arretes_A"],  
            st.session_state.data["ratio_tirs_arretes_B"],  
            st.session_state.data["victoires_domicile_A"],  
            st.session_state.data["victoires_exterieur_B"],  
            st.session_state.data["passes_longues_A"],  
            st.session_state.data["passes_longues_B"],  
            st.session_state.data["dribbles_reussis_A"],  
            st.session_state.data["dribbles_reussis_B"],  
            st.session_state.data["ratio_tirs_cadres_A"],  
            st.session_state.data["ratio_tirs_cadres_B"],  
            st.session_state.data["grandes_chances_manquees_A"],  
            st.session_state.data["grandes_chances_manquees_B"],  
            st.session_state.data["fautes_zones_dangereuses_A"],  
            st.session_state.data["fautes_zones_dangereuses_B"],  
            st.session_state.data["buts_corners_A"],  
            st.session_state.data["buts_corners_B"],  
            st.session_state.data["jours_repos_A"],  
            st.session_state.data["jours_repos_B"],  
            st.session_state.data["matchs_30_jours_A"],  
            st.session_state.data["matchs_30_jours_B"],  
        ]  
    ])  
    prediction_rf = model_rf.predict(X_rf_pred)  

    # Affichage des résultats  
    st.subheader("Résultats des Prédictions")  
    st.write(f"📊 **Probabilité de 0-0 (Poisson)** : {prob_0_0:.2%}")  
    st.write(f"📊 **Probabilité de 1-1 (Poisson)** : {prob_1_1:.2%}")  
    st.write(f"📊 **Probabilité de 2-2 (Poisson)** : {prob_2_2:.2%}")  
    st.write(f"📊 **Régression Logistique** : {'Équipe A' if prediction_lr[0] == 1 else 'Équipe B'}")  
    st.write(f"🌲 **Random Forest** : {'Équipe A' if prediction_rf[0] == 1 else 'Équipe B'}")  

# Section 4 : Bankroll et Value Bet  
st.header("💶 Bankroll et Value Bet")  
col_a, col_b = st.columns(2)  

# Cote Implicite et Value Bet  
with col_a:  
    cote = st.number_input(  
        "📈 Cote offerte",  
        min_value=1.0,  
        value=2.0,  
        key="cote_input"  
    )  
    prob_victoire = st.number_input(  
        "🎯 Probabilité de victoire (en %)",  
        min_value=0.0,  
        max_value=100.0,  
        value=50.0,  
        key="prob_victoire_input"  
    )  
    cote_implicite = 100 / prob_victoire  
    value_bet = (cote * prob_victoire / 100) - 1  
    st.write(f"📊 **Cote Implicite** : {cote_implicite:.2f}")  
    st.write(f"📊 **Value Bet** : {value_bet:.2%}")  

# Mise de Kelly  
with col_b:  
    bankroll = st.number_input(  
        "💰 Bankroll (en €)",  
        min_value=0.0,  
        value=100.0,  
        key="bankroll_input"  
    )  
    mise_kelly = (prob_victoire / 100 * (cote - 1) - (1 - prob_victoire / 100)) / (cote - 1)  
    mise_kelly = max(0, mise_kelly)  # Éviter les valeurs négatives  
    st.write(f"💶 **Mise de Kelly recommandée** : {mise_kelly * bankroll:.2f} €")  

# Section 5 : Visuels  
st.header("📈 Visuels")  
col_a, col_b = st.columns(2)  

# Graphique des buts  
with col_a:  
    fig, ax = plt.subplots()  
    ax.bar(["Équipe A", "Équipe B"], [st.session_state.data["buts_par_match_A"], st.session_state.data["buts_par_match_B"]], color=["yellow", "red"])  
    ax.set_title("⚽ Buts par match")  
    st.pyplot(fig)  

# Graphique de possession  
with col_b:  
    fig, ax = plt.subplots()  
    ax.bar(["Équipe A", "Équipe B"], [st.session_state.data["possession_moyenne_A"], st.session_state.data["possession_moyenne_B"]], color=["yellow", "red"])  
    ax.set_title("🔄 Possession moyenne")  
    st.pyplot(fig)
