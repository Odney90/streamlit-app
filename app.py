import streamlit as st  
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
from io import BytesIO  
from scipy.special import factorial  
from sklearn.linear_model import LogisticRegression  
from sklearn.ensemble import RandomForestClassifier  
from xgboost import XGBClassifier  
from docx import Document  

# Fonction pour prédire avec le modèle Poisson  
def poisson_prediction(home_goals, away_goals):  
    home_prob = np.exp(-home_goals) * (home_goals ** home_goals) / factorial(home_goals)  
    away_prob = np.exp(-away_goals) * (away_goals ** away_goals) / factorial(away_goals)  
    return home_prob, away_prob  

# Fonction pour créer un document Word avec les résultats  
def create_doc(results):  
    doc = Document()  
    doc.add_heading('Analyse de Matchs de Football et Prédictions de Paris Sportifs', level=1)  

    # Ajout des données des équipes  
    doc.add_heading('Données des Équipes', level=2)  
    doc.add_paragraph(f"Équipe Domicile: {results['Équipe Domicile']}")  
    doc.add_paragraph(f"Équipe Extérieure: {results['Équipe Extérieure']}")  
    doc.add_paragraph(f"Buts Prédit Domicile: {results['Buts Prédit Domicile']:.2f}")  
    doc.add_paragraph(f"Buts Prédit Extérieur: {results['Buts Prédit Extérieur']:.2f}")  

    # Ajout des probabilités des modèles  
    doc.add_heading('Probabilités des Modèles', level=2)  
    doc.add_paragraph(f"Probabilité Domicile: {results['Probabilité Domicile']:.2f}")  
    doc.add_paragraph(f"Probabilité Nul: {results['Probabilité Nul']:.2f}")  
    doc.add_paragraph(f"Probabilité Extérieure: {results['Probabilité Extérieure']:.2f}")  

    # Enregistrement du document  
    buffer = BytesIO()  
    doc.save(buffer)  
    buffer.seek(0)  
    return buffer  

# Fonction pour entraîner et prédire avec les modèles  
@st.cache_resource  
def train_models():  
    # Créer un ensemble de données d'entraînement fictif  
    data = pd.DataFrame({  
        'home_goals': np.random.randint(0, 3, size=50),  
        'away_goals': np.random.randint(0, 3, size=50),  
        'home_xG': np.random.uniform(0, 2, size=50),  
        'away_xG': np.random.uniform(0, 2, size=50),  
        'home_defense': np.random.randint(0, 3, size=50),  
        'away_defense': np.random.randint(0, 3, size=50),  
        'result': np.random.choice([0, 1, 2], size=50)  
    })  

    # Séparer les caractéristiques et la cible  
    X = data[['home_goals', 'away_goals', 'home_xG', 'away_xG', 'home_defense', 'away_defense']]  
    y = data['result']  

    # Modèle de régression logistique  
    log_reg = LogisticRegression(max_iter=100)  
    log_reg.fit(X, y)  

    # Modèle Random Forest  
    rf = RandomForestClassifier(n_estimators=10)  
    rf.fit(X, y)  

    # Modèle XGBoost  
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', n_estimators=10)  
    xgb.fit(X, y)  

    return log_reg, rf, xgb  

# Vérifier si les modèles sont déjà chargés dans l'état de session  
if 'models' not in st.session_state:  
    st.session_state.models = train_models()  

log_reg_model, rf_model, xgb_model = st.session_state.models  

# Interface utilisateur  
st.title("🏆 Analyse de Matchs de Football et Prédictions de Paris Sportifs")  

# Saisie des données des équipes  
st.header("Saisie des données des équipes")  
col1, col2 = st.columns(2)  

with col1:  
    home_team = st.text_input("Nom de l'équipe à domicile", value="Équipe A")  
    st.subheader("Statistiques de l'équipe à domicile")  
    home_stats = {  
        "moyenne_buts_marques": st.number_input("Moyenne de buts marqués par match (domicile)", min_value=0.0, value=2.5),  
        "xG": st.number_input("xG (Expected Goals) (domicile)", min_value=0.0, value=2.0),  
        "moyenne_buts_encais": st.number_input("Moyenne de buts encaissés par match (domicile)", min_value=0.0, value=1.0),  
    }  

with col2:  
    away_team = st.text_input("Nom de l'équipe à l'extérieur", value="Équipe B")  
    st.subheader("Statistiques de l'équipe à l'extérieur")  
    away_stats = {  
        "moyenne_buts_marques": st.number_input("Moyenne de buts marqués par match (extérieur)", min_value=0.0, value=1.5),  
        "xG": st.number_input("xG (Expected Goals) (extérieur)", min_value=0.0, value=1.8),  
        "moyenne_buts_encais": st.number_input("Moyenne de buts encaissés par match (extérieur)", min_value=0.0, value=2.0),  
    }  

# Saisie des cotes des bookmakers  
st.header("Saisie des cotes des bookmakers")  
odds_home = 1.8  # Cote pour l'équipe à domicile  
odds_away = 2.2  # Cote pour l'équipe à l'extérieur  
st.write(f"**Cote pour {home_team} :** {odds_home}")  
st.write(f"**Cote pour {away_team} :** {odds_away}")  

# Prédictions  
if st.button("🔍 Prédire les résultats"):  
    # Calcul des buts prédit  
    home_goals = home_stats["moyenne_buts_marques"] + home_stats["xG"] - away_stats["moyenne_buts_encais"]  
    away_goals = away_stats["moyenne_buts_marques"] + away_stats["xG"] - home_stats["moyenne_buts_encais"]  
    
    home_prob, away_prob = poisson_prediction(home_goals, away_goals)  

    # Prédictions avec les modèles  
    input_data = [[home_stats['moyenne_buts_marques'], away_stats['moyenne_buts_marques'], home_stats['xG'], away_stats['xG']]]  
    try:  
        log_reg_prob = log_reg_model.predict_proba(input_data)[0]  
        rf_prob = rf_model.predict_proba(input_data)[0]  
        xgb_prob = xgb_model.predict_proba(input_data)[0]  
    except Exception as e:  
        st.error(f"Erreur lors de la prédiction : {e}")  
        log_reg_prob, rf_prob, xgb_prob = None, None, None  

    # Affichage des résultats  
    st.subheader("📊 Résultats des Prédictions")  

    # Tableau pour le modèle de Poisson  
    poisson_results = pd.DataFrame({  
        "Équipe": [home_team, away_team],  
        "Buts Prédit": [f"{home_goals:.2f} (🔵{home_prob * 100:.2f}%)", f"{away_goals:.2f} (🔵{away_prob * 100:.2f}%)"]  
    })  

    st.markdown("### Résultats du Modèle de Poisson")  
    st.dataframe(poisson_results)  

    # Détails sur chaque prédiction des modèles  
    st.markdown("### Détails des Prédictions des Modèles")  
    model_details = {  
        "Modèle": ["Régression Logistique", "Random Forest", "XGBoost"],  
        "Victoire Domicile (%)": [log_reg_prob[2] * 100 if log_reg_prob is not None else None,  
                                  rf_prob[2] * 100 if rf_prob is not None else None,  
                                  xgb_prob[2] * 100 if xgb_prob is not None else None],  
        "Match Nul (%)": [log_reg_prob[1] * 100 if log_reg_prob is not None else None,  
                          rf_prob[1] * 100 if rf_prob is not None else None,  
                          xgb_prob[1] * 100 if xgb_prob is not None else None],  
        "Victoire Extérieure (%)": [log_reg_prob[0] * 100 if log_reg_prob is not None else None,  
                                    rf_prob[0] * 100 if rf_prob is not None else None,  
                                    xgb_prob[0] * 100 if xgb_prob is not None else None],  
    }  
    model_details_df = pd.DataFrame(model_details)  
    st.dataframe(model_details_df)  

    # Explication des modèles  
    st.subheader("📊 Explication des Modèles")  
    st.write("""  
    - **Régression Logistique** : Modèle utilisé pour prédire la probabilité d'un événement binaire.  
    - **Random Forest** : Modèle d'ensemble qui utilise plusieurs arbres de décision pour améliorer la précision.  
    - **XGBoost** : Modèle d'apprentissage par boosting qui est très efficace pour les compétitions de machine learning.  
    """)  

    # Option de téléchargement des résultats  
    results = {  
        "Équipe Domicile": home_team,  
        "Équipe Extérieure": away_team,  
        "Buts Prédit Domicile": home_goals,  
        "Buts Prédit Extérieur": away_goals,  
        "Probabilité Domicile": log_reg_prob[2] if log_reg_prob is not None else None,  
        "Probabilité Nul": log_reg_prob[1] if log_reg_prob is not None else None,  
        "Probabilité Extérieure": log_reg_prob[0] if log_reg_prob is not None else None,  
    }  

    if st.button("📥 Télécharger les résultats en DOC"):  
        buffer = create_doc(results)  
        st.download_button(  
            label="Télécharger les résultats",  
            data=buffer,  
            file_name="predictions.docx",  
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"  
        )
