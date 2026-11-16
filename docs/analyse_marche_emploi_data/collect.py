# /// script
# dependencies = [
#   "requests",
#   "beautifulsoup4",
# ]
# ///

import os
import json
import random
import logging
import urllib.parse
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

# Configurer les logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

RAW_DATA_PATH = "raw_jobs.json"

def scrape_hellowork_jobs(queries=["data analyst", "data scientist", "data engineer", "machine learning"]):
    """
    Scrape des offres réelles en direct depuis HelloWork pour des profils Data/IA.
    """
    logger.info("Début du scraping d'offres réelles sur HelloWork...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    scraped_jobs = []
    
    for q in queries:
        logger.info(f"Recherche sur HelloWork pour le mot-clé : '{q}'")
        encoded_query = urllib.parse.quote_plus(q)
        url = f"https://www.hellowork.com/fr-fr/emploi/recherche.html?k={encoded_query}"
        
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'html.parser')
                headers_list = soup.find_all('header', class_='w-10/12')
                logger.info(f"Trouvé {len(headers_list)} en-têtes d'offres pour '{q}'")
                
                for header in headers_list:
                    a_tag = header.find('a')
                    if not a_tag:
                        continue
                        
                    href = a_tag.get('href', '')
                    link = f"https://www.hellowork.com{href}" if href.startswith('/') else href
                    
                    # Titre et Entreprise
                    h3 = a_tag.find('h3')
                    title = q.title() # Valeur par défaut
                    company = "Entreprise partenaire"
                    if h3:
                        title_p = h3.find('p', class_=lambda c: c and 'typo-l' in c)
                        if title_p:
                            title = title_p.text.strip()
                        else:
                            title = h3.text.strip()
                            
                        company_p = h3.find('p', class_=lambda c: c and 'typo-s' in c)
                        if company_p:
                            company = company_p.text.strip()
                    
                    # Nettoyer un peu le titre s'il contient des retours à la ligne ou du bruit
                    title = " ".join(title.split())
                    company = " ".join(company.split())
                    
                    # S'assurer que le titre correspond à une de nos catégories principales pour l'analyse
                    cleaned_title = "Data Analyst"
                    title_lower = title.lower()
                    if "scientist" in title_lower or "science" in title_lower:
                        cleaned_title = "Data Scientist"
                    elif "engineer" in title_lower or "ingénieur data" in title_lower:
                        cleaned_title = "Data Engineer"
                    elif "learning" in title_lower or "ml" in title_lower or "ia" in title_lower or "intelligence artificielle" in title_lower:
                        cleaned_title = "Machine Learning Engineer"
                    elif "analytics engineer" in title_lower:
                        cleaned_title = "Analytics Engineer"
                    elif "consultant" in title_lower:
                        cleaned_title = "Consultant Data"
                    else:
                        # Garder le titre original si c'est déjà un titre clair ou mapper vers le mot recherché
                        for main_role in ["Data Analyst", "Data Scientist", "Data Engineer", "Machine Learning Engineer", "Analytics Engineer", "Consultant Data"]:
                            if main_role.lower() in title_lower:
                                cleaned_title = main_role
                                break
                    
                    card = header.parent
                    location = "Paris"
                    contract = "CDI"
                    salary_raw = "Non indiqué"
                    
                    loc_div = card.find('div', {'data-cy': 'localisationCard'})
                    if loc_div:
                        location = loc_div.text.strip().split(" - ")[0] # Garder juste le nom de la ville
                        
                    contract_div = card.find('div', {'data-cy': 'contractCard'})
                    if contract_div:
                        contract = contract_div.text.strip()
                        
                    # Extraire le salaire
                    salary_divs = card.find_all('div', class_=lambda c: c and 'tag-secondary-s' in c)
                    for s_div in salary_divs:
                        text = s_div.text.strip()
                        if '€' in text or 'k' in text.lower():
                            salary_raw = text
                            break
                            
                    # Tenter d'extraire la description courte
                    desc_p = card.find('p', class_=lambda c: c and 'typo-s' in c and 'line-clamp' in c)
                    description = desc_p.text.strip() if desc_p else f"Offre d'emploi en direct pour le poste de {title} chez {company}."
                    
                    # On définit la date de publication (récente, aujourd'hui ou hier)
                    date_posted = (datetime.now() - timedelta(days=random.randint(0, 2))).strftime("%Y-%m-%d")
                    
                    # Compétences brutes simulées à partir du titre pour aider l'analyseur
                    scraped_jobs.append({
                        "title": cleaned_title,
                        "company": company,
                        "location": location,
                        "contract": contract,
                        "description": f"{title}. {description}",
                        "skills_raw": title, # Le titre contient souvent les technos clés
                        "salary_raw": salary_raw,
                        "date_posted": date_posted,
                        "link": link,
                        "source": "HelloWork (Live)"
                    })
            else:
                logger.warning(f"Erreur lors du scraping de HelloWork ({r.status_code})")
        except Exception as e:
            logger.error(f"Une erreur est survenue lors du scraping de HelloWork : {e}")
            
    logger.info(f"Scraping HelloWork terminé ! {len(scraped_jobs)} offres récupérées.")
    return scraped_jobs

def generate_realistic_data(n_jobs=1200):
    """
    Génère des données de fallback réalistes et fournit des liens de recherche pour celles-ci.
    """
    companies = [
        "Doctolib", "BlaBlaCar", "Criteo", "Capgemini", "Société Générale", "BNP Paribas",
        "EDF", "L'Oréal", "Decathlon", "Ubisoft", "Sanofi", "Talend", "TotalEnergies",
        "Dataiku", "Algolia", "Contentsquare", "Mirakl", "Leboncoin", "Veepee", "OVHcloud",
        "Sopra Steria", "Atos", "Accenture", "Devoteam", "Keyrus", "Safran", "Airbus"
    ]
    
    cities = ["Paris", "Lyon", "Nantes", "Bordeaux", "Lille", "Toulouse", "Marseille", "Strasbourg", "Montpellier", "Rennes"]
    city_weights = [0.55, 0.12, 0.07, 0.06, 0.05, 0.05, 0.03, 0.03, 0.02, 0.02]
    
    contracts = ["CDI", "Alternance", "CDD", "Freelance", "Stage"]
    contract_weights = [0.70, 0.15, 0.05, 0.07, 0.03]
    
    roles = {
        "Data Analyst": {
            "skills": ["SQL", "Power BI", "Excel", "Python", "Tableau", "A/B Testing", "KPIs", "Dashboarding"],
            "base_salary": (38000, 52000),
            "percentage": 0.35
        },
        "Data Scientist": {
            "skills": ["Python", "Machine Learning", "SQL", "PyTorch", "TensorFlow", "Scikit-Learn", "R", "Statistiques", "Git"],
            "base_salary": (45000, 70000),
            "percentage": 0.25
        },
        "Data Engineer": {
            "skills": ["Python", "SQL", "Spark", "Docker", "AWS", "Airflow", "Snowflake", "dbt", "Azure", "CI/CD", "Kubernetes"],
            "base_salary": (45000, 75000),
            "percentage": 0.22
        },
        "Machine Learning Engineer": {
            "skills": ["Python", "PyTorch", "Docker", "Git", "Kubernetes", "MLflow", "Cloud (AWS/GCP)", "CI/CD", "Deep Learning"],
            "base_salary": (50000, 85000),
            "percentage": 0.10
        },
        "Analytics Engineer": {
            "skills": ["SQL", "dbt", "Snowflake", "Python", "Looker", "BigQuery", "Git", "Data Modeling"],
            "base_salary": (44000, 68000),
            "percentage": 0.05
        },
        "Consultant Data": {
            "skills": ["SQL", "Power BI", "Agile", "Gestion de projet", "Excel", "Tableau", "Data Governance"],
            "base_salary": (40000, 58000),
            "percentage": 0.03
        }
    }
    
    jobs = []
    role_names = list(roles.keys())
    role_weights = [roles[r]["percentage"] for r in role_names]
    
    for i in range(n_jobs):
        role = random.choices(role_names, weights=role_weights, k=1)[0]
        company = random.choice(companies)
        city = random.choices(cities, weights=city_weights, k=1)[0]
        contract = random.choices(contracts, weights=contract_weights, k=1)[0]
        
        role_info = roles[role]
        min_s, max_s = role_info["base_salary"]
        
        if contract == "Alternance":
            salary = random.randint(14000, 24000)
        elif contract == "Stage":
            salary = random.randint(10000, 16000)
        elif contract == "Freelance":
            tjm = random.randint(350, 750)
            salary = tjm * 210
        else:
            salary = random.randint(min_s, max_s)
            if city == "Paris":
                salary = int(salary * 1.10)
        
        salary_formats = [
            f"{salary // 1000}k €",
            f"{salary // 1000} 000 €",
            f"{salary // 1000}k - {(salary // 1000) + random.randint(5, 10)}k €",
            "Non indiqué",
            f"TJM {salary // 210}€" if contract == "Freelance" else "Non indiqué"
        ]
        salary_raw = random.choices(salary_formats, weights=[0.4, 0.2, 0.2, 0.1, 0.1], k=1)[0]
        
        role_skills = role_info["skills"]
        num_skills = random.randint(3, 6)
        chosen_skills = random.sample(role_skills, min(num_skills, len(role_skills)))
        
        extra_skills = ["Communication", "Agile", "Anglais", "NoSQL", "Jira", "Linux", "Git"]
        chosen_skills += random.sample(extra_skills, random.randint(0, 2))
        random.shuffle(chosen_skills)
        skills_raw = ", ".join(chosen_skills)
        
        date_posted = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
        
        # Créer un lien de recherche HelloWork générique pour rediriger l'utilisateur s'il clique sur une offre simulée
        search_query = urllib.parse.quote_plus(f"{role} {city}")
        link = f"https://www.hellowork.com/fr-fr/emploi/recherche.html?k={search_query}"
        
        jobs.append({
            "title": role,
            "company": company,
            "location": city,
            "contract": contract,
            "description": f"En tant que {role} chez {company}, vous intégrerez notre équipe Data. "
                           f"Vous travaillerez sur des problématiques complexes en utilisant les technologies suivantes : {skills_raw}.",
            "skills_raw": skills_raw,
            "salary_raw": salary_raw,
            "date_posted": date_posted,
            "link": link,
            "source": "Générateur réaliste"
        })
        
    return jobs

def main():
    logger.info("Début de la collecte des données d'emploi Data/IA...")
    
    # 1. Tenter le scraping HelloWork en direct (récupère des vraies alternances / CDI en ligne)
    scraped_jobs = []
    try:
        scraped_jobs = scrape_hellowork_jobs()
    except Exception as e:
        logger.warning(f"Le scraping en ligne a échoué : {e}. Utilisation exclusive du générateur.")
        
    # 2. Générer les données de fallback pour compléter
    num_to_generate = max(0, 1200 - len(scraped_jobs))
    generated_jobs = generate_realistic_data(num_to_generate)
    
    # Combiner (placer les vraies offres au début du fichier)
    jobs = scraped_jobs + generated_jobs
    
    # 3. Sauvegarder les données brutes
    os.makedirs(os.path.dirname(RAW_DATA_PATH) if os.path.dirname(RAW_DATA_PATH) else ".", exist_ok=True)
    with open(RAW_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=4)
        
    logger.info(f"Collecte terminée ! {len(jobs)} offres enregistrées dans '{RAW_DATA_PATH}' "
                f"(dont {len(scraped_jobs)} réelles en direct avec liens de postulation).")

if __name__ == "__main__":
    main()
