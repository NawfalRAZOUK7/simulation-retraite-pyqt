# 🧮 Simulation Discrète d’un Système de Retraite

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://python.org)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green?logo=qt)](https://riverbankcomputing.com/software/pyqt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey)]()

![Tests](https://github.com/NawfalRAZOUK7/simulation-retraite-pyqt/actions/workflows/tests.yml/badge.svg)
![Coverage](coverage.svg)


**Projet Python PyQt5 – Architecture Modulaire, Expérience Utilisateur Moderne & Professionnelle**

---

## 📋 Présentation

Cette application simule l’évolution d’un système de retraite par répartition, selon différents scénarios démographiques et financiers.  
Elle propose une **interface graphique moderne** (PyQt5) avec mode sombre/clair, animations fluides, exports avancés, raccourcis clavier universels, et une architecture logicielle modulaire et orientée objet.

> **Objectif pédagogique** : Illustrer l’impact des paramètres sur la viabilité d’un système de retraite, tout en démontrant la maîtrise des bonnes pratiques logicielles ET d’une UX contemporaine (toolbar animée, PDF, dark mode…).

---

## ✨ Nouveautés UX / Pro

- 🌙 **Mode sombre/clair** dynamique (bouton dans la toolbar)
- 🖱️ **Toolbar animée** avec boutons stylés et effets d’agrandissement au survol
- ⌨️ **Raccourcis clavier universels** :  
  - `Ctrl+S` – Sauvegarde rapide du graphique
  - `Ctrl+O` – Import CSV instantané
  - `Ctrl+→ / Ctrl+←` – Navigation rapide entre onglets
  - `Ctrl+C / Ctrl+V` – Copier/coller Excel dans les tableaux
- 📑 **Export PDF** complet (graphiques, statistiques, résumé)
- 📋 **Copier/coller Excel-like** dans toutes les tables (sélection rapide)
- ✨ **Animations fluides** : transitions, fade-in onglets, boutons modernes
- 🔒 **Logger centralisé** et paramétrable par menu (niveau DEBUG/INFO…)

---

## 🚀 Fonctionnalités principales

- **Interface graphique (PyQt5)** ergonomique et intuitive
- **Génération réaliste** de populations (employés/retraités)
- **Choix de scénarios** variés et germes pseudo-aléatoires
- **Simulation multi-runs** (statistiques sur plusieurs décennies)
- **Analyse statistique** (moyenne, intervalles de confiance…)
- **Graphiques interactifs** (réserve, comparaisons, IC…)
- **Export CSV** & **Export PDF** des résultats
- **Configuration avancée** : germes, dossiers, logs…
- **Copier/Coller** compatible Excel dans les tableaux
- **Système de logs** configurable

---

## 🗂️ Architecture du projet

<pre>
📁 simulation-retraite-pyqt/
│
├── 📄 README.md              # ➤ Ce fichier contient la documentation principale du projet : objectif, installation, usage, etc.
├── 📦 requirements.txt       # ➤ Liste des bibliothèques Python nécessaires pour exécuter le projet
├── 🚀 main.py                # ➤ Fichier principal à lancer pour démarrer l’application
│
├── ✅ coverage.svg           # ➤ Badge local affichant le pourcentage de couverture des tests
├── 📊 htmlcov/               # ➤ Dossier généré automatiquement par pytest-cov pour afficher un rapport HTML complet
│
├── 🎨 assets/                # ➤ Contient les ressources visuelles (ex. : icônes lune et soleil)
│   ├── moon.png
│   └── sun.png
│
├── 🧠 core/                  # 💡 Composants métier fondamentaux (modèles, logique de simulation)
│   ├── __init__.py           # ➤ Marqueur de package Python
│   ├── employee.py           # ➤ Définition de la classe Employé
│   ├── retiree.py            # ➤ Définition de la classe Retraité
│   ├── scenario.py           # ➤ Définition des scénarios de retraite
│   ├── simulator.py          # ➤ Moteur principal qui exécute la simulation
│   ├── germes.py             # ➤ Gestion des éléments aléatoires (germes)
│   └── logger.py             # ➤ Logger spécifique pour suivre les actions dans core/
│
├── 🗃️ data/                  # 📂 Dossier de données et résultats
│   ├── config/               # ⚙️ Configuration initiale de l’utilisateur (placeholder)
│   │   └── README.md
│   └── output/               # 📤 Résultats générés après exécution
│       ├── README.md
│       └── resultats.csv     # ➤ Fichier CSV d’export
│
├── 🖼️ ui/                    # 🖼️ Interface utilisateur graphique PyQt5
│   ├── __init__.py
│   ├── menu_window.py        # ➤ Menu principal
│   ├── simulation_window.py  # ➤ Fenêtre principale de simulation
│   ├── progress_dialog.py    # ➤ Fenêtre de progression lors des calculs
│   ├── settings_window.py    # ➤ Fenêtre des paramètres utilisateurs
│   ├── dialogs.py            # ➤ Boîtes de dialogue diverses
│   ├── theme.py              # ➤ Gestion du thème clair/sombre
│
│   ├── charts_window/        # 📊 Graphiques interactifs
│   │   ├── __init__.py
│   │   ├── charts_window.py          # ➤ Fenêtre des graphiques
│   │   ├── tab_comparaison.py       # ➤ Onglet comparaison entre scénarios
│   │   ├── tab_confidence.py        # ➤ Onglet pour intervalles de confiance
│   │   ├── tab_reserve.py           # ➤ Onglet pour les réserves de retraite
│   │   ├── scenario_selector.py     # ➤ Sélection dynamique des scénarios
│   │   └── logger.py                # ➤ Logger local pour cette fenêtre
│
│   ├── results_window/       # 📈 Résultats tabulaires
│   │   ├── __init__.py
│   │   ├── results_window.py       # ➤ Fenêtre d’affichage global
│   │   ├── tab_by_year.py         # ➤ Vue par année
│   │   ├── tab_csv_export.py      # ➤ Export CSV
│   │   ├── tab_csv_import.py      # ➤ Import CSV
│   │   ├── tab_summary.py         # ➤ Résumé global
│   │   └── logger.py              # ➤ Logger spécifique
│
│   └── widgets/              # 🧩 Composants PyQt personnalisés
│       ├── __init__.py
│       ├── animated_tool_button.py    # ➤ Bouton avec animation
│       ├── csv_table_widget.py        # ➤ Table CSV avec gestion d'import/export
│       ├── fade_tab_widget.py         # ➤ Onglets avec transition en fondu
│       ├── fade_widget.py             # ➤ Widget avec effet de disparition
│       ├── hybrid_graph_widget.py     # ➤ Graphique interactif combiné
│       ├── plot_helpers.py            # ➤ Fonctions d’aide pour les graphiques
│       ├── report_export_dialog.py    # ➤ Dialogue pour exporter les rapports
│       └── sort_dialog.py             # ➤ Dialogue pour tri personnalisé
│
├── 🧪 tests/                 # ✅ Tests unitaires automatisés avec Pytest
│   ├── conftest.py               # ➤ Configuration des fixtures communes
│   ├── test_charts.py            # ➤ Tests des graphiques
│   ├── test_fileio.py            # ➤ Tests des fonctions de fichier
│   ├── test_logger.py            # ➤ Tests des loggers
│   ├── test_simulator.py         # ➤ Tests du moteur de simulation
│   ├── test_stats.py             # ➤ Tests statistiques
│   ├── test_structure.py         # ➤ Tests de structure (données, format, validité)
│   ├── test_theme.py             # ➤ Tests des thèmes UI
│   ├── test_ui_shortcuts.py      # ➤ Tests des raccourcis clavier
│   ├── test_widgets.py           # ➤ Tests des widgets personnalisés
│   └── README.md                 # ➤ Guide pour lancer les tests localement
│
└── 🧰 utils/                 # 🧰 Fonctions utilitaires transversales
    ├── __init__.py
    ├── charts.py               # ➤ Génération de graphiques
    ├── fileio.py               # ➤ Lecture/écriture de fichiers
    ├── csv_sort_utils.py       # ➤ Aide au tri CSV
    ├── logger.py               # ➤ Logger générique
    ├── mpl_theme.py            # ➤ Thèmes personnalisés matplotlib
    ├── pdf_export.py           # ➤ Export PDF
    ├── stats.py                # ➤ Fonctions statistiques
    └── theme_utils.py          # ➤ Fonctions liées aux thèmes graphiques
</pre>

---

## ⚙️ Installation & lancement

1. **Cloner le dépôt**
    ```bash
    git clone <url-du-repo>
    cd simulation-retraite-pyqt
    ```

2. **Créer l’environnement virtuel & installer les dépendances**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows : .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Lancer l’application**
    ```bash
    python main.py
    ```

---

## 🖥️ Utilisation

- **Simulation** : Choisis un scénario, configure les germes, puis lance la simulation.
- **Résultats** : Visualise les indicateurs globaux/annuels, exporte en CSV.
- **Graphiques** : Compare réserves, scénarios, intervalles de confiance.
- **Comparaison multi-scénarios** : Lance la génération, ouvre la vue graphique dédiée.
- **Paramètres** : Modifie les valeurs par défaut (germes, dossier export, logs).
- **Mode sombre/clair** : Change instantanément via la toolbar en haut.
- **Raccourcis clavier** :  
  - `Ctrl+S` : Sauvegarder graphique · `Ctrl+O` : Importer CSV ·
  - `Ctrl+→/←` : Naviguer entre onglets · `Ctrl+C/V` : Copier/Coller tableaux.

---

## 📂 Organisation des données

- `data/config/` : fichiers de configuration utilisateur (ex : `parametres.json`)
- `data/output/` : tous les fichiers exportés (CSV, résultats, logs…)
- Ces dossiers sont toujours présents grâce à un fichier `README.md`.

---

## 🛠️ Bonnes pratiques et options avancées

- **Architecture OOP et modulaire** (UI, logique métier, utilitaires)
- **Logger centralisé & configurable** (par le menu Paramètres)
- **Génération automatique des dossiers de données**
- **Code robuste, commenté, prêt à l’extension**

---

## 📦 Dépendances principales

- Python >= 3.8
- PyQt5 >= 5.15
- pandas >= 1.2
- numpy >= 1.19
- matplotlib >= 3.4

---

## 👤 Auteur

- Nawfal RAZOUK
- Projet académique – Simulation Discrète / Système de Retraite

---

## 🖼️ Demo / Captures

<!-- TODO: Ajouter des captures d’écran ou GIF animés ici pour illustrer l’interface moderne et les animations -->

---

## 📄 Licence

Ce projet est destiné à un usage pédagogique et académique (MIT).
