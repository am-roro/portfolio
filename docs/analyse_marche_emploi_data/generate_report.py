# /// script
# dependencies = [
#   "reportlab",
# ]
# ///

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Canvas personnalisé pour ajouter un en-tête et un pied de page
    professionnels sur toutes les pages sauf la page de garde,
    avec calcul dynamique du nombre total de pages (Pass 2).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Pas d'en-tête ni de pied de page sur la page de garde (page 1)
        if self._pageNumber == 1:
            # Dessiner quelques éléments graphiques de fond sur la page de garde
            self.saveState()
            self.setFillColor(colors.HexColor("#4f46e5")) # Couleur Indigo primaire
            self.rect(0, 800, 595.27, 41.89, stroke=0, fill=1)
            self.setFillColor(colors.HexColor("#0d9488")) # Couleur Teal secondaire
            self.rect(0, 0, 595.27, 20, stroke=0, fill=1)
            self.restoreState()
            return

        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#4b5563")) # Gris foncé
        
        # En-tête
        self.drawString(54, 800, "Rapport de Projet — Pipeline & Dashboard Analyse Emploi Data/IA")
        self.drawRightString(541, 800, "Août 2026")
        self.setStrokeColor(colors.HexColor("#e5e7eb"))
        self.setLineWidth(0.75)
        self.line(54, 790, 541, 790)
        
        # Pied de page
        self.drawString(54, 40, "Projet : Data & IA Jobs Tracker — Portfolio de Candidature")
        page_text = f"Page {self._pageNumber} sur {page_count}"
        self.drawRightString(541, 40, page_text)
        self.line(54, 52, 541, 52)
        
        self.restoreState()

def create_report(filename="Rapport_Projet_Analyse_Emploi.pdf"):
    # Initialisation du document avec marges de 54pt (approx. 1.9cm)
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    
    # Couleurs du thème
    primary_color = colors.HexColor("#312e81") # Indigo foncé / Navy
    secondary_color = colors.HexColor("#0f766e") # Teal foncé
    text_color = colors.HexColor("#1f2937") # Gris très foncé
    bg_light = colors.HexColor("#f9fafb") # Gris très clair pour les blocs
    border_color = colors.HexColor("#e5e7eb") # Gris clair pour les bordures

    # Redéfinition et ajout de styles personnalisés
    styles['Normal'].textColor = text_color
    styles['Normal'].fontSize = 10
    styles['Normal'].leading = 14

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=primary_color,
        spaceAfter=15,
        alignment=0
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=18,
        textColor=colors.HexColor("#4b5563"),
        spaceAfter=30,
        alignment=0
    )

    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#4b5563"),
        spaceAfter=5
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=primary_color,
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#065f46"),
        spaceBefore=6,
        spaceAfter=6,
        leftIndent=15
    )

    block_style = ParagraphStyle(
        'Block_Text',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1e3a8a"),
    )

    story = []

    # ================= PAGE DE GARDE =================
    story.append(Spacer(1, 100))
    story.append(Paragraph("RAPPORT DE PROJET PROFESSIONNEL", ParagraphStyle('Upper', fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=secondary_color, spaceAfter=10)))
    story.append(Paragraph("Analyse du Marché de l'Emploi<br/>Data & Intelligence Artificielle", title_style))
    story.append(Paragraph("Conception et implémentation d'un pipeline complet d'ingénierie des données en Python, d'un entrepôt de données normalisé sous Pandas, et d'un tableau de bord interactif en temps réel (Chart.js et Power BI).", subtitle_style))
    
    story.append(HRFlowable(width="100%", thickness=3, color=primary_color, spaceBefore=20, spaceAfter=40))
    
    story.append(Paragraph("<b>Auteur :</b> Amokrane", meta_style))
    story.append(Paragraph("<b>Rôle :</b> Data Engineer / Analyst", meta_style))
    story.append(Paragraph("<b>Date :</b> Août 2026", meta_style))
    story.append(Paragraph("<b>Technologies clés :</b> Python, Pandas, NumPy, BeautifulSoup, JavaScript, Chart.js, Power BI", meta_style))
    story.append(PageBreak())

    # ================= SOMMAIRE / INTRO =================
    story.append(Paragraph("1. Introduction et Objectifs du Projet", h1_style))
    story.append(Paragraph(
        "Dans le cadre du développement de mon portfolio de compétences, j'ai réalisé un projet complet d'ingénierie "
        "et d'analyse de données axé sur le marché de l'emploi dans les domaines de la <b>Data</b> et de l'<b>Intelligence Artificielle</b> "
        "en France. Ce projet a pour but de fournir une visibilité complète sur la répartition géographique des opportunités, les salaires pratiqués "
        "et les technologies les plus recherchées par les recruteurs.",
        body_style
    ))
    story.append(Paragraph(
        "Ce projet a été conçu selon des critères professionnels exigeants, reflétant des situations réelles d'entreprise :",
        body_style
    ))
    story.append(Paragraph("• <b>Robustesse technique :</b> Un pipeline capable de collecter des offres réelles et de générer un volume statistique cohérent en cas de restriction réseau.", bullet_style))
    story.append(Paragraph("• <b>Qualité de données (Data Quality) :</b> Un module d'analyse sous Pandas dédié à la déduplication, au nettoyage textuel et à la normalisation financière complexe (calculs de salaires, conversion TJM, etc.).", bullet_style))
    story.append(Paragraph("• <b>Expérience utilisateur (UI/UX) :</b> Une interface de restitution web interactive appliquant les codes esthétiques modernes (Glassmorphism, Dark mode, animations) et une maquette prête pour Power BI Desktop.", bullet_style))
    
    story.append(Spacer(1, 10))

    # ================= ARCHITECTURE TECHNIQUE =================
    story.append(Paragraph("2. Architecture Technique Générale", h1_style))
    story.append(Paragraph(
        "L'architecture repose sur un flux de données modulaire séparant distinctement la phase de collecte, "
        "la phase de transformation/analyse et la phase de restitution visuelle :",
        body_style
    ))

    # Tableau d'architecture
    arch_data = [
        [Paragraph("<b>Étape / Module</b>", styles['Normal']), Paragraph("<b>Rôle principal</b>", styles['Normal']), Paragraph("<b>Technologies utilisées</b>", styles['Normal'])],
        [Paragraph("<b>1. Collecte (collect.py)</b>", styles['Normal']), Paragraph("Scraping en direct de HelloWork et génération réaliste d'offres (fallback 1200+ lignes).", styles['Normal']), Paragraph("Python, BeautifulSoup4, Requests, JSON", styles['Normal'])],
        [Paragraph("<b>2. Traitement (analyze.py)</b>", styles['Normal']), Paragraph("Nettoyage géographique, parsing de chaînes hétérogènes de salaires, extraction des compétences clés.", styles['Normal']), Paragraph("Python, Pandas, NumPy, Expressions régulières", styles['Normal'])],
        [Paragraph("<b>3. Données de Sortie</b>", styles['Normal']), Paragraph("Export CSV structuré pour BI et export JS dynamique pour le Dashboard.", styles['Normal']), Paragraph("CSV (UTF-8-sig), JSON / JS Variable", styles['Normal'])],
        [Paragraph("<b>4. Visualisation Web</b>", styles['Normal']), Paragraph("Tableau de bord interactif avec filtres multi-critères synchronisés et graphiques animés.", styles['Normal']), Paragraph("HTML5, Vanilla CSS, Chart.js, FontAwesome", styles['Normal'])],
        [Paragraph("<b>5. Intégration BI</b>", styles['Normal']), Paragraph("Modélisation et reporting décisionnel pour présentations professionnelles.", styles['Normal']), Paragraph("Power BI Desktop (Power Query)", styles['Normal'])],
    ]

    t_arch = Table(arch_data, colWidths=[120, 230, 130])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e0e7ff")),
        ('TEXTCOLOR', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light])
    ]))
    story.append(t_arch)
    story.append(PageBreak())

    # ================= PIPELINE DE COLLECTE =================
    story.append(Paragraph("3. Pipeline de Collecte de Données (collect.py)", h1_style))
    story.append(Paragraph(
        "La collecte de données est le premier maillon de la chaîne. J'ai conçu un script Python autonome "
        "qui combine du scraping web en direct et une simulation statistique avancée :",
        body_style
    ))
    story.append(Paragraph(
        "<b>Scraping Direct de HelloWork :</b><br/>"
        "Le script interroge la plateforme HelloWork à l'aide de requêtes HTTP simulées (en-têtes HTTP modifiés "
        "pour éviter le blocage). Il parse le code HTML récupéré à l'aide de <b>BeautifulSoup4</b>. Les informations collectées sont : "
        "le titre de l'offre, le nom de l'entreprise, la localisation textuelle, le type de contrat (CDI, Freelance, etc.), "
        "le salaire brut mentionné et le lien direct de postulation.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Générateur de Fallback Réaliste :</b><br/>"
        "Pour surmonter les limitations de requêtes en direct (anti-scraping) et garantir un volume de données suffisant "
        "pour des analyses statistiques de confiance (taille d'échantillon N = 1200+), j'ai écrit un moteur de simulation robuste. "
        "Celui-ci respecte fidèlement les réalités du marché français :",
        body_style
    ))
    story.append(Paragraph("• <i>Distribution géographique cohérente</i> : Pondération favorisant Paris (55%), suivi des grandes métropoles (Lyon 12%, Nantes 7%, etc.).", bullet_style))
    story.append(Paragraph("• <i>Grille salariale réaliste</i> : Les salaires sont générés en fonction du rôle (Data Scientist, Analyst, Engineer) avec des primes géographiques (ex: +10% à Paris) et des spécificités contractuelles (les salaires des alternances/stages sont bridés aux barèmes légaux).", bullet_style))
    story.append(Paragraph("• <i>Freelancing</i> : Les Taux Journaliers Moyens (TJM) sont simulés entre 350€ et 750€ et convertis sur une base annuelle de 210 jours ouvrés pour une comparaison harmonisée.", bullet_style))
    story.append(Paragraph("• <i>Compétences associées</i> : Chaque métier pioche dans un panier de technologies logiques (ex: SQL/Power BI pour l'Analyst ; PyTorch/Scikit-Learn pour le ML Engineer).", bullet_style))

    # Encadré d'information
    story.append(Spacer(1, 5))
    info_box_data = [[
        Paragraph(
            "<b>Astuce technique :</b> Pour simplifier l'exécution sur le poste client, le script utilise les métadonnées de dépendance "
            "intégrées. Ainsi, en utilisant le gestionnaire <code>uv</code>, le script s'exécute dans un environnement virtuel temporaire "
            "sans nécessiter l'installation globale de packages tiers via la commande : <code>uv run collect.py</code>.",
            block_style
        )
    ]]
    t_info = Table(info_box_data, colWidths=[480])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eff6ff")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#bfdbfe")),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 10))

    # ================= PIPELINE DE NETTOYAGE =================
    story.append(Paragraph("4. Analyse et Préparation des Données (analyze.py)", h1_style))
    story.append(Paragraph(
        "La phase de nettoyage sous Pandas constitue la partie 'ETL' (Extract, Transform, Load) la plus critique "
        "pour la véracité de nos rapports. Le script de nettoyage réalise les transformations suivantes :",
        body_style
    ))
    story.append(Paragraph(
        "<b>Déduplication :</b> Détection et suppression automatique des doublons potentiels sur la base du regroupement "
        "du titre nettoyé, du nom de l'entreprise, de la ville et du type de contrat.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Standardisation Géographique :</b> Conversion des zones de recherche textuelles floues. Les libellés comme "
        "<i>'Paris (75)'</i> ou <i>'Région Parisienne'</i> sont uniformisés sous l'étiquette unique <i>'Paris'</i> pour "
        "éviter l'émiettement des indicateurs.",
        body_style
    ))
    
    story.append(Paragraph(
        "<b>Algorithme de parsing financier (Salaires) :</b><br/>"
        "La colonne contenant le salaire est souvent au format texte brut ('45k €', '35 000 €', 'TJM 550 €', '40k - 50k €'). "
        "J'ai implémenté une fonction de nettoyage par expressions régulières (Regex) capable de :",
        body_style
    ))
    story.append(Paragraph("• Extraire les chiffres bruts en convertissant le suffixe 'k' en milliers.", bullet_style))
    story.append(Paragraph("• Calculer la moyenne arithmétique pour les plages de salaires (ex: '45k - 55k' devient 50 000).", bullet_style))
    story.append(Paragraph("• Convertir le TJM des indépendants (Freelance) sur la base standardisée de 210 jours travaillés par an pour une comparaison équitable avec les salaires bruts des salariés.", bullet_style))
    story.append(Paragraph("• Identifier les valeurs manquantes ('Non indiqué') et les convertir en valeurs nulles (NaN) interprétables par Pandas.", bullet_style))

    story.append(Paragraph(
        "<b>Extraction sémantique des Compétences :</b><br/>"
        "Pour recenser de manière fiable les outils demandés, le script scanne le contenu textuel complet des descriptions d'offres "
        "et recherche la présence de 22 compétences clés prédéfinies (Python, Git, Airflow, SQL, Power BI, Docker, etc.) à l'aide de motifs Regex robustes "
        "qui évitent les faux positifs (par exemple, la détection de la lettre seule 'R' est limitée aux cas du mot indépendant 'R' ou 'langage R').",
        body_style
    ))
    story.append(PageBreak())

    # ================= RESTITUTION WEB =================
    story.append(Paragraph("5. Visualisation Web : Dashboard Interactif (index.html, style.css, app.js)", h1_style))
    story.append(Paragraph(
        "Pour restituer visuellement ces analyses, j'ai construit une application Web interactive monopage "
        "adoptant les standards de l'art du Web moderne :",
        body_style
    ))
    story.append(Paragraph(
        "<b>Interface Graphique Premium (UI/UX) :</b><br/>"
        "L'interface graphique est codée en HTML5 sémantique et mise en valeur par une feuille de style CSS optimisée. "
        "Le design utilise une esthétique <b>Glassmorphic</b> (panneaux sombres translucides avec un flou d'arrière-plan obtenu via "
        "<code>backdrop-filter</code>) et des dégradés de couleurs harmonieux (Indigo et Sarcelle/Teal). "
        "Les polices système ont été remplacées par les familles modernes <b>Outfit</b> et <b>Inter</b> via l'API Google Fonts. "
        "Des micro-animations fluides de survol (hover) dynamisent l'interaction.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Logique interactive (JavaScript Client) :</b><br/>"
        "Le fichier <code>app.js</code> écoute les filtres utilisateurs (Métier, Ville, Type de contrat) et recalcule "
        "instantanément en JavaScript les métriques clés (Total d'offres filtrées, Salaire brut annuel moyen hors stages, compétence reine). "
        "Il réorganise également dynamiquement le tableau d'échantillon d'offres en bas de page pour refléter la sélection.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Liaison des Données locale (Zéro Configuration CORS) :</b><br/>"
        "Pour éviter les contraintes de sécurité CORS des navigateurs modernes (qui bloquent le chargement de fichiers JSON locaux "
        "en double-cliquant simplement sur un fichier HTML), les données issues de <code>analyze.py</code> sont écrites sous forme "
        "d'une variable globale JavaScript dans le fichier <code>dashboard_data.js</code>. Cela permet au dashboard de fonctionner "
        "immédiatement sur n'importe quel ordinateur par un simple double-clic sur <code>index.html</code>, sans nécessiter de serveur local.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Moteur Graphique (Chart.js) :</b><br/>"
        "L'intégration de la librairie <b>Chart.js</b> permet d'afficher 4 vues graphiques interactives :",
        body_style
    ))
    story.append(Paragraph("1. <b>Top Compétences :</b> Barres horizontales affichant le pourcentage d'offres exigeant chaque technologie.", bullet_style))
    story.append(Paragraph("2. <b>Répartition des Contrats :</b> Graphique de type Doughnut distinguant les CDI, Freelances, Alternances, etc.", bullet_style))
    story.append(Paragraph("3. <b>Salaires par Profil :</b> Barres verticales comparant les salaires moyens annuels des 6 principaux métiers.", bullet_style))
    story.append(Paragraph("4. <b>Répartition Géographique :</b> Graphique en barres horizontales montrant le nombre absolu de postes ouverts par ville.", bullet_style))

    story.append(Spacer(1, 10))

    # ================= INTÉGRATION POWER BI =================
    story.append(Paragraph("6. Intégration Power BI et Valorisation CV", h1_style))
    story.append(Paragraph(
        "Pour aller plus loin et donner à ce projet une valeur professionnelle concrète dans le cadre de recrutements, "
        "les données nettoyées sont enregistrées sous un format CSV optimisé : <code>cleaned_jobs.csv</code>. "
        "Ce format est conçu pour être directement importable dans <b>Microsoft Power BI Desktop</b> (l'outil décisionnel leader du marché).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Recommandations de modélisation dans Power Query :</b>",
        h2_style
    ))
    story.append(Paragraph(
        "Lors de l'intégration dans Power BI, la colonne <code>skills_csv</code> contient des compétences séparées "
        "par des points-virgules (ex: 'Python;SQL;Docker'). Pour réaliser une analyse des compétences sous Power BI, "
        "l'utilisateur doit appliquer la transformation suivante dans Power Query :",
        body_style
    ))
    story.append(Paragraph(
        "1. Sélectionner la colonne <code>skills_csv</code>.<br/>"
        "2. Choisir <b>'Diviser la colonne'</b> -> <b>'Par délimiteur'</b>.<br/>"
        "3. Spécifier le point-virgule comme séparateur et sélectionner <b>'Options avancées -> Diviser en LIGNES'</b>.<br/>"
        "Cette manipulation dé-pivote la table pour permettre la création de graphiques de distribution de compétences interactifs et synchronisés.",
        body_style
    ))

    # Valorisation CV
    story.append(Paragraph(
        "<b>Exemple de valorisation sur le CV :</b>",
        h2_style
    ))
    
    cv_box_data = [[
        Paragraph(
            "<b>Développeur / Analyste de Données — Pipeline & Dashboard Emploi Data/IA</b><br/>"
            "• Conception d'un pipeline Python complet : scraping BeautifulSoup d'offres HelloWork et simulation statistique (N = 1200+).<br/>"
            "• ETL sous Pandas/NumPy : Déduplication, nettoyage géographique, standardisation financière et parsing Regex des technologies clés.<br/>"
            "• Restitution : Dashboard HTML5/CSS interactif (Chart.js) avec filtres temps réel et modélisation Power BI Desktop.<br/>"
            "<i>Technologies : Python, Pandas, BeautifulSoup, JavaScript, Chart.js, Power BI.</i>",
            ParagraphStyle('CVText', parent=styles['Normal'], fontSize=9, leading=13)
        )
    ]]
    t_cv = Table(cv_box_data, colWidths=[480])
    t_cv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f3f4f6")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#d1d5db")),
    ]))
    story.append(t_cv)
    story.append(Spacer(1, 10))

    # ================= CONCLUSION =================
    story.append(Paragraph("7. Conclusion", h1_style))
    story.append(Paragraph(
        "Ce projet démontre une maîtrise complète du cycle de vie de la donnée, depuis son extraction et son nettoyage "
        "jusqu'à sa modélisation et sa visualisation finale. Il constitue une excellente démonstration technique de portfolio "
        "pour valoriser des compétences d'ingénierie des données et de Business Intelligence auprès d'employeurs potentiels.",
        body_style
    ))
    
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceBefore=40, spaceAfter=15))
    story.append(Paragraph(
        "Rapport généré automatiquement le 02/08/2026. Code source et ressources disponibles dans le dossier du projet.",
        ParagraphStyle('FooterNotice', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.HexColor("#9ca3af"), alignment=1)
    ))

    # Construction du PDF
    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    create_report()
    print("Rapport PDF généré avec succès !")
