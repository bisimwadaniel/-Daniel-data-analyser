# 📊 Daniel Data Analyser

Une application Streamlit interactive pour analyser, filtrer et visualiser vos données facilement.

## ✨ Fonctionnalités

### 1. 📁 Chargement de Données
- Importez des fichiers **CSV** ou **Excel**
- Chargement avec cache pour optimiser les performances
- Affichage automatique des types de colonnes

### 2. 🔍 Aperçu des Données
- Indicateurs clés (KPI) : nombre de lignes, colonnes, valeurs manquantes, usage mémoire
- Affichage des 10 premières lignes

### 3. 🔎 Filtrage des Données
- Filtrez les données par colonne et valeur
- Téléchargez les données filtrées en CSV

### 4. 📈 Statistiques Avancées
- **Variables Numériques** : statistiques descriptives (mean, std, min, max, quartiles, etc.)
- **Variables Catégorielles** : analyse des catégories
- **Groupement** : agrégation par groupes (mean, sum, count, min, max)
- Téléchargement des statistiques en CSV

### 5. 📊 Visualisations Interactives
Créez facilement des graphiques Plotly :
- **Nuage de points (Scatter)**
- **Lignes (Line)**
- **Barres (Bar)**
- **Boîte à moustaches (Boxplot)**
- **Histogramme**

Chaque graphique peut être coloré par une variable catégorique pour plus d'insights.

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Étapes

1. **Clonez le repository**
```bash
git clone https://github.com/bisimwadaniel/-Daniel-data-analyser.git
cd Daniel-data-analyser
```

2. **Créez un environnement virtuel** (recommandé)
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installez les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancez l'application**
```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

## 📖 Utilisation

1. Cliquez sur **"Choisissez un fichier"** dans la barre latérale
2. Sélectionnez un fichier CSV ou Excel
3. Explorez les différentes sections :
   - **Aperçu** : Visualisez les données brutes
   - **Filtrer** : Recherchez des valeurs spécifiques
   - **Statistiques** : Analysez les distributions
   - **Visualisation** : Créez des graphiques interactifs

## 📝 Structure du Projet

```
Daniel-data-analyser/
├── app.py              # Application principale
├── requirements.txt    # Dépendances Python
└── README.md          # Ce fichier
```

## 🛠️ Technologies Utilisées

- **Streamlit** : Framework pour créer des apps web interactives
- **Pandas** : Manipulation et analyse de données
- **Plotly** : Visualisations graphiques interactives
- **OpenPyXL** : Support des fichiers Excel

## 💡 Exemple de Données

L'application fonctionne avec des données structurées en tableau :

| Date | Ventes (€) | Catégorie |
|------|-----------|----------|
| 2026-01-01 | 1200 | Électronique |
| 2026-01-02 | 1500 | Mode |
| 2026-01-03 | 1100 | Électronique |

## 🎯 Améliorations Apportées

✅ Fonction générique `create_chart()` pour éviter la duplication  
✅ Gestion robuste des erreurs  
✅ Filtrage dynamique des données  
✅ Téléchargement de données et statistiques  
✅ Statistiques descriptives avancées  
✅ Groupement et agrégation des données  
✅ Interface utilisateur optimisée  
✅ Documentation complète du code  
✅ Support des types de données automatique  

## 📌 Notes

- Les fichiers volumineux (>100MB) peuvent être lents à charger
- La mise en cache Streamlit optimise les rechargements
- Les graphiques Plotly sont entièrement interactifs (zoom, hover, etc.)

## 📧 Support

Pour des questions ou des suggestions, n'hésitez pas à ouvrir une **issue** sur GitHub.

## 📄 Licence

Ce projet est libre d'utilisation et de modification.

---

**Créé par Daniel** 🎉
