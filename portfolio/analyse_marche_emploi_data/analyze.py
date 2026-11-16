# /// script
# dependencies = [
#   "pandas",
#   "numpy",
# ]
# ///

import os
import json
import re
import logging
import pandas as pd
import numpy as np
from datetime import datetime

# Configurer les logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

RAW_DATA_PATH = "raw_jobs.json"
CLEANED_CSV_PATH = "cleaned_jobs.csv"
JS_DATA_PATH = "dashboard_data.js"

# Liste de compétences cibles à extraire pour uniformiser l'analyse
TARGET_SKILLS = [
    "Python", "SQL", "Power BI", "R", "Spark", "Docker", "AWS", "PyTorch", 
    "TensorFlow", "Tableau", "Excel", "Git", "Kubernetes", "Azure", "GCP", 
    "Snowflake", "dbt", "Airflow", "MLflow", "Agile", "NoSQL", "CI/CD"
]

def parse_salary(salary_str, contract):
    """
    Parse les chaînes de salaire complexes pour en extraire un montant annuel numérique en EUR.
    Exemples gérés :
    - "45k €" -> 45000
    - "38 000 €" -> 38000
    - "45k - 55k €" -> 50000 (moyenne)
    - "TJM 500€" -> 500 * 210 = 105000
    - "Non indiqué" -> NaN
    """
    if not isinstance(salary_str, str) or salary_str.lower() in ["non indiqué", "non indique", ""]:
        return np.nan
    
    try:
        # Nettoyage basique
        salary_str = salary_str.replace(" ", "").replace("€", "").lower()
        
        # Cas du TJM (Taux Journalier Moyen) pour les Freelance
        if "tjm" in salary_str:
            tjm_val = re.findall(r'\d+', salary_str)
            if tjm_val:
                tjm = int(tjm_val[0])
                return tjm * 210 # 210 jours ouvrés par an
        
        # Cas de plage de salaires (ex: 45k-55k ou 45000-55000)
        if "-" in salary_str:
            parts = salary_str.split("-")
            vals = []
            for p in parts:
                val = re.findall(r'\d+', p)
                if val:
                    num = int(val[0])
                    if "k" in p or num < 1000: # Si noté 45k ou 45
                        num *= 1000
                    vals.append(num)
            if len(vals) == 2:
                return int(np.mean(vals))
        
        # Cas d'un salaire simple (ex: 45k ou 45000)
        digits = re.findall(r'\d+', salary_str)
        if digits:
            num = int(digits[0])
            if "k" in salary_str or num < 1000:
                num *= 1000
            return num
            
    except Exception as e:
        logger.debug(f"Erreur lors du parsing du salaire '{salary_str}': {e}")
        
    return np.nan

def extract_skills(text, skills_raw):
    """
    Extrait les compétences cibles d'une offre d'emploi à partir
    des compétences brutes et de la description globale.
    """
    found_skills = set()
    combined_text = f"{skills_raw} {text}".lower()
    
    for skill in TARGET_SKILLS:
        if skill.lower() == "r":
            pattern = r'\b(r|langage r)\b'
        elif skill.lower() == "excel":
            pattern = r'\bexcel\b'
        elif skill.lower() == "aws":
            pattern = r'\baws\b'
        elif skill.lower() == "gcp":
            pattern = r'\bgcp\b'
        elif skill.lower() == "dbt":
            pattern = r'\bdbt\b'
        else:
            pattern = re.escape(skill.lower())
            
        if re.search(pattern, combined_text):
            found_skills.add(skill)
            
    return list(found_skills)

def main():
    logger.info("Début de l'analyse et du nettoyage des données...")
    
    if not os.path.exists(RAW_DATA_PATH):
        logger.error(f"Fichier brut '{RAW_DATA_PATH}' introuvable. Veuillez d'abord exécuter collect.py.")
        return
        
    # Charger les données brutes avec Pandas
    df = pd.read_json(RAW_DATA_PATH)
    logger.info(f"Nombre d'offres brutes chargées : {len(df)}")
    
    # 1. Supprimer les doublons éventuels
    df = df.drop_duplicates(subset=["title", "company", "location", "contract"])
    logger.info(f"Nombre d'offres après déduplication : {len(df)}")
    
    # 2. Nettoyer et standardiser les villes
    df["location"] = df["location"].fillna("Non renseigné").str.strip()
    df["location"] = df["location"].replace({
        "Paris (75)": "Paris",
        "Région Parisienne": "Paris",
        "Lyon (69)": "Lyon",
        "Nantes (44)": "Nantes",
        "Bordeaux (33)": "Bordeaux",
        "Lille (59)": "Lille"
    })
    
    # 3. Parser et standardiser les salaires
    df["salary_annual_eur"] = df.apply(lambda row: parse_salary(row["salary_raw"], row["contract"]), axis=1)
    
    # 4. Extraire la liste structurée des compétences
    df["skills_list"] = df.apply(lambda row: extract_skills(row["description"], row["skills_raw"]), axis=1)
    df["skills_count"] = df["skills_list"].apply(len)
    
    # 5. Enregistrer le fichier nettoyé en CSV pour Power BI/Excel
    df_csv = df.copy()
    df_csv["skills_csv"] = df_csv["skills_list"].apply(lambda x: ";".join(x))
    df_csv.drop(columns=["skills_list"]).to_csv(CLEANED_CSV_PATH, index=False, encoding="utf-8-sig")
    logger.info(f"Fichier CSV nettoyé enregistré sous '{CLEANED_CSV_PATH}'.")
    
    # 6. Préparer les données pour le dashboard web
    # Remplacer les valeurs NaN par None pour la compatibilité JSON
    df_clean_nan = df.replace({np.nan: None})
    
    # Exporter toute la liste nettoyée pour le filtrage côté client (avec le champ link)
    jobs_list = df_clean_nan[["title", "company", "location", "contract", "salary_annual_eur", "salary_raw", "skills_list", "date_posted", "link"]].to_dict(orient="records")
    
    stats = {
        "jobs": jobs_list,
        "lastUpdated": datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
    }
    
    # 7. Exporter sous format JavaScript
    with open(JS_DATA_PATH, "w", encoding="utf-8") as f:
        f.write(f"// Données générées le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
        f.write("const MARKET_DATA = ")
        json.dump(stats, f, ensure_ascii=False, indent=4)
        f.write(";\n")
        
    logger.info(f"Fichier JavaScript avec l'ensemble des données (avec liens) enregistré sous '{JS_DATA_PATH}'.")
    logger.info("Analyse terminée avec succès !")

if __name__ == "__main__":
    main()
