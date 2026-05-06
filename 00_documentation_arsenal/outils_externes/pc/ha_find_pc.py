#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Recherche d'entité Home Assistant
---------------------------------
Fonctionnalités :
 - Demande une entité Home Assistant via boîte de dialogue
 - Recherche récursive dans C:\HA\data
 - Exclut les dossiers techniques (.storage, .git, etc.)
 - Génère un fichier résultat dans C:\HA\results
 - Message final avec nombre d'occurrences
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
from pathlib import Path
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================

ROOT_DIR = Path(r"C:\HA\data")
OUT_DIR = Path(r"C:\HA\results")

EXTENSIONS_AUTORISEES = {
    ".yaml", ".yml", ".json", ".txt", ".j2", ".jinja", ".jinja2", ".md"
}

DOSSIERS_EXCLUS = {
    ".storage", ".git", "__pycache__", "deps", "node_modules"
}


# ============================================================
# UTILITAIRES
# ============================================================

def is_excluded(path: Path) -> bool:
    return any(part in DOSSIERS_EXCLUS for part in path.parts)


def read_text_safe(path: Path) -> list[str] | None:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="cp1252", errors="replace").splitlines()
        except Exception:
            return None
    except Exception:
        return None


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main():
    root = tk.Tk()
    root.withdraw()

    # --------------------------------------------------------
    # 1) Vérification du dossier racine
    # --------------------------------------------------------
    if not ROOT_DIR.exists():
        messagebox.showerror(
            "Recherche entité HA",
            f"Le dossier suivant est introuvable :\n\n{ROOT_DIR}\n\n"
            "Vérifie que la sauvegarde est bien extraite."
        )
        return

    # --------------------------------------------------------
    # 2) Saisie de l'entité
    # --------------------------------------------------------
    entity = simpledialog.askstring(
        "Recherche entité Home Assistant",
        "Entité à rechercher :\n\n"
        "Exemple : input_boolean.lumiere_jardin_allumee_par_ha"
    )

    if not entity:
        return

    entity = entity.strip()
    entity_lower = entity.lower()

    # --------------------------------------------------------
    # 3) Recherche
    # --------------------------------------------------------
    results = []
    occurrences = 0

    for file in ROOT_DIR.rglob("*"):
        if not file.is_file():
            continue
        if is_excluded(file):
            continue
        if file.suffix.lower() not in EXTENSIONS_AUTORISEES:
            continue

        lines = read_text_safe(file)
        if lines is None:
            continue

        for idx, line in enumerate(lines, start=1):
            if entity_lower in line.lower():
                results.append(
                    f"{file}\n"
                    f"  Ligne {idx}: {line.strip()}\n"
                )
                occurrences += 1

    # --------------------------------------------------------
    # 4) Écriture du fichier résultat
    # --------------------------------------------------------
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = OUT_DIR / f"recherche_{entity}_{timestamp}.txt"

    header = (
        "============================================================\n"
        "Recherche d'entité Home Assistant\n"
        "------------------------------------------------------------\n"
        f"Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Racine : {ROOT_DIR}\n"
        f"Entité : {entity}\n"
        f"Résultats : {occurrences} occurrence(s)\n"
        "============================================================\n\n"
    )

    if results:
        content = header + "\n".join(results)
    else:
        content = header + "Aucune occurrence trouvée.\n"

    out_file.write_text(content, encoding="utf-8")

    # --------------------------------------------------------
    # 5) Message final
    # --------------------------------------------------------
    messagebox.showinfo(
        "Recherche terminée",
        f"Recherche terminée.\n\n"
        f"Occurrences trouvées : {occurrences}\n\n"
        f"Fichier généré :\n{out_file}"
    )


if __name__ == "__main__":
    main()
