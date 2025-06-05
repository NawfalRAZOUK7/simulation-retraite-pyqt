# 🧮 Simulation Discrète d’un Système de Retraite

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://python.org)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green?logo=qt)](https://riverbankcomputing.com/software/pyqt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey)]()

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
├── 📄 README.md              # ➤ Documentation générale du projet
├── 📦 requirements.txt       # ➤ Liste des dépendances Python
├── 🚀 main.py                # ➤ Point d'entrée principal
│
├── 🎨 assets/                # ➤ Images, logos, icônes
│
├── 🧠 core/                  # 💡 Logique métier (modèles, moteur de simulation)
│   ├── __init__.py
│   ├── employee.py       # Classe Employé
│   ├── retiree.py        # Classe Retraité
│   ├── scenario.py       # Définition scénarios
│   ├── simulator.py      # Moteur principal
│   └── germes.py         # Gestion des germes
│
├── 🗃️ data/
│   ├── config/           # ⚙️ Configurations utilisateur
│   └── output/           # 📤 Fichiers générés/exportés
│
├── 🖼️ ui/                    # 🖼️ Interface graphique PyQt5
│   ├── __init__.py
│   ├── menu_window.py
│   ├── simulation_window.py
│   ├── progress_dialog.py
│   ├── settings_window.py
│   ├── charts_window/
│   │   ├── __init__.py
│   │   ├── charts_window.py
│   │   ├── tab_comparaison.py
│   │   ├── tab_confidence.py
│   │   └── tab_reserve.py
│   ├── results_window/
│   │   ├── __init__.py
│   │   ├── results_window.py
│   │   ├── tab_by_year.py
│   │   ├── tab_csv_export.py
│   │   ├── tab_csv_import.py
│   │   └── tab_summary.py
│   └── widgets/
│       ├── __init__.py
│       ├── animated_tool_button.py
│       ├── csv_table_widget.py
│       ├── fade_tab_widget.py
│       ├── fade_widget.py
│       ├── hybrid_graph_widget.py
│       ├── plot_helpers.py
│       ├── report_export_dialog.py
│       └── sort_dialog.py
│
└── 🧰 utils/                 # 🧰 Fonctions utilitaires
    ├── __init__.py
    ├── charts.py
    ├── fileio.py
    ├── csv_sort_utils.py
    ├── logger.py
    ├── mpl_theme.py
    ├── pdf_export.py
    ├── stats.py
    └── theme_utils.py
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
