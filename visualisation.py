import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import csv
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Visualisation des Résultats", layout="centered")

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
        delta = end - start
        random_seconds = random.randint(0, int(delta.total_seconds()))
        return start + timedelta(seconds=random_seconds)

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

    sites_possibles = sorted(df['Site'].dropna().unique().tolist())
    site_choisi = st.multiselect(
        "Filtrer par site",
        options=sites_possibles,
        default=sites_possibles
    )
    if not site_choisi:
        site_choisi = sites_possibles

    examens_possibles = sorted(df['Examen'].dropna().unique().tolist())
    examen_choisi = st.multiselect(
        "Filtrer par examen",
        options=examens_possibles,
        default=examens_possibles
    )
    if not examen_choisi:
        examen_choisi = examens_possibles

    df_filtre = df.copy()
    if site_choisi and len(site_choisi) != len(sites_possibles):
        df_filtre = df_filtre[df_filtre['Site'].isin(site_choisi)]

    if examen_choisi and len(examen_choisi) != len(examens_possibles):
        df_filtre = df_filtre[df_filtre['Examen'].isin(examen_choisi)]

    st.markdown(f"**Nombre de réponses affichées : {len(df_filtre)}**")

    questions_possibles = [col for col in df.columns if col not in colonnes_non_question]

    question_choisie = st.selectbox("Choisir une question à visualiser", options=questions_possibles)

    st.subheader(f"Visualisation pour : {question_choisie}")
    plot_pie_chart(df_filtre, question_choisie)

    st.subheader("Tableau des réponses filtrées")
    st.dataframe(df_filtre)

    if st.button("🔄 Purger les données"):
        if os.path.exists("visualisation.csv"):
            os.remove("visualisation.csv")
            generer_donnees()
            st.success("Données purgées et fichier recréé avec succès !")
        else:
            st.warning("Le fichier 'visualisation.csv' n'existe pas.")

if __name__ == "__main__":
    main()
