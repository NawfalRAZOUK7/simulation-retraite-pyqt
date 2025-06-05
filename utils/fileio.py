# utils/fileio.py

import pandas as pd
import json
import os
import datetime

# Logger métier : place ici ton import du logger commun
try:
    from utils.logger import logger  # Si tu as un logger dans utils/logger.py
except ImportError:
    import logging
    logger = logging.getLogger("fileio")
    logging.basicConfig(level=logging.INFO)

def export_dataframe_to_csv(df_or_dict, path, mode='single', sep=',', encoding='utf-8'):
    """
    Exporte un DataFrame pandas OU un dict de DataFrames en CSV.

    - df_or_dict: pd.DataFrame OU dict[str, pd.DataFrame]
    - path: chemin de base (ex: 'export.csv' ou 'multi_export')
    - mode:
        - 'single' (défaut) -> DataFrame unique ou concatène tous les DataFrames (dict) dans un seul CSV.
        - 'split' -> dict[str, DataFrame]: exporte chaque scénario dans un fichier séparé "<path>_<nom>.csv"
    - sep: séparateur CSV (défaut: virgule)
    - encoding: encodage (utf-8 par défaut)

    Retourne True si tout OK, False sinon.
    """
    try:
        ensure_directory_exists(path)

        # Cas 1: DataFrame simple
        if isinstance(df_or_dict, pd.DataFrame):
            df_or_dict.to_csv(path, index=False, sep=sep, encoding=encoding)
            if df_or_dict.empty:
                logger.warning("Export d'un DataFrame vide (colonnes exportées uniquement) dans %s", path)
            else:
                logger.info("Fichier CSV exporté avec succès : %s", path)
            return True

        # Cas 2: Dictionnaire de DataFrames
        elif isinstance(df_or_dict, dict):
            if mode == 'single':
                # Concatène tous les DataFrames, ajoute une colonne 'Scenario' pour l'identifiant
                concat_list = []
                for k, df in df_or_dict.items():
                    if isinstance(df, pd.DataFrame) and not df.empty:
                        df_copy = df.copy()
                        df_copy.insert(0, "Scenario", k)
                        concat_list.append(df_copy)
                if concat_list:
                    df_concat = pd.concat(concat_list, ignore_index=True)
                else:
                    # Si tous vides, crée DataFrame vide avec juste les colonnes
                    df_concat = pd.DataFrame()
                df_concat.to_csv(path, index=False, sep=sep, encoding=encoding)
                logger.info("Fichier CSV multi-scenarios exporté (concaténé) : %s", path)
                return True

            elif mode == 'split':
                # Export chaque DataFrame séparément
                exported = False
                for k, df in df_or_dict.items():
                    if not isinstance(df, pd.DataFrame):
                        continue
                    filename = f"{os.path.splitext(path)[0]}_{k}.csv"
                    df.to_csv(filename, index=False, sep=sep, encoding=encoding)
                    if df.empty:
                        logger.warning("Export d'un DataFrame vide (colonnes exportées uniquement) dans %s", filename)
                    else:
                        logger.info("Scénario '%s' exporté : %s", k, filename)
                    exported = True
                return exported

            else:
                logger.error("Mode export non reconnu : '%s' (utilise 'single' ou 'split')", mode)
                return False

        else:
            logger.error("Type d'entrée non pris en charge pour export_dataframe_to_csv : %s", type(df_or_dict))
            return False

    except Exception as e:
        logger.error("Export CSV échoué pour %s : %s", path, str(e))
        return False

def ensure_directory_exists(path):
    """
    Vérifie et crée le dossier parent du fichier (CSV, PDF, etc.) si besoin.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        logger.info("Dossier créé pour export : %s", directory)

def get_default_pdf_path(section_name=None, base_dir="data/output", prefix="rapport", ext="pdf"):
    """
    Génère un chemin de fichier PDF unique basé sur la date et l'heure courante.
    Utilise optionnellement un nom de section ou autre identifiant.
    Exemple: "data/output/rapport_2024-06-05_14-55_section.pdf"
    """
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d_%H-%M")
    if section_name:
        section_part = f"_{section_name.replace(' ', '_')}"
    else:
        section_part = ""
    filename = f"{prefix}_{date_str}{section_part}.{ext}"
    return os.path.join(base_dir, filename)

def export_pdf_file(pdf_bytes, path):
    """
    Sauvegarde un PDF à partir d'un buffer bytes (optionnel, pour usage avancé).
    """
    try:
        ensure_directory_exists(path)
        with open(path, "wb") as f:
            f.write(pdf_bytes)
        logger.info("Fichier PDF exporté : %s", path)
        return True
    except Exception as e:
        logger.error("Erreur export PDF dans %s : %s", path, str(e))
        return False

def load_config(path):
    """
    Charge un fichier de configuration JSON et retourne un dictionnaire.
    Logger : succès, fichier manquant, ou erreur de lecture.
    """
    if not os.path.exists(path):
        logger.warning("Aucun fichier de config trouvé à : %s", path)
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
        logger.info("Config chargée depuis : %s", path)
        return config
    except Exception as e:
        logger.error("Lecture config échouée : %s — %s", path, str(e))
        return {}

def save_config(config, path):
    """
    Sauvegarde un dictionnaire de configuration en JSON.
    Logger : succès ou erreur d'écriture.
    """
    try:
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            logger.info("Dossier créé pour sauvegarde config : %s", directory)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        logger.info("Config sauvegardée dans : %s", path)
        return True
    except Exception as e:
        logger.error("Sauvegarde config échouée pour %s : %s", path, str(e))
        return False

# --- Exemples d'utilisation ---
# export_dataframe_to_csv(df, "data/output/simulations.csv")          # Simple
# export_dataframe_to_csv(dict_scenarios, "data/output/scen_multi.csv", mode='single')   # Multi-concaténé
# export_dataframe_to_csv(dict_scenarios, "data/output/scen_multi", mode='split')        # Multi-fichiers
# pdf_path = get_default_pdf_path(section_name="comparaison")
# export_pdf_file(pdf_bytes, pdf_path)
# cfg = load_config("data/config/parametres.json")
# save_config({"IX": 123, "IY": 456, "IZ": 789}, "data/config/parametres.json")
