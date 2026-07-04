#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle M5 : Réouverture pendant blocage
Source normative : 00_documentation_arsenal/contrats/aeration_blocage_chauffage/m5_reouverture/
Contrats :
  - 1_reouverture_pendant_blocage.md  (cadre général M5)
  - 2_interaction_avec_m3.md          (interaction M5 / M3)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ERRORS = []


def check(label: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  ✔ {label}")
    else:
        ERRORS.append(f"{label}{': ' + detail if detail else ''}")


# ===========================================================================
# BLOC A — Présence des entités canoniques
# ===========================================================================

def test_declaration_suspension_active():
    """T01 — input_boolean.aeration_suspension_active déclaré (clé mapping)."""
    f = ROOT / "05_input_booleans/aeration/suspension_aeration.yaml"
    if not f.is_file():
        ERRORS.append("T01: fichier déclaratif introuvable: " + str(f.relative_to(ROOT)))
        return
    content = f.read_text(encoding="utf-8", errors="ignore")
    found = bool(re.search(r"^\s*aeration_suspension_active\s*:", content, re.MULTILINE))
    check("T01 — aeration_suspension_active déclaré",
          found, f"clé manquante dans {f.relative_to(ROOT)}")


def test_declaration_reouverture_last():
    """T02 — input_datetime.aeration_reouverture_last déclaré (clé mapping)."""
    f = ROOT / "07_input_datetimes/aeration/derniere_ouverture.yaml"
    if not f.is_file():
        ERRORS.append("T02: fichier déclaratif introuvable: " + str(f.relative_to(ROOT)))
        return
    content = f.read_text(encoding="utf-8", errors="ignore")
    found = bool(re.search(r"^\s*aeration_reouverture_last\s*:", content, re.MULTILINE))
    check("T02 — aeration_reouverture_last déclaré",
          found, f"clé manquante dans {f.relative_to(ROOT)}")


def test_declaration_timer_analyse():
    """T03 — timer.aeration_analyse_delta_t déclaré (clé mapping)."""
    f = ROOT / "08_timers/aeration/analyse_delta_t.yaml"
    if not f.is_file():
        ERRORS.append("T03: fichier déclaratif introuvable: " + str(f.relative_to(ROOT)))
        return
    content = f.read_text(encoding="utf-8", errors="ignore")
    found = bool(re.search(r"^\s*aeration_analyse_delta_t\s*:", content, re.MULTILINE))
    check("T03 — aeration_analyse_delta_t déclaré",
          found, f"clé manquante dans {f.relative_to(ROOT)}")


def test_declaration_delai_stabilisation():
    """T04 — input_number.delai_stabilisation_capteurs déclaré (clé mapping)."""
    f = ROOT / "03_input_numbers/aeration/blocage_chauffage/delai_stabilisation_capteurs.yaml"
    if not f.is_file():
        ERRORS.append("T04: fichier déclaratif introuvable: " + str(f.relative_to(ROOT)))
        return
    content = f.read_text(encoding="utf-8", errors="ignore")
    found = bool(re.search(r"^\s*delai_stabilisation_capteurs\s*:", content, re.MULTILINE))
    check("T04 — delai_stabilisation_capteurs déclaré",
          found, f"clé manquante dans {f.relative_to(ROOT)}")


# ===========================================================================
# BLOC B — Existence du script M5
# ===========================================================================

def test_script_m5_existe():
    """T05 — Fichier script M5 présent."""
    f = ROOT / "10_scripts/aeration/m5_reouverture_pendant_blocage.yaml"
    check("T05 — script m5_reouverture_pendant_blocage.yaml présent",
          f.is_file(), str(f.relative_to(ROOT)))


# ===========================================================================
# BLOC C — Effets normatifs M5 (contrat 1)
# ===========================================================================

def test_m5_active_suspension():
    """T06 — M5 active aeration_suspension_active (turn_on).
    Coprésence input_boolean.turn_on + aeration_suspension_active dans 300 chars.
    """
    f = ROOT / "10_scripts/aeration/m5_reouverture_pendant_blocage.yaml"
    if not f.is_file():
        ERRORS.append("T06: script M5 introuvable, test ignoré")
        return
    content = f.read_text(encoding="utf-8", errors="ignore")
    pattern = re.compile(
        r"input_boolean\.turn_on.{1,300}aeration_suspension_active|"
        r"aeration_suspension_active.{1,300}input_boolean\.turn_on",
        re.DOTALL,
    )
    check("T06 — M5 active aeration_suspension_active",
          bool(pattern.search(content)),
          "turn_on + entité absents ou trop éloignés dans m5_reouverture_pendant_blocage.yaml")


def test_m5_horodate_reouverture():
    """T07 — M5 horodate aeration_reouverture_last (set_datetime).
    Coprésence input_datetime.set_datetime + aeration_reouverture_last dans 300 chars.
    """
    f = ROOT / "10_scripts/aeration/m5_reouverture_pendant_blocage.yaml"
    if not f.is_file():
        ERRORS.append("T07: script M5 introuvable, test ignoré")
        return
    content = f.read_text(encoding="utf-8", errors="ignore")
    pattern = re.compile(
        r"input_datetime\.set_datetime.{1,300}aeration_reouverture_last|"
        r"aeration_reouverture_last.{1,300}input_datetime\.set_datetime",
        re.DOTALL,
    )
    check("T07 — M5 horodate aeration_reouverture_last",
          bool(pattern.search(content)),
          "set_datetime + aeration_reouverture_last absents ou trop éloignés dans m5_reouverture_pendant_blocage.yaml")


def test_m5_reference_timer_analyse():
    """T08 — M5 référence timer.aeration_analyse_delta_t (redémarrage monotone attendu)."""
    f = ROOT / "10_scripts/aeration/m5_reouverture_pendant_blocage.yaml"
    if not f.is_file():
        ERRORS.append("T08: script M5 introuvable, test ignoré")
        return
    content = f.read_text(encoding="utf-8", errors="ignore")
    check("T08 — M5 référence timer.aeration_analyse_delta_t",
          "timer.aeration_analyse_delta_t" in content,
          "entité absente de m5_reouverture_pendant_blocage.yaml")


def test_m5_reference_timer_blocage():
    """T09 — M5 référence timer.aeration_blocage (redémarrage monotone attendu)."""
    f = ROOT / "10_scripts/aeration/m5_reouverture_pendant_blocage.yaml"
    if not f.is_file():
        ERRORS.append("T09: script M5 introuvable, test ignoré")
        return
    content = f.read_text(encoding="utf-8", errors="ignore")
    check("T09 — M5 référence timer.aeration_blocage",
          "timer.aeration_blocage" in content,
          "entité absente de m5_reouverture_pendant_blocage.yaml")


# ===========================================================================
# BLOC D — Interdits M5 (contrats 1 & 2)
# ===========================================================================

def test_m5_interdit_ecriture_blocage():
    """T10 — M5 n'écrit pas chauffage_blocage_aeration.
    Interdit absolu : lever ou modifier le blocage n'est pas de la compétence de M5.
    Scope : fichier M5 uniquement.
    Lectures passives (is_state, states) non ciblées.
    """
    f = ROOT / "10_scripts/aeration/m5_reouverture_pendant_blocage.yaml"
    if not f.is_file():
        ERRORS.append("T10: script M5 introuvable, test ignoré")
        return
    content = f.read_text(encoding="utf-8", errors="ignore")
    pattern = re.compile(
        r"input_boolean\.turn_(?:on|off).{1,300}chauffage_blocage_aeration|"
        r"chauffage_blocage_aeration.{1,300}input_boolean\.turn_(?:on|off)",
        re.DOTALL,
    )
    check("T10 — M5 n'écrit pas chauffage_blocage_aeration",
          not bool(pattern.search(content)),
          "écriture détectée sur chauffage_blocage_aeration dans m5_reouverture_pendant_blocage.yaml")


def test_m5_interdit_ecriture_pipeline_arme():
    """T11 — M5 n'écrit pas aeration_pipeline_arme.
    Interdit absolu : désarmer ou modifier le pipeline n'est pas de la compétence de M5.
    Scope : fichier M5 uniquement.
    """
    f = ROOT / "10_scripts/aeration/m5_reouverture_pendant_blocage.yaml"
    if not f.is_file():
        ERRORS.append("T11: script M5 introuvable, test ignoré")
        return
    content = f.read_text(encoding="utf-8", errors="ignore")
    pattern = re.compile(
        r"input_boolean\.turn_(?:on|off).{1,300}aeration_pipeline_arme|"
        r"aeration_pipeline_arme.{1,300}input_boolean\.turn_(?:on|off)",
        re.DOTALL,
    )
    check("T11 — M5 n'écrit pas aeration_pipeline_arme",
          not bool(pattern.search(content)),
          "écriture détectée sur aeration_pipeline_arme dans m5_reouverture_pendant_blocage.yaml")


def test_m5_interdit_appel_m3():
    """T12 — M5 n'appelle pas directement M3.
    Interdit contrat 2 : la décision ΔT reste exclusivement de compétence M3.
    Scope : fichier M5 uniquement.
    Pattern : coprésence script.turn + m3 dans 200 chars.
    """
    f = ROOT / "10_scripts/aeration/m5_reouverture_pendant_blocage.yaml"
    if not f.is_file():
        ERRORS.append("T12: script M5 introuvable, test ignoré")
        return
    content = f.read_text(encoding="utf-8", errors="ignore")
    # Détecte un appel script.turn (script.turn_on ou script.<id>) ciblant un script m3_*
    pattern = re.compile(
        r"script\.turn_on.{1,200}m3_|"
        r"script\.aeration_m3",
        re.DOTALL | re.IGNORECASE,
    )
    check("T12 — M5 n'appelle pas M3 directement",
          not bool(pattern.search(content)),
          "appel direct à un script m3_* détecté dans m5_reouverture_pendant_blocage.yaml")


def test_m5_consomme_delai_stabilisation():
    """T13 — M5 consomme delai_stabilisation_capteurs (lecture attendue par contrat 2).
    Vérifie la présence de l'entity_id dans le fichier M5.
    """
    f = ROOT / "10_scripts/aeration/m5_reouverture_pendant_blocage.yaml"
    if not f.is_file():
        ERRORS.append("T13: script M5 introuvable, test ignoré")
        return
    content = f.read_text(encoding="utf-8", errors="ignore")
    check("T13 — M5 consomme delai_stabilisation_capteurs",
          "delai_stabilisation_capteurs" in content,
          "entité absente de m5_reouverture_pendant_blocage.yaml")


# ===========================================================================
# Registre des tests
# ===========================================================================

TESTS = [
    test_declaration_suspension_active,
    test_declaration_reouverture_last,
    test_declaration_timer_analyse,
    test_declaration_delai_stabilisation,
    test_script_m5_existe,
    test_m5_active_suspension,
    test_m5_horodate_reouverture,
    test_m5_reference_timer_analyse,
    test_m5_reference_timer_blocage,
    test_m5_interdit_ecriture_blocage,
    test_m5_interdit_ecriture_pipeline_arme,
    test_m5_interdit_appel_m3,
    test_m5_consomme_delai_stabilisation,
]

if __name__ == "__main__":
    print("=== Arsenal — Contrat M5 : Réouverture pendant blocage ===\n")
    for t in TESTS:
        t()
    print()
    if ERRORS:
        print("❌ CONTRAT M5 NON CONFORME")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("✅ CONTRAT M5 CONFORME")
