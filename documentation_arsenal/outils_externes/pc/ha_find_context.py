#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Recherche d'entité Home Assistant — AVEC CONTEXTE
-------------------------------------------------
Fonctionnalités :
 - Demande une entité Home Assistant via boîte de dialogue
 - Recherche récursive dans C:\HA\data
 - Exclut les dossiers techniques
 - Affiche 5 lignes avant / après chaque occurrence
 - Génère un fichier résultat détaillé dans C:\HA\results
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

LIGNES_CONTEXTE = 5


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
            f"Dossier introuvable :\n\n{ROOT_DIR}"
        )
        return

    # --------------------------------------------------------
    # 2) Saisie de l'entité
    # --------------------------------------------------------
    entity = simpledialog.askstring(
        "Recherche entité Home Assistant (contexte)",
        "Entité à rechercher :"
    )

    if not entity:
        return

    entity = entity.strip()
    entity_lower = entity.lower()

    results = []
    occurrences = 0

    # --------------------------------------------------------
    # 3) Recherche avec contexte
    # --------------------------------------------------------
    for file in ROOT_DIR.rglob("*"):
        if not file.is_file():
            continue
        if is_excluded(file):
            continue
        if file.suffix.lower() not in EXTENSIONS_AUTORISEES:
            continue

        lines = read_text_safe(file)
        if not lines:
            continue

        total_lines = len(lines)

        for idx, line in enumerate(lines, start=1):
            if entity_lower in line.lower():
                occurrences += 1

                start = max(1, idx - LIGNES_CONTEXTE)
                end = min(total_lines, idx + LIGNES_CONTEXTE)

                block = [
                    "\n------------------------------------------------------------",
                    f"Fichier : {file}",
                    f"Ligne   : {idx}",
                    "------------------------------------------------------------"
                ]

                for i in range(start, end + 1):
                    prefix = ">>>" if i == idx else "   "
                    block.append(f"{prefix} {i:4d} | {lines[i - 1]}")

                results.append("\n".join(block))

    # --------------------------------------------------------
    # 4) Écriture du fichier résultat
    # --------------------------------------------------------
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = OUT_DIR / f"recherche_contexte_{entity}_{timestamp}.txt"

    header = (
        "============================================================\n"
        "Recherche d'entité Home Assistant — AVEC CONTEXTE\n"
        "------------------------------------------------------------\n"
        f"Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Racine : {ROOT_DIR}\n"
        f"Entité : {entity}\n"
        f"Résultats : {occurrences} occurrence(s)\n"
        "============================================================\n"
    )

    content = header + ("\n\n".join(results) if results else "\nAucune occurrence trouvée.\n")
    out_file.write_text(content, encoding="utf-8")

    # --------------------------------------------------------
    # 5) Message final
    # --------------------------------------------------------
    messagebox.showinfo(
        "Recherche terminée",
        f"Occurrences trouvées : {occurrences}\n\n"
        f"Fichier généré :\n{out_file}"
    )


if __name__ == "__main__":
    main()
