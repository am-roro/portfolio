# 📊 Analyse du Marché de l'Emploi en Data/IA (France)

Ce projet permet de collecter, nettoyer, analyser et visualiser les offres d'emploi dans les domaines de la Data et de l'Intelligence Artificielle en France. Il met en lumière les compétences clés les plus recherchées, la répartition géographique, les salaires moyens et les types de contrats.

Il est structuré en deux grandes parties :
1. **Pipeline de données (Python/Pandas)** : Collecte brute (scraping & génération) et analyse statistique.
2. **Visualisation (Web & Power BI)** : Un tableau de bord web interactif immédiat et un fichier CSV prêt pour Power BI.

---

## 📂 Structure du Projet

- 📄 `collect.py` : Script Python de collecte (scraping BeautifulSoup avec fallback de génération réaliste de 1200+ offres).
- 📄 `analyze.py` : Script de nettoyage et d'analyse utilisant **Pandas** et **NumPy** (génère les fichiers de sortie).
- 📄 `cleaned_jobs.csv` : Jeu de données nettoyé et structuré (idéal pour **Power BI** ou Excel).
- 📄 `dashboard_data.js` : Les données analysées injectées dans une variable JavaScript (évite les blocages CORS du navigateur).
- 📄 `index.html` : Structure HTML5 du tableau de bord web interactif.
- 📄 `style.css` : Styles graphiques premium du dashboard (Dark mode, Glassmorphism, animations).
- 📄 `app.js` : Logique JavaScript du dashboard (liaison des filtres dynamiques et graphiques Chart.js).
- 📄 `README.md` : Ce guide d'utilisation.

---

## 🛠️ Instructions de Fonctionnement

### 1. Prérequis
Grâce à `uv` (le gestionnaire de packages ultra-rapide utilisé par l'IDE), **vous n'avez pas besoin d'installer Python globalement sur votre ordinateur**. Tout s'exécute dans un environnement isolé à la volée.

### 2. Exécuter le pipeline de données
Ouvrez votre terminal dans le dossier du projet et exécutez les deux commandes suivantes :

```powershell
# Étape 1 : Collecter les offres d'emploi (brut)
uv run collect.py

# Étape 2 : Nettoyer les données et exécuter l'analyse statistique
uv run analyze.py
```
*Note : Si les bibliothèques Pandas, BeautifulSoup4 ou requests ne sont pas présentes, `uv` les téléchargera et les installera automatiquement en arrière-plan.*

### 3. Consulter le Tableau de Bord interactif
Pour ouvrir le tableau de bord web :
- **Double-cliquez simplement sur le fichier `index.html`** dans votre explorateur de fichiers pour l'ouvrir dans votre navigateur habituel.
- *Aucun serveur web ou configuration CORS n'est requis* car les données sont directement chargées localement via `dashboard_data.js`.
- Vous pouvez filtrer dynamiquement les offres par **Métier**, **Ville** et **Type de contrat** ; tous les KPIs et graphiques se recalculent instantanément en temps réel !

---

## 📈 Guide d'Intégration Power BI (Le plus pour le CV)

Pour valoriser ce projet lors d'entretiens d'embauche, il est fortement recommandé de recréer un tableau de bord sur **Power BI Desktop** (version gratuite de Microsoft).

### Étapes d'intégration :
1. **Téléchargement** : Installez **Power BI Desktop** depuis le Microsoft Store (gratuit).
2. **Importer les données** :
   - Cliquez sur **"Obtenir les données"** (Get Data) -> **"Texte/CSV"**.
   - Sélectionnez le fichier `cleaned_jobs.csv` généré par le script Python.
   - Power BI détectera automatiquement les colonnes et le formatage UTF-8. Cliquez sur **"Charger"**.
3. **Créer les Visualisations** :
   - **Filtres (Slicers)** : Ajoutez un filtre visuel pour la colonne `location` (Ville) et un autre pour `title` (Métier).
   - **Graphique de Compétences** : Utilisez la colonne `skills_csv`. Dans Power BI, vous pouvez créer un graphique en barres horizontales. *Astuce : Pour séparer les compétences listées par `;`, vous pouvez utiliser Power Query ("Transformer les données") -> Diviser la colonne par délimiteur `;`.*
   - **Cartes KPI** : Créez une carte affichant le nombre de lignes (Total Offres) et une autre affichant la moyenne de `salary_annual_eur` (filtrez le visuel pour exclure les alternances et les stages).
4. **Mise en page** : Adoptez un thème sombre ou épuré pour correspondre aux meilleures pratiques de design de données.

---

## 📝 Exemple de valorisation sur le CV

Voici comment vous pouvez présenter ce projet dans la section **"Projets"** ou **"Expériences"** de votre CV :

> **Analyseur du Marché de l'Emploi Data/IA — Pipeline Python & Dashboard Interactif**
> - Développement d'un script de scraping (BeautifulSoup) et de traitement de données (Pandas/NumPy) sur plus de 1200 offres d'emploi en France.
> - Normalisation des salaires bruts et TJM, et extraction de mots-clés textuels pour identifier les technologies clés.
> - Conception d'un tableau de bord dynamique en HTML5/Chart.js avec filtrage en temps réel, et intégration sous Power BI Desktop pour l'aide à la décision géographique.
> *Mots-clés : Python, Pandas, BeautifulSoup, Power BI, Chart.js, Nettoyage de données.*
