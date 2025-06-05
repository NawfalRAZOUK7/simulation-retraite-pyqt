# ui/results_window/csv_sort_utils.py

import os
import json

DEFAULT_PATH = "data/config/tab_csv_import_sort.json"

def save_sort_config(columns, orders, path=DEFAULT_PATH):
    """
    Sauvegarde la configuration de tri (colonnes + ordre) au format JSON.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"columns": columns, "orders": orders}, f)
    except Exception as e:
        print(f"[csv_sort_utils] Erreur sauvegarde tri : {e}")

def load_sort_config(path=DEFAULT_PATH):
    """
    Charge la configuration de tri (colonnes + ordre) depuis un JSON.
    Retourne (columns, orders), ou ([], []) si aucun tri trouvé.
    """
    if not os.path.exists(path):
        return [], []
    try:
        with open(path, "r", encoding="utf-8") as f:
            obj = json.load(f)
        return obj.get("columns", []), obj.get("orders", [])
    except Exception as e:
        print(f"[csv_sort_utils] Erreur lecture tri : {e}")
        return [], []
