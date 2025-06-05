# 🧪 Tests automatisés pour `simulation-retraite-pyqt`

Bienvenue dans le dossier des tests du projet **simulation-retraite-pyqt**.

Cette suite de tests couvre à la fois :
- ✅ la **logique métier** (simulateur, stats, fichiers, logger)
- 🎨 l’**interface graphique PyQt5** (widgets animés, onglets, thèmes)

---

## 🧰 Outils utilisés

- 🐍 **[pytest](https://docs.pytest.org/)** — moteur principal de tests  
- 🪄 **[pytest-qt](https://pytest-qt.readthedocs.io/)** — pour tester les composants `PyQt5`  
- 🎯 Conforme à la norme **PEP8**  
- 📋 Le **logger global** est intégré et testé  

---

## 📂 Organisation des fichiers

| 📁 Fichier de test            | 🔎 Ce qu’il teste                                                        |
|------------------------------|---------------------------------------------------------------------------|
| `test_structure.py`          | Architecture du projet, dossiers requis, logger, importabilité des modules |
| `test_logger.py`             | Logger global, niveaux (INFO, DEBUG...), sortie fichier, logger enfant     |
| `test_fileio.py`             | Lecture/écriture CSV, erreurs, intégration logger                         |
| `test_stats.py`              | Moyenne, écart-type, intervalle de confiance                             |
| `test_simulator.py`          | Simulateur principal, indicateurs, boucle annuelle, scénarios             |
| `test_charts.py`             | Composants de graphique : Réserve, Comparaison, Confiance                  |
| `test_widgets.py`            | Widgets personnalisés : `FadeTabWidget`, `FadeWidget`, `AnimatedButton`   |
| `test_theme.py`              | Thèmes clair/sombre, préférences utilisateur                             |
| `test_ui_shortcuts.py`       | Raccourcis clavier (`QAction`, `Ctrl+Q`, etc.) dans `MenuWindow`         |

---

## 🚀 Comment exécuter tous les tests

Depuis la racine du projet, lance simplement :

```bash
pytest tests/ -v
```

📦 Pour les tests graphiques, installe `pytest-qt` si ce n’est pas déjà fait :

```bash
pip install pytest-qt
```

▶️ Pour lancer un seul fichier de test :

```bash
pytest tests/test_simulator.py
```

---

## 📊 (Optionnel) Couverture de code

Pour mesurer la couverture des tests :

```bash
pip install pytest-cov
pytest --cov=core --cov=utils --cov=ui tests/
```

Tu peux modifier les chemins `--cov=` selon l’architecture de ton projet.

---

## 💡 Philosophie de test

* 🧩 Chaque fichier de test correspond à un module fonctionnel  
* 🧪 Tous les tests sont regroupés par classe (`TestXYZ`)  
* 💨 Les composants graphiques utilisent le `qtbot` de `pytest-qt`  
* 🔐 Les fichiers sont gérés en dossiers temporaires (`tempfile`)  
* 📋 Les logs sont capturés avec `caplog`  

---

## 🛠 Suggestions d’amélioration futures

* 🔁 Ajouter des tests de simulation complète sur 40 itérations (batch)  
* 📸 Ajouter des tests de **régression visuelle** pour les graphiques `matplotlib`  
* 🚀 Intégrer un pipeline CI/CD avec **GitHub Actions** pour automatiser les tests à chaque push/PR  

---

🎓 **Projet académique réalisé par Nawfal RAZOUK**  
📘 Sujet : **Simulation Discrète — Système de Retraite Marocain**  
🗓️ Année : **2024–2025**