# utils/charts.py

import matplotlib.pyplot as plt
import os
from utils import logger

def plot_reserve_evolution(df_runs, simulation_id=1, couleur="#2077B4", save_path=None):
    """
    Affiche l'évolution de la réserve pour une simulation donnée (par défaut ID=1).
    """
    try:
        # Vérification défensive des colonnes attendues
        for col in ["Simulation", "Annee", "Reserve"]:
            if col not in df_runs.columns:
                logger.error(f"plot_reserve_evolution : colonne absente : '{col}'. DataFrame columns = {df_runs.columns.tolist()}")
                return
        df = df_runs[df_runs["Simulation"] == simulation_id]
        if df.empty:
            logger.warning("plot_reserve_evolution : aucune donnée pour simulation_id=%s.", simulation_id)
            return
        plt.figure(figsize=(7, 4))
        plt.plot(df["Annee"], df["Reserve"], marker='o', color=couleur, label=f"Simulation {simulation_id}")
        plt.xlabel("Année")
        plt.ylabel("Réserve (DH)")
        plt.title(f"Évolution de la réserve — Simulation {simulation_id}")
        plt.grid(True)
        plt.legend()
        if save_path:
            directory = os.path.dirname(save_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                logger.info("Création dossier export graphique : %s", directory)
            plt.savefig(save_path)
            logger.info("Graphique réserve évolution sauvegardé : %s", save_path)
        else:
            plt.show()
        plt.close()
        logger.info("plot_reserve_evolution généré pour Simulation %d.", simulation_id)
    except Exception as e:
        logger.error("Erreur plot_reserve_evolution : %s", str(e))

def plot_indicator_evolution(df_runs, indicator="TotCotis", simulation_id=1, couleur="#F15854", save_path=None):
    """
    Affiche l'évolution d'un indicateur (TotCotis, TotPens, etc.) pour une simulation donnée.
    """
    try:
        # Vérification défensive des colonnes
        for col in ["Simulation", "Annee"]:
            if col not in df_runs.columns:
                logger.error(f"plot_indicator_evolution : colonne absente : '{col}'. DataFrame columns = {df_runs.columns.tolist()}")
                return
        if indicator not in df_runs.columns:
            logger.error(f"plot_indicator_evolution : colonne absente : '{indicator}'. DataFrame columns = {df_runs.columns.tolist()}")
            return
        df = df_runs[df_runs["Simulation"] == simulation_id]
        if df.empty:
            logger.warning("plot_indicator_evolution : aucune donnée pour simulation_id=%s.", simulation_id)
            return
        plt.figure(figsize=(7, 4))
        plt.plot(df["Annee"], df[indicator], marker='s', color=couleur, label=f"{indicator} — Sim {simulation_id}")
        plt.xlabel("Année")
        plt.ylabel(indicator)
        plt.title(f"Évolution {indicator} — Simulation {simulation_id}")
        plt.grid(True)
        plt.legend()
        if save_path:
            directory = os.path.dirname(save_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                logger.info("Création dossier export graphique : %s", directory)
            plt.savefig(save_path)
            logger.info("Graphique évolution %s sauvegardé : %s", indicator, save_path)
        else:
            plt.show()
        plt.close()
        logger.info("plot_indicator_evolution généré pour %s (Sim %d).", indicator, simulation_id)
    except Exception as e:
        logger.error("Erreur plot_indicator_evolution : %s", str(e))

def plot_scenario_comparaison(df_multi, indicator="Reserve", annees=[2025, 2030, 2035], couleurs=None, save_path=None):
    """
    Compare un indicateur (Reserve ou autre) sur plusieurs scénarios, pour des années spécifiques.
    df_multi : dict {nom_scenario: DataFrame}
    couleurs : dict {nom_scenario: couleur} ou None
    """
    try:
        plt.figure(figsize=(9, 5))
        for i, (name, df) in enumerate(df_multi.items()):
            # Vérification défensive des colonnes
            for col in ["Annee", indicator]:
                if col not in df.columns:
                    logger.error(f"plot_scenario_comparaison : colonne absente : '{col}' dans scénario '{name}'. Columns = {df.columns.tolist()}")
                    continue
            y = [df[df["Annee"] == annee][indicator].mean() for annee in annees]
            color = couleurs[name] if couleurs and name in couleurs else None
            plt.plot(annees, y, marker='o', label=name, color=color)
        plt.xlabel("Année")
        plt.ylabel(indicator)
        plt.title(f"Comparaison scénarios — {indicator}")
        plt.grid(True)
        plt.legend()
        if save_path:
            directory = os.path.dirname(save_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                logger.info("Création dossier export graphique : %s", directory)
            plt.savefig(save_path)
            logger.info("Graphique comparaison scénarios %s sauvegardé : %s", indicator, save_path)
        else:
            plt.show()
        plt.close()
        logger.info("plot_scenario_comparaison généré pour %s sur %d scénarios.", indicator, len(df_multi))
    except Exception as e:
        logger.error("Erreur plot_scenario_comparaison : %s", str(e))

def plot_reserve_distribution(df_runs, annee, couleur="#70AD47", save_path=None):
    """
    Affiche la distribution (histogramme) de la réserve finale pour une année.
    """
    try:
        for col in ["Annee", "Reserve"]:
            if col not in df_runs.columns:
                logger.error(f"plot_reserve_distribution : colonne absente : '{col}'. DataFrame columns = {df_runs.columns.tolist()}")
                return
        reserves = df_runs[df_runs["Annee"] == annee]["Reserve"].values
        if len(reserves) == 0:
            logger.warning("plot_reserve_distribution : aucune donnée pour année %s.", annee)
            return
        plt.figure(figsize=(7, 4))
        plt.hist(reserves, bins=15, color=couleur, alpha=0.85, edgecolor="black")
        plt.xlabel("Réserve (DH)")
        plt.ylabel("Nombre de simulations")
        plt.title(f"Distribution de la réserve finale — Année {annee}")
        plt.grid(True, axis='y')
        if save_path:
            directory = os.path.dirname(save_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                logger.info("Création dossier export graphique : %s", directory)
            plt.savefig(save_path)
            logger.info("Histogramme réserve année %s sauvegardé : %s", annee, save_path)
        else:
            plt.show()
        plt.close()
        logger.info("plot_reserve_distribution généré pour année %s.", annee)
    except Exception as e:
        logger.error("Erreur plot_reserve_distribution : %s", str(e))

def plot_indicator_distribution(df_runs, indicator, annee, couleur="#FFB300", save_path=None):
    """
    Affiche la distribution (histogramme) d'un indicateur pour une année.
    """
    try:
        if "Annee" not in df_runs.columns:
            logger.error(f"plot_indicator_distribution : colonne absente : 'Annee'. DataFrame columns = {df_runs.columns.tolist()}")
            return
        if indicator not in df_runs.columns:
            logger.error(f"plot_indicator_distribution : colonne absente : '{indicator}'. DataFrame columns = {df_runs.columns.tolist()}")
            return
        values = df_runs[df_runs["Annee"] == annee][indicator].values
        if len(values) == 0:
            logger.warning("plot_indicator_distribution : aucune donnée pour %s, année %s.", indicator, annee)
            return
        plt.figure(figsize=(7, 4))
        plt.hist(values, bins=15, color=couleur, alpha=0.85, edgecolor="black")
        plt.xlabel(indicator)
        plt.ylabel("Nombre de simulations")
        plt.title(f"Distribution de {indicator} — Année {annee}")
        plt.grid(True, axis='y')
        if save_path:
            directory = os.path.dirname(save_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                logger.info("Création dossier export graphique : %s", directory)
            plt.savefig(save_path)
            logger.info("Histogramme %s année %s sauvegardé : %s", indicator, annee, save_path)
        else:
            plt.show()
        plt.close()
        logger.info("plot_indicator_distribution généré pour %s, année %s.", indicator, annee)
    except Exception as e:
        logger.error("Erreur plot_indicator_distribution : %s", str(e))

# --- Exemples d'utilisation ---
# plot_reserve_evolution(df_concat, simulation_id=1)
# plot_indicator_evolution(df_concat, indicator="TotPens", simulation_id=3)
# plot_scenario_comparaison({"Scénario 1": df1, "Scénario 2": df2}, indicator="Reserve", annees=[2025, 2030, 2035])
# plot_reserve_distribution(df_concat, annee=2030)
# plot_indicator_distribution(df_concat, indicator="TotCotis", annee=2025)
