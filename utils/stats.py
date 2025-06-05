# utils/stats.py

import numpy as np
import pandas as pd
import statistics
import scipy.stats as st

from utils.logger import get_child_logger
logger = get_child_logger("utils.stats")


# --- Fonctions de base (utilisées aussi dans les tests unitaires) ---

def mean(data):
    """Calcule la moyenne simple d'une liste de valeurs numériques."""
    try:
        return float(statistics.mean(data))  # ✅ cast explicite
    except statistics.StatisticsError:
        raise ValueError("Liste vide")  # ✅ conversion pour satisfaire le test


def standard_deviation(data):
    """Calcule l'écart-type d'une liste de valeurs numériques."""
    return statistics.stdev(data)


def confidence_interval(data, z=1.96):
    """
    Calcule l’intervalle de confiance à partir d’un z-score (normal).
    Retourne : (moyenne, borne_inf, borne_sup)
    """
    m = mean(data)
    s = standard_deviation(data)
    margin = z * (s / len(data) ** 0.5)
    return m, m - margin, m + margin


# --- Fonctions liées à la réserve (avec logger) ---

def moyenne_reserve(data, annee=None):
    """
    Calcule la moyenne de la réserve (optionnellement pour une année).
    """
    try:
        if isinstance(data, pd.DataFrame):
            df = data
            if annee is not None:
                if "Annee" not in df.columns:
                    logger.warning("moyenne_reserve : colonne 'Annee' manquante.")
                    return None
                df = df[df["Annee"] == annee]
            if "Reserve" not in df.columns:
                logger.warning("moyenne_reserve : colonne 'Reserve' manquante.")
                return None
            reserves = df["Reserve"].values

        elif isinstance(data, pd.Series):
            reserves = data.values
        elif isinstance(data, (list, np.ndarray)):
            reserves = np.asarray(data)
        else:
            logger.warning("moyenne_reserve : type de données non supporté (%s).", type(data))
            return None

        if len(reserves) == 0:
            logger.warning("moyenne_reserve : aucune donnée pour l'année %s.", annee)
            return None

        result = float(np.mean(reserves))
        logger.info("Moyenne réserve calculée pour année %s : %.2f (n=%d)", str(annee), result, len(reserves))
        return result

    except Exception as e:
        logger.error("Erreur calcul moyenne réserve : %s", str(e))
        return None


def intervalle_confiance(data, alpha=0.05):
    """
    Calcule l’intervalle de confiance à 1-alpha sur des données numériques.
    """
    try:
        if isinstance(data, pd.DataFrame):
            if "Reserve" not in data.columns:
                logger.warning("intervalle_confiance : colonne 'Reserve' manquante dans DataFrame.")
                return (None, None)
            arr = data["Reserve"].values
        elif isinstance(data, pd.Series):
            arr = data.values
        elif isinstance(data, (list, np.ndarray)):
            arr = np.asarray(data)
        else:
            logger.warning("intervalle_confiance : type de données non supporté (%s).", type(data))
            return (None, None)

        n = len(arr)
        if n == 0:
            return (None, None)
        if n == 1:
            return (arr[0], arr[0])

        m = np.mean(arr)
        se = st.sem(arr)
        h = se * st.t.ppf(1 - alpha / 2, n - 1)
        return (m - h, m + h)

    except Exception as e:
        logger.error("Erreur intervalle_confiance : %s", str(e))
        return (None, None)


def intervalle_confiance_reserve(df_runs, annee, alpha=0.05):
    """
    IC pour la réserve d’une année spécifique.
    """
    try:
        if df_runs is None or "Reserve" not in df_runs.columns or "Annee" not in df_runs.columns:
            logger.warning("intervalle_confiance_reserve : DataFrame incomplet ou None.")
            return (None, None)

        reserves = df_runs[df_runs["Annee"] == annee]["Reserve"].values
        n = len(reserves)
        if n == 0:
            logger.warning("intervalle_confiance_reserve : aucune donnée pour année %s.", annee)
            return (None, None)
        if n == 1:
            return (reserves[0], reserves[0])

        m = np.mean(reserves)
        se = st.sem(reserves)
        h = se * st.t.ppf(1 - alpha / 2, n - 1)
        logger.info("IC %.1f%% pour année %s (n=%d) : [%.2f, %.2f]", 100 * (1 - alpha), annee, n, m - h, m + h)
        return (m - h, m + h)

    except Exception as e:
        logger.error("Erreur calcul IC réserve pour année %s : %s", annee, str(e))
        return (None, None)


def intervalle_confiance_multi(df_runs, annees, alpha=0.05):
    """
    Calcule l'IC de réserve pour chaque année dans une liste.
    """
    results = {}
    try:
        for annee in annees:
            ic = intervalle_confiance_reserve(df_runs, annee, alpha=alpha)
            results[annee] = ic
        logger.info("IC multi-années calculé pour %d années.", len(annees))
        return results
    except Exception as e:
        logger.error("Erreur calcul IC multi-années : %s", str(e))
        return {}

# --- Exports explicites ---
__all__ = [
    "mean",
    "standard_deviation",
    "confidence_interval",
    "moyenne_reserve",
    "intervalle_confiance",
    "intervalle_confiance_reserve",
    "intervalle_confiance_multi"
]

# --- Exemples d'utilisation ---
# df_concat = pd.concat(runs, ignore_index=True)
# print(moyenne_reserve(df_concat, annee=2025))
# print(intervalle_confiance_reserve(df_concat, annee=2030))
# print(intervalle_confiance_multi(df_concat, [2025, 2030, 2035]))
# data = [12, 15, 14, 10, 13]
# print(intervalle_confiance(data))
