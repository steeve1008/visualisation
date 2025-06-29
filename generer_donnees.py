import csv
import random
from datetime import datetime, timedelta
import pandas as pd

# --- Données pour la simulation ---
sites = ["Evreux", "Vernon", "Bernay", "Verneuil"]
examens = ["Radiographie", "Scanner", "Échographie", "IRM", "Mammographie"]
accueil_opts = ["Très bon", "Bon", "Moyen", "Mauvais"]
satisfaction_opts = ["Très satisfait", "Satisfait", "Moyen", "Insatisfait"]
prise_rdv_opts = ["Téléphone", "Sur place", "Doctolib", "Consultation orthopédique ou pneumologie"]
signalisation_opts = ["Oui", "Non"]
infos_exam_opts = ["Oui", "Non"]

def random_date():
    start = datetime.now() - timedelta(days=60)
    end = datetime.now()
    return start + (end - start) * random.random()

# Chemin complet du fichier CSV
chemin_fichier = r"C:\Users\steev\Documents\visualisation\visualisation.csv"

# Génération du fichier
with open(chemin_fichier, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([
        "Date", "Site", "Examen", "Prise_RDV", "Attente",
        "Accueil_secretaire", "Accueil_manipulateur",
        "Signalisation", "Infos_apres_exam", "Satisfaction", "Commentaire"
    ])
    for _ in range(500):
        writer.writerow([
            random_date().strftime("%Y-%m-%d"),
            random.choice(sites),
            random.choice(examens),
            random.choice(prise_rdv_opts),
            random.randint(0, 120),
            random.choice(accueil_opts),
            random.choice(accueil_opts),
            random.choice(signalisation_opts),
            random.choice(infos_exam_opts),
            random.choice(satisfaction_opts),
            ""
        ])

print(f"Fichier généré avec succès : {chemin_fichier}")

# Lecture et analyse avec pandas
df = pd.read_csv(chemin_fichier, sep=';', encoding='utf-8-sig')

print("\nAperçu des données :")
print(df.head())

print("\nNombre de réponses par site :")
print(df['Site'].value_counts())

print("\nRépartition de la satisfaction par site :")
print(df.groupby(['Site', 'Satisfaction']).size().unstack(fill_value=0))
