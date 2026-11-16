import sys
import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

def test():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    url = 'https://www.hellowork.com/fr-fr/emploi/recherche.html?k=data+alternance'
    print(f"Requesting {url}...")
    r = requests.get(url, headers=headers, timeout=10)
    print("Status:", r.status_code)
    
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # Trouver tous les en-têtes d'offres
    headers_list = soup.find_all('header', class_='w-10/12')
    print(f"Found {len(headers_list)} job headers.")
    
    for i, header in enumerate(headers_list[:5]):
        print(f"\n--- Job {i+1} ---")
        a_tag = header.find('a')
        if not a_tag:
            print("No a_tag found")
            continue
            
        href = a_tag.get('href', '')
        link = f"https://www.hellowork.com{href}" if href.startswith('/') else href
        
        # Titre et Entreprise
        h3 = a_tag.find('h3')
        title = "Inconnu"
        company = "Inconnu"
        if h3:
            title_p = h3.find('p', class_=lambda c: c and 'typo-l' in c)
            if title_p:
                title = title_p.text.strip()
            else:
                title = h3.text.strip()
                
            company_p = h3.find('p', class_=lambda c: c and 'typo-s' in c)
            if company_p:
                company = company_p.text.strip()
        
        # Localisation et contrat
        card = header.parent
        location = "Non renseigné"
        contract = "Non renseigné"
        salary = "Non indiqué"
        
        loc_div = card.find('div', {'data-cy': 'localisationCard'})
        if loc_div:
            location = loc_div.text.strip()
            
        contract_div = card.find('div', {'data-cy': 'contractCard'})
        if contract_div:
            contract = contract_div.text.strip()
            
        # Essayer de trouver la description ou le résumé
        desc_p = card.find('p', class_=lambda c: c and 'typo-s' in c and 'line-clamp' in c)
        desc = desc_p.text.strip() if desc_p else ""
        
        # Essayer de trouver le salaire
        # Parcourir tous les div tag-secondary-s pour trouver le salaire
        salary_divs = card.find_all('div', class_=lambda c: c and 'tag-secondary-s' in c)
        for s_div in salary_divs:
            text = s_div.text.strip()
            if '€' in text or 'k' in text.lower():
                salary = text
                break
                
        print(f"Title: {title}")
        print(f"Company: {company}")
        print(f"Location: {location}")
        print(f"Contract: {contract}")
        print(f"Salary: {salary}")
        print(f"Link: {link}")
        print(f"Desc snippet: {desc[:100]}")

if __name__ == '__main__':
    test()
