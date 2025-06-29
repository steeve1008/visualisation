import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import csv
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Visualisation des Résultats", layout="centered")

# Génération automatique du fichier CSV si absent
def generer_donnees(fichier="visualisation.csv"):
    if os.path.exists(fichier):
        return
    sites = ["Evreux", "Vernon", "Bernay", "Verneuil"]
    examens = ["Radiographie", "Scanner", "Échographie", "IRM", "Mammographie"]
    accueil_opts = ["Très bon", "Bon", "Moyen", "Mauvais"]
    satisfaction_opts = ["Très satisfait", "Satisfait", "Moyen", "Insatisfait"]
    prise_rdv_opts = [
        "Téléphone", "Sur place", "Doctolib",
        "Consultation orthopédique ou pneumologie"
    ]
    signalisation_opts = ["Oui", "Non"]
    infos_exam_opts = ["Oui", "Non"]

    def random_date():
        start = datetime.now() - timedelta(days=60)
        end = datetime.now()
        return start + (end - start) * random.random()

    with open(fichier, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([
            "Date", "Site", "Examen", "Prise_RDV", "Attente",
            "Accueil_secretaire", "Accueil_manipulateur",
            "Signalisation", "Infos_apres_exam", "Satisfaction", "Commentaire"
        ])

        for _ in range(500):
            date = random_date().strftime("%Y-%m-%d")
            site = random.choice(sites)
            examen = random.choice(examens)
            prise_rdv = random.choice(prise_rdv_opts)
            attente = random.randint(0, 120)
            accueil_sec = random.choice(accueil_opts)
            accueil_manip = random.choice(accueil_opts)
            signalisation = random.choice(signalisation_opts)
            infos_exam = random.choice(infos_exam_opts)
            satisfaction = random.choice(satisfaction_opts)
            commentaire = ""

            writer.writerow([
                date, site, examen, prise_rdv, attente, accueil_sec, accueil_manip,
                signalisation, infos_exam, satisfaction, commentaire
            ])

# Chargement des données
def charger_donnees(fichier="visualisation.csv"):
    try:
        df = pd.read_csv(fichier, sep=';', encoding='utf-8-sig')
        return df
    except FileNotFoundError:
        st.warning(f"Le fichier '{fichier}' est introuvable dans l’app.")
        return None
    except Exception as e:
        st.error(f"Erreur lors de la lecture des données : {e}")
        return None

# Affichage graphique en camembert
def plot_pie_chart(df, column):
    if column not in df.columns:
        st.warning(f"Colonne manquante : {column}")
        return
    counts = df[column].value_counts(dropna=False)
    labels = counts.index.tolist()
    values = counts.values
    colors = sns.color_palette("Set2", len(labels))

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    ax.axis('equal')
    st.pyplot(fig)

def main():
    st.title("📊 Visualisation des Résultats - Imagerie Médicale")

    generer_donnees()
    df = charger_donnees()
    if df is None:
        return

    colonnes_non_question = ["Date", "Site", "Examen", "Commentaire", "Attente"]

    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        site_choisi = st.selectbox("Filtrer par site", options=["Tous"] + sorted(df['Site'].dropna().unique().tolist()))
    with col2:
        examen_choisi = st.selectbox("Filtrer par examen", options=["Tous"] + sorted(df['Examen'].dropna().unique().tolist()))

    df_filtre = df.copy()
    if site_choisi != "Tous":
        df_filtre = df_filtre[df_filtre['Site'] == site_choisi]
    if examen_choisi != "Tous":
        df_filtre = df_filtre[df_filtre['Examen'] == examen_choisi]

    st.markdown(f"**Nombre de réponses affichées : {len(df_filtre)}**")

    questions_possibles = [col for col in df.columns if col not in colonnes_non_question]
    question_choisie = st.selectbox("Choisir une question à visualiser", options=questions_possibles)

    st.subheader(f"Visualisation pour : {question_choisie}")
    plot_pie_chart(df_filtre, question_choisie)

    st.subheader("Tableau des réponses filtrées")
    st.dataframe(df_filtre)

    if st.button("🔄 Purger les données"):
        if os.path.exists("visualisation.csv"):
            with open("visualisation.csv", "w", encoding="utf-8") as f:
                f.write("")  # vide fichier
            st.success("Données purgées avec succès !")
        else:
            st.warning("Le fichier 'visualisation.csv' n'existe pas.")

if __name__ == "__main__":
    main()
