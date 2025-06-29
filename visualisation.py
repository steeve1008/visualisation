import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Visualisation des Résultats", layout="centered")

def charger_donnees(fichier="visualisation.csv"):
    try:
        df = pd.read_csv(fichier, sep=';', encoding='utf-8-sig')
        return df
    except FileNotFoundError:
        st.warning(f"Le fichier '{fichier}' est introuvable. Veuillez d'abord collecter des réponses.")
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

    df = charger_donnees()
    if df is None:
        return

    colonnes_non_question = ["Date", "Site", "Examen", "Commentaire", "Temps_d_attente"]

    # Filtres sur une ligne
    col1, col2 = st.columns(2)
    with col1:
        site_choisi = st.selectbox("Filtrer par site", options=["Tous"] + sorted(df['Site'].dropna().unique().tolist()))
    with col2:
        examen_choisi = st.selectbox("Filtrer par examen", options=["Tous"] + sorted(df['Examen'].dropna().unique().tolist()))

    # Appliquer filtres
    df_filtre = df.copy()
    if site_choisi != "Tous":
        df_filtre = df_filtre[df_filtre['Site'] == site_choisi]
    if examen_choisi != "Tous":
        df_filtre = df_filtre[df_filtre['Examen'] == examen_choisi]

    st.markdown(f"**Nombre de réponses affichées : {len(df_filtre)}**")

    # Choix de la question
    questions_possibles = [col for col in df.columns if col not in colonnes_non_question]
    question_choisie = st.selectbox("Choisir une question à visualiser", options=questions_possibles)

    st.subheader(f"Visualisation pour : {question_choisie}")
    plot_pie_chart(df_filtre, question_choisie)

    # Tableau des réponses filtrées
    st.subheader("Tableau des réponses filtrées")
    st.dataframe(df_filtre)

    # Bouton purge données
    if st.button("🔄 Purger les données"):
        if os.path.exists("visualisation.csv"):
            with open("visualisation.csv", "w", encoding="utf-8") as f:
                f.write("")  # vide fichier
            st.success("Données purgées avec succès !")
        else:
            st.warning("Le fichier 'visualisation.csv' n'existe pas.")

if __name__ == "__main__":
    main()
