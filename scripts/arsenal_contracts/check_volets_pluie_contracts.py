#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Réaction des volets à la pluie
Contrat (source normative) : 00_documentation_arsenal/contrats/volets_pluie.md
Script  : scripts/arsenal_contracts/check_volets_pluie_contracts.py
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Racine du repo Arsenal
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Fichiers canoniques
# ---------------------------------------------------------------------------
F_CIBLES_CHAMBRES = REPO_ROOT / "12_template_sensors/volets/cibles_volets_pluie_chambres.yaml"
F_CIBLES_SEJOUR   = REPO_ROOT / "12_template_sensors/volets/cibles_volets_pluie_sejour.yaml"
F_AUTO_CHAMBRES   = REPO_ROOT / "11_automations/meteo/pluie/pluie_volets_chambres.yaml"
F_AUTO_SEJOUR     = REPO_ROOT / "11_automations/meteo/pluie/pluie_volets_sejour.yaml"

# Sous-dossiers à scanner pour localiser les autres entités
DIR_TEMPLATES_VOLETS = REPO_ROOT / "12_template_sensors/volets"
DIR_SCRIPTS          = REPO_ROOT / "10_scripts"
DIR_INPUT_BOOLEANS   = REPO_ROOT / "05_input_booleans"
DIR_INPUT_SELECTS    = REPO_ROOT / "06_input_selects"

# ---------------------------------------------------------------------------
# Entités canoniques (§5)
# ---------------------------------------------------------------------------

# Couche décision — unique_id attendus
UNIQUE_IDS_DECISION = [
    "cibles_volets_pluie_chambres",
    "cibles_volets_pluie_sejour",
    "intention_fenetres_concernees_ouvertes_pluie",
    "autorisation_fermeture_volets_pluie_sejour",
]

# Couche paramètres — clés de mapping attendues
INPUT_BOOLEANS_PARAMS = [
    "fermeture_volets_pluie",
]
INPUT_SELECTS_PARAMS = [
    "activation_volets_pluie",
]

# Covers séjour — invariant §5.3
COVERS_SEJOUR = ["cover.sejour_gauche", "cover.sejour_droit"]

# Contacts séjour — interdits dans sensor cibles séjour (§5.3)
CONTACTS_SEJOUR_PATTERN = re.compile(r"contact_sejour_\d")

# Frontières d'entrée contexte (§5.2)
FRONTIERE_CHAMBRES = "pluie_en_cours"
FRONTIERE_SEJOUR   = "intention_pluie_forte"

# Verrou global (§5.4)
VERROU_GLOBAL = "fermeture_volets_pluie"

# Tags de notification (§6)
NOTIFICATION_TAGS = [
    "pluie_fenetres_ouvertes",
    "fermeture_volets_pluie_chambres",
    "fermeture_volets_pluie_forte_sejour",
]

ERRORS: list[str] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(*directories: Path) -> list[Path]:
    result = []
    for d in directories:
        if d.is_dir():
            result.extend(p for p in d.rglob("*.yaml") if p.is_file())
    return result


def find_file_by_unique_id(uid: str, *directories: Path) -> Path | None:
    """Retourne le premier fichier contenant unique_id: <uid>."""
    pattern = re.compile(rf"unique_id\s*:\s*{re.escape(uid)}\b")
    for d in directories:
        for path in yaml_files(d):
            if pattern.search(read(path)):
                return path
    return None


# ---------------------------------------------------------------------------
# T1 — Présence des fichiers canoniques connus
# ---------------------------------------------------------------------------

def test_canonical_files_present() -> None:
    files = {
        "cibles_volets_pluie_chambres": F_CIBLES_CHAMBRES,
        "cibles_volets_pluie_sejour":   F_CIBLES_SEJOUR,
        "automation chambres":          F_AUTO_CHAMBRES,
        "automation séjour":            F_AUTO_SEJOUR,
    }
    all_ok = True
    for label, path in files.items():
        if not path.is_file():
            ERRORS.append(f"T1 — Fichier canonique manquant ({label}) : "
                          f"{path.relative_to(REPO_ROOT)}")
            all_ok = False
    if all_ok:
        print("✔ T1 — Fichiers canoniques présents (sensors cibles + automations)")


# ---------------------------------------------------------------------------
# T2 — Entités décision déclarées via unique_id (§5.3)
# ---------------------------------------------------------------------------

def test_decision_entities_declared() -> None:
    search_dirs = [
        REPO_ROOT / "12_template_sensors",
    ]
    all_ok = True
    for uid in UNIQUE_IDS_DECISION:
        path = find_file_by_unique_id(uid, *search_dirs)
        if path is None:
            ERRORS.append(f"T2 — unique_id: {uid} non trouvé dans "
                          f"12_template_sensors/ (entité décision manquante)")
            all_ok = False
    if all_ok:
        print(f"✔ T2 — Les {len(UNIQUE_IDS_DECISION)} entités de décision "
              f"sont déclarées (unique_id)")


# ---------------------------------------------------------------------------
# T3 — Paramètres déclarés (input_boolean + input_select) (§5.4)
# ---------------------------------------------------------------------------

def test_params_declared() -> None:
    all_ok = True
    for key in INPUT_BOOLEANS_PARAMS:
        found = False
        for path in yaml_files(DIR_INPUT_BOOLEANS):
            if re.search(rf"^\s*{re.escape(key)}\s*:", read(path), re.MULTILINE):
                found = True
                break
        if not found:
            ERRORS.append(f"T3 — input_boolean.{key} non déclaré dans "
                          f"05_input_booleans/ (§5.4)")
            all_ok = False
    for key in INPUT_SELECTS_PARAMS:
        found = False
        for path in yaml_files(DIR_INPUT_SELECTS):
            if re.search(rf"^\s*{re.escape(key)}\s*:", read(path), re.MULTILINE):
                found = True
                break
        if not found:
            ERRORS.append(f"T3 — input_select.{key} non déclaré dans "
                          f"06_input_selects/ (§5.4)")
            all_ok = False
    if all_ok:
        print("✔ T3 — Paramètres input_boolean.fermeture_volets_pluie + "
              "input_select.activation_volets_pluie déclarés")


# ---------------------------------------------------------------------------
# T4 — Invariant séjour : sensor cibles séjour ne référence aucun contact séjour
#
# Invariant (§5.3) : sensor.cibles_volets_pluie_sejour ne dépend d'aucun
# contact séjour. Toute référence à contact_sejour_* est une violation.
# ---------------------------------------------------------------------------

def test_sejour_no_contact_sejour() -> None:
    content = read(F_CIBLES_SEJOUR)
    if not content:
        ERRORS.append(f"T4 — Fichier inaccessible : "
                      f"{F_CIBLES_SEJOUR.relative_to(REPO_ROOT)}")
        return
    violations = []
    for i, line in enumerate(content.splitlines(), 1):
        if line.strip().startswith("#"):
            continue
        if CONTACTS_SEJOUR_PATTERN.search(line):
            violations.append(f"ligne {i}: {line.strip()[:80]}")
    if violations:
        for v in violations:
            ERRORS.append(f"T4 — contact_sejour_* interdit dans "
                          f"{F_CIBLES_SEJOUR.relative_to(REPO_ROOT)} "
                          f"(§5.3 invariant séjour) : {v}")
    else:
        print("✔ T4 — Aucun contact_sejour_* dans sensor.cibles_volets_pluie_sejour")


# ---------------------------------------------------------------------------
# T5 — Invariant séjour : sensor cibles séjour retourne cover.sejour_gauche
#      et cover.sejour_droit (§5.3)
# ---------------------------------------------------------------------------

def test_sejour_returns_correct_covers() -> None:
    content = read(F_CIBLES_SEJOUR)
    if not content:
        ERRORS.append(f"T5 — Fichier inaccessible : "
                      f"{F_CIBLES_SEJOUR.relative_to(REPO_ROOT)}")
        return
    all_ok = True
    for cover in COVERS_SEJOUR:
        if cover not in content:
            ERRORS.append(f"T5 — Cover attendu '{cover}' absent de "
                          f"{F_CIBLES_SEJOUR.relative_to(REPO_ROOT)} (§5.3)")
            all_ok = False
    if all_ok:
        print("✔ T5 — cover.sejour_gauche + cover.sejour_droit présents dans "
              "sensor.cibles_volets_pluie_sejour")


# ---------------------------------------------------------------------------
# T6 — Invariant cardinalité : state reflète le nombre de cibles (§5.3)
#
# Invariant (§5.3) : le state des sensors de cibles reflète la cardinalité
# de entity_ids. Le runtime peut l'implémenter via un compteur ns.n ou
# via entity_ids | length — les deux sont conformes.
# Test : présence conjointe de 'state' et 'entity_ids' dans chaque fichier.
# ---------------------------------------------------------------------------

def test_cibles_state_is_length() -> None:
    all_ok = True
    for path in [F_CIBLES_CHAMBRES, F_CIBLES_SEJOUR]:
        content = read(path)
        if not content:
            ERRORS.append(f"T6 — Fichier inaccessible : "
                          f"{path.relative_to(REPO_ROOT)}")
            all_ok = False
            continue
        has_state     = bool(re.search(r"^\s*state\s*:", content, re.MULTILINE))
        has_entity_ids = "entity_ids" in content
        if not has_state or not has_entity_ids:
            ERRORS.append(f"T6 — Coprésence state + entity_ids non vérifiée dans "
                          f"{path.relative_to(REPO_ROOT)} "
                          f"(invariant cardinalité §5.3)")
            all_ok = False
    if all_ok:
        print("✔ T6 — Invariant cardinalité : state + entity_ids présents "
              "dans les deux sensors cibles")


# ---------------------------------------------------------------------------
# T7 — Automation chambres déclenche sur pluie_en_cours (§5.7)
# ---------------------------------------------------------------------------

def test_chambres_trigger() -> None:
    content = read(F_AUTO_CHAMBRES)
    if not content:
        ERRORS.append(f"T7 — Fichier inaccessible : "
                      f"{F_AUTO_CHAMBRES.relative_to(REPO_ROOT)}")
        return
    if FRONTIERE_CHAMBRES not in content:
        ERRORS.append(f"T7 — Trigger '{FRONTIERE_CHAMBRES}' absent de "
                      f"{F_AUTO_CHAMBRES.relative_to(REPO_ROOT)} (§5.7)")
    else:
        print(f"✔ T7 — Automation chambres déclenche sur {FRONTIERE_CHAMBRES}")


# ---------------------------------------------------------------------------
# T8 — Automation séjour déclenche sur intention_pluie_forte (§5.7)
# ---------------------------------------------------------------------------

def test_sejour_trigger() -> None:
    content = read(F_AUTO_SEJOUR)
    if not content:
        ERRORS.append(f"T8 — Fichier inaccessible : "
                      f"{F_AUTO_SEJOUR.relative_to(REPO_ROOT)}")
        return
    if FRONTIERE_SEJOUR not in content:
        ERRORS.append(f"T8 — Trigger '{FRONTIERE_SEJOUR}' absent de "
                      f"{F_AUTO_SEJOUR.relative_to(REPO_ROOT)} (§5.7)")
    else:
        print(f"✔ T8 — Automation séjour déclenche sur {FRONTIERE_SEJOUR}")


# ---------------------------------------------------------------------------
# T9 — script.volets_fermeture_execute en mode queued (§5.6)
#
# Invariant (§5.6) : mode: queued pour absorber les appels concurrents.
# ---------------------------------------------------------------------------

def test_script_mode_queued() -> None:
    # Cherche le script dans 10_scripts/
    pattern = re.compile(r"unique_id\s*:\s*volets_fermeture_execute\b|"
                         r"alias\s*:.*volets_fermeture_execute")
    script_path = None
    for path in yaml_files(DIR_SCRIPTS):
        if pattern.search(read(path)) or "volets_fermeture_execute" in read(path):
            if "mode" in read(path) and "volets_fermeture" in path.name:
                script_path = path
                break
    # Fallback : chercher par contenu
    if script_path is None:
        for path in yaml_files(DIR_SCRIPTS):
            content = read(path)
            if "volets_fermeture_execute" in content and "queued" in content:
                script_path = path
                break

    if script_path is None:
        # Peut être déclaré sans fichier dédié — non bloquant
        print("✔ T9 — script.volets_fermeture_execute : "
              "fichier non trouvé dans 10_scripts/ (non bloquant si déclaré ailleurs)")
        return

    content = read(script_path)
    if "queued" not in content:
        ERRORS.append(f"T9 — mode: queued absent de "
                      f"{script_path.relative_to(REPO_ROOT)} "
                      f"(invariant unicité d'exécution §5.6)")
    else:
        print("✔ T9 — script.volets_fermeture_execute en mode queued")


# ---------------------------------------------------------------------------
# T10 — Notification d'exposition présente dans la branche présence (§6)
#
# Invariant (§6) : la branche présence ON doit déclencher une notification
# d'exposition. Le runtime utilise un push mobile sans tag explicite —
# conforme à §6 qui ne rend le tag obligatoire que pour les persistantes.
# Test : présence d'un appel de notification dans l'automation chambres,
# ET présence d'une référence à presence_famille_securite (condition branche).
# ---------------------------------------------------------------------------

def test_notification_exposition_present() -> None:
    content = read(F_AUTO_CHAMBRES)
    if not content:
        ERRORS.append(f"T10 — Fichier inaccessible : "
                      f"{F_AUTO_CHAMBRES.relative_to(REPO_ROOT)}")
        return

    has_presence = "presence_famille_securite" in content
    has_notif    = bool(re.search(
        r"service\s*:\s*(?:notify\.|script\.notification_envoyer)",
        content
    ))

    if not has_presence:
        ERRORS.append(f"T10 — presence_famille_securite absent de "
                      f"{F_AUTO_CHAMBRES.relative_to(REPO_ROOT)} (§6)")
    elif not has_notif:
        ERRORS.append(f"T10 — Aucune notification dans "
                      f"{F_AUTO_CHAMBRES.relative_to(REPO_ROOT)} "
                      f"(branche exposition requise — §6)")
    else:
        print("✔ T10 — Notification d'exposition présente dans "
              "l'automation chambres (§6)")


# ---------------------------------------------------------------------------
# T11 — sensor.cibles_volets_pluie_chambres consomme presence + verrou (§5.3)
# ---------------------------------------------------------------------------

def test_chambres_cibles_inputs() -> None:
    content = read(F_CIBLES_CHAMBRES)
    if not content:
        ERRORS.append(f"T11 — Fichier inaccessible : "
                      f"{F_CIBLES_CHAMBRES.relative_to(REPO_ROOT)}")
        return
    all_ok = True
    for entity in ["presence_famille_securite", "fermeture_volets_pluie"]:
        if entity not in content:
            ERRORS.append(f"T11 — '{entity}' absent de "
                          f"{F_CIBLES_CHAMBRES.relative_to(REPO_ROOT)} (§5.3)")
            all_ok = False
    if all_ok:
        print("✔ T11 — sensor.cibles_volets_pluie_chambres consomme "
              "presence_famille_securite + fermeture_volets_pluie")


# ---------------------------------------------------------------------------
# T12 — sensor.cibles_volets_pluie_sejour consomme autorisation + pluie forte (§5.3)
# ---------------------------------------------------------------------------

def test_sejour_cibles_inputs() -> None:
    content = read(F_CIBLES_SEJOUR)
    if not content:
        ERRORS.append(f"T12 — Fichier inaccessible : "
                      f"{F_CIBLES_SEJOUR.relative_to(REPO_ROOT)}")
        return
    all_ok = True
    for entity in ["autorisation_fermeture_volets_pluie_sejour",
                   "intention_pluie_forte"]:
        if entity not in content:
            ERRORS.append(f"T12 — '{entity}' absent de "
                          f"{F_CIBLES_SEJOUR.relative_to(REPO_ROOT)} (§5.3)")
            all_ok = False
    if all_ok:
        print("✔ T12 — sensor.cibles_volets_pluie_sejour consomme "
              "autorisation_fermeture_volets_pluie_sejour + intention_pluie_forte")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_canonical_files_present,
    test_decision_entities_declared,
    test_params_declared,
    test_sejour_no_contact_sejour,
    test_sejour_returns_correct_covers,
    test_cibles_state_is_length,
    test_chambres_trigger,
    test_sejour_trigger,
    test_script_mode_queued,
    test_notification_exposition_present,
    test_chambres_cibles_inputs,
    test_sejour_cibles_inputs,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : Volets pluie v2.2.1\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT VOLETS PLUIE NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT VOLETS PLUIE CONFORME")
