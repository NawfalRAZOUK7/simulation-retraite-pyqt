# utils/fileio.py

import pandas as pd
import json
import os
import datetime
import csv

from utils.logger import get_child_logger
logger = get_child_logger("utils.fileio")


# --- CSV <-> list[rows] (basique, style unittest) ---

def write_csv(file_path, data):
    """
    Écrit un tableau de lignes (list of lists) dans un fichier CSV.
    """
    try:
        ensure_directory_exists(file_path)
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(data)
        logger.info("Écriture dans le fichier : %s (n lignes = %d)", file_path, len(data))
        return True
    except Exception as e:
        logger.error("Erreur écriture CSV simple : %s — %s", file_path, str(e))
        raise  # Re-lever l'exception pour les tests


def read_csv(file_path):
    """
    Lit un fichier CSV et retourne une liste de lignes (list of lists).
    """
    try:
        with open(file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            data = list(reader)
        logger.info("CSV lu depuis %s (n lignes = %d)", file_path, len(data))
        return data
    except FileNotFoundError as e:
        logger.error("Erreur lecture CSV simple : %s — %s", file_path, str(e))
        raise  # Re-lever pour test_read_nonexistent_file_raises
    except Exception as e:
        logger.error("Erreur lecture CSV inconnue : %s — %s", file_path, str(e))
        raise


# --- Export CSV pandas (avancé, DataFrame(s)) ---

def export_dataframe_to_csv(df_or_dict, path, mode='single', sep=',', encoding='utf-8'):
    """
    Exporte un DataFrame pandas OU un dict de DataFrames en CSV.
    """
    try:
        ensure_directory_exists(path)

        if isinstance(df_or_dict, pd.DataFrame):
            df_or_dict.to_csv(path, index=False, sep=sep, encoding=encoding)
            if df_or_dict.empty:
                logger.warning("Export d'un DataFrame vide (colonnes exportées uniquement) dans %s", path)
            else:
                logger.info("Fichier CSV exporté avec succès : %s", path)
            return True

        elif isinstance(df_or_dict, dict):
            if mode == 'single':
                concat_list = []
                for k, df in df_or_dict.items():
                    if isinstance(df, pd.DataFrame) and not df.empty:
                        df_copy = df.copy()
                        df_copy.insert(0, "Scenario", k)
                        concat_list.append(df_copy)
                df_concat = pd.concat(concat_list, ignore_index=True) if concat_list else pd.DataFrame()
                df_concat.to_csv(path, index=False, sep=sep, encoding=encoding)
                logger.info("Fichier CSV multi-scenarios exporté (concaténé) : %s", path)
                return True

            elif mode == 'split':
                exported = False
                for k, df in df_or_dict.items():
                    if not isinstance(df, pd.DataFrame):
                        continue
                    filename = f"{os.path.splitext(path)[0]}_{k}.csv"
                    df.to_csv(filename, index=False, sep=sep, encoding=encoding)
                    if df.empty:
                        logger.warning("Export d'un DataFrame vide dans %s", filename)
                    else:
                        logger.info("Scénario '%s' exporté : %s", k, filename)
                    exported = True
                return exported

            else:
                logger.error("Mode export non reconnu : '%s' (utilise 'single' ou 'split')", mode)
                return False

        else:
            logger.error("Type d'entrée non pris en charge : %s", type(df_or_dict))
            return False

    except Exception as e:
        logger.error("Export CSV échoué pour %s : %s", path, str(e))
        return False


# --- Outils génériques fichiers ---

def ensure_directory_exists(path):
    """
    Vérifie et crée le dossier parent du fichier si besoin.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        logger.info("Dossier créé : %s", directory)


def get_default_pdf_path(section_name=None, base_dir="data/output", prefix="rapport", ext="pdf"):
    """
    Génère un nom de fichier PDF unique avec timestamp + section.
    """
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d_%H-%M")
    section_part = f"_{section_name.replace(' ', '_')}" if section_name else ""
    filename = f"{prefix}_{date_str}{section_part}.{ext}"
    return os.path.join(base_dir, filename)


def export_pdf_file(pdf_bytes, path):
    """
    Sauvegarde un PDF à partir d’un buffer de bytes.
    """
    try:
        ensure_directory_exists(path)
        with open(path, "wb") as f:
            f.write(pdf_bytes)
        logger.info("PDF exporté : %s", path)
        return True
    except Exception as e:
        logger.error("Erreur export PDF dans %s : %s", path, str(e))
        return False


# --- Gestion de config (JSON) ---

def load_config(path):
    """
    Charge un fichier JSON (config) et retourne un dictionnaire.
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
        logger.error("Erreur lecture config : %s — %s", path, str(e))
        return {}


def save_config(config, path):
    """
    Sauvegarde un dictionnaire de configuration en fichier JSON.
    """
    try:
        ensure_directory_exists(path)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        logger.info("Config sauvegardée dans : %s", path)
        return True
    except Exception as e:
        logger.error("Sauvegarde config échouée pour %s : %s", path, str(e))
        return False


# --- Exports explicites (optionnel) ---
__all__ = [
    "write_csv", "read_csv",
    "export_dataframe_to_csv", "ensure_directory_exists",
    "get_default_pdf_path", "export_pdf_file",
    "load_config", "save_config"
]

# --- Exemples d'utilisation ---
# export_dataframe_to_csv(df, "data/output/simulations.csv")          # Simple
# export_dataframe_to_csv(dict_scenarios, "data/output/scen_multi.csv", mode='single')   # Multi-concaténé
# export_dataframe_to_csv(dict_scenarios, "data/output/scen_multi", mode='split')        # Multi-fichiers
# pdf_path = get_default_pdf_path(section_name="comparaison")
# export_pdf_file(pdf_bytes, pdf_path)
# cfg = load_config("data/config/parametres.json")
# save_config({"IX": 123, "IY": 456, "IZ": 789}, "data/config/parametres.json")
