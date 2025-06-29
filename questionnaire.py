import streamlit as st
import csv
from datetime import datetime

st.set_page_config(page_title="Questionnaire de Satisfaction - Imagerie Médicale", layout="centered")

st.title("Questionnaire de Satisfaction - Imagerie Médicale")
st.write("Merci de prendre un moment pour répondre à ce questionnaire. Votre avis est important pour améliorer notre service.")

# 1. Choix du site
site = st.selectbox(
    "Sur quel site avez-vous effectué votre examen ?",
    ["Evreux", "Vernon", "Bernay", "Verneuil"]
)

# 2. Type d'examen
examen = st.selectbox(
    "Quel examen avez-vous passé ?",
    ["Radiographie", "Scanner", "Échographie", "IRM", "Mammographie"]
)

# 3. Date de venue
date_venue = st.date_input("Quel jour êtes-vous venu(e) ?")

# 4. Comment avez-vous pris votre rendez-vous ?
prise_rdv = st.selectbox(
    "Comment avez-vous pris votre rendez-vous ?",
    [
        "Par téléphone",
        "Sur place",
        "Via Doctolib",
        "Consultation orthopédique ou pneumologie"
    ]
)

# 5. Temps d'attente estimé (en minutes)
attente = st.slider("Temps d'attente estimé (en minutes)", 0, 120, 30)

# 6. Qualité de l'accueil au secrétariat
accueil_secretaire = st.radio(
    "Comment évaluez-vous la qualité de l'accueil au secrétariat ?",
    ["Très bon", "Bon", "Moyen", "Mauvais"]
)

# 7. Qualité de l'accueil par les manipulateurs ou radiologues
accueil_manipulateur = st.radio(
    "Comment évaluez-vous la qualité de l'accueil par les manipulateurs ou radiologues ?",
    ["Très bon", "Bon", "Moyen", "Mauvais"]
)

# 8. Signalisation claire dans le service
signalisation = st.radio(
    "La signalisation dans le service était-elle claire ?",
    ["Oui", "Non", "Ne sais pas"]
)

# 9. Informations reçues après l'examen
infos_post_exam = st.radio(
    "Avez-vous reçu toutes les informations nécessaires après votre examen ?",
    ["Oui", "Non", "Partiellement"]
)

# 10. Satisfaction globale
satisfaction = st.radio(
    "Quelle est votre satisfaction globale concernant votre prise en charge ?",
    ["Très satisfait", "Satisfait", "Moyen", "Insatisfait"]
)

# 11. Commentaires ou suggestions
commentaire = st.text_area("Commentaires ou suggestions (facultatif)")

if st.button("Envoyer ma réponse"):
    date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_venue_str = date_venue.strftime("%Y-%m-%d")
    
    reponse = [
        date_heure, site, examen, date_venue_str, prise_rdv, attente,
        accueil_secretaire, accueil_manipulateur, signalisation,
        infos_post_exam, satisfaction, commentaire
    ]
    
    # Vérifie si le fichier existe pour écrire l'entête sinon pas
    try:
        with open("visualisation.csv", "x", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow([
                "Date_Envoi", "Site", "Examen", "Date_Venue", "Prise_RDV", "Attente",
                "Accueil_secretaire", "Accueil_manipulateur", "Signalisation",
                "Infos_post_exam", "Satisfaction", "Commentaire"
            ])
    except FileExistsError:
        pass  # fichier existe déjà
    
    with open("visualisation.csv", mode="a", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(reponse)
    
    st.success("Merci pour votre réponse. Elle a bien été enregistrée.")
