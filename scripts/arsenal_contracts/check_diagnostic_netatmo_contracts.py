#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arsenal — Validation contractuelle
Domaine : Diagnostic station meteo Netatmo
Contrat : v1.1 (couche observation)

Le script verifie les invariants testables sans ambiguite du contrat
v1.1, en se restreignant au fichier canonique pour les invariants
structurels, et au repo entier (hors documentation) pour l'invariant
de non-regression du renommage v1.0 -> v1.1.

Aucune dependance externe.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Racine du repo Arsenal
# ---------------------------------------------------------------------------
# Convention Arsenal : scripts/arsenal_contracts/check_<domaine>_contracts.py
# donc ROOT = parents[2]
ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Chemins canoniques (confirmes par recherche runtime)
# ---------------------------------------------------------------------------
CANONICAL_FILE = (
    ROOT
    / "12_template_sensors"
    / "system"
    / "connectivite"
    / "netatmo"
    / "homekit.yaml"
)

TEMPLATE_SENSORS_DIR = ROOT / "12_template_sensors"
DOCUMENTATION_DIR = ROOT / "00_documentation_arsenal"

# ---------------------------------------------------------------------------
# Constantes contractuelles
# ---------------------------------------------------------------------------
UNIQUE_IDS = (
    "diagnostic_netatmo_arnaud",
    "diagnostic_netatmo_matthieu",
)

CONTRACT_STATES = ("ok", "muet_ping_ok", "muet_ping_ko")

# Anciens noms v1.0 - interdits dans tout le runtime fonctionnel.
LEGACY_STATES = ("ko_homekit", "ko_reseau")

# Extensions scannees pour la non-regression des anciens noms.
SCANNED_EXTENSIONS = (".yaml", ".yml")

# ---------------------------------------------------------------------------
# Accumulateur d'erreurs
# ---------------------------------------------------------------------------
ERRORS: list[str] = []


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_canonical_file_exists() -> None:
    """T1 - Le fichier canonique existe."""
    if not CANONICAL_FILE.is_file():
        ERRORS.append(
            f"T1 - Fichier canonique introuvable : "
            f"{CANONICAL_FILE.relative_to(ROOT)}"
        )
        return
    print(f"✔ T1 - Fichier canonique present : "
          f"{CANONICAL_FILE.relative_to(ROOT)}")


def test_unique_ids_present_in_canonical_file() -> None:
    """T2 - Les deux unique_id sont presents dans le fichier canonique."""
    if not CANONICAL_FILE.is_file():
        ERRORS.append("T2 - Saute (T1 a echoue)")
        return
    content = _read(CANONICAL_FILE)
    missing = []
    for uid in UNIQUE_IDS:
        pattern = rf"unique_id\s*:\s*{re.escape(uid)}\b"
        if not re.search(pattern, content):
            missing.append(uid)
    if missing:
        ERRORS.append(
            "T2 - unique_id absent du fichier canonique : "
            + ", ".join(missing)
        )
        return
    print("✔ T2 - Les deux unique_id sont presents dans le fichier canonique")


def test_unique_ids_uniqueness_in_template_sensors() -> None:
    """T3 - Chaque unique_id n'apparait qu'une fois dans 12_template_sensors/."""
    if not TEMPLATE_SENSORS_DIR.is_dir():
        ERRORS.append(
            f"T3 - Dossier introuvable : "
            f"{TEMPLATE_SENSORS_DIR.relative_to(ROOT)}"
        )
        return
    duplicates: dict[str, list[str]] = {uid: [] for uid in UNIQUE_IDS}
    for path in TEMPLATE_SENSORS_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SCANNED_EXTENSIONS:
            continue
        content = _read(path)
        for uid in UNIQUE_IDS:
            pattern = rf"unique_id\s*:\s*{re.escape(uid)}\b"
            if re.search(pattern, content):
                duplicates[uid].append(str(path.relative_to(ROOT)))
    failed = False
    for uid, files in duplicates.items():
        if len(files) != 1:
            ERRORS.append(
                f"T3 - unique_id '{uid}' attendu exactement 1 fois dans "
                f"12_template_sensors/, trouve {len(files)} fois : "
                f"{files if files else '[aucun]'}"
            )
            failed = True
    if not failed:
        print("✔ T3 - Unicite du point de definition des deux unique_id")


def test_contract_states_present_in_canonical_file() -> None:
    """T4 - Les trois etats contractuels sont presents dans le fichier canonique."""
    if not CANONICAL_FILE.is_file():
        ERRORS.append("T4 - Saute (T1 a echoue)")
        return
    content = _read(CANONICAL_FILE)
    # On cherche le token isole, pas un sous-token : muet_ping_ok ne doit pas
    # matcher muet_ping_ko et vice-versa. \b suffit car les caracteres alentour
    # sont des espaces ou des sauts de ligne dans le YAML.
    missing = []
    for state in CONTRACT_STATES:
        pattern = rf"(?<![A-Za-z0-9_]){re.escape(state)}(?![A-Za-z0-9_])"
        if not re.search(pattern, content):
            missing.append(state)
    if missing:
        ERRORS.append(
            "T4 - Etat contractuel absent du fichier canonique : "
            + ", ".join(missing)
        )
        return
    print("✔ T4 - Les trois etats contractuels sont presents "
          "(ok, muet_ping_ok, muet_ping_ko)")


def test_no_legacy_state_in_repo() -> None:
    """T5 - Aucune trace des anciens noms d'etats v1.0 dans le repo fonctionnel.

    Scope : tout le repo, en excluant :
      - 00_documentation_arsenal/ (le contrat lui-meme mentionne les anciens
        noms dans son historique §13),
      - le script de tests lui-meme (qui contient les chaines comme donnees).
    """
    if not ROOT.is_dir():
        ERRORS.append(f"T5 - Racine introuvable : {ROOT}")
        return
    this_script = Path(__file__).resolve()
    legacy_hits: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SCANNED_EXTENSIONS:
            continue
        try:
            if path.resolve().is_relative_to(DOCUMENTATION_DIR):
                continue
        except AttributeError:
            # Python < 3.9 fallback (rare en CI moderne, mais robuste).
            if str(path.resolve()).startswith(str(DOCUMENTATION_DIR)):
                continue
        if path.resolve() == this_script:
            continue
        content = _read(path)
        for legacy in LEGACY_STATES:
            pattern = rf"(?<![A-Za-z0-9_]){re.escape(legacy)}(?![A-Za-z0-9_])"
            for m in re.finditer(pattern, content):
                line_no = content.count("\n", 0, m.start()) + 1
                legacy_hits.append(
                    f"{path.relative_to(ROOT)}:{line_no} -> '{legacy}'"
                )
    if legacy_hits:
        ERRORS.append(
            "T5 - Anciens noms d'etats v1.0 detectes hors documentation "
            f"({len(legacy_hits)} occurrence(s)) :\n  "
            + "\n  ".join(legacy_hits)
        )
        return
    print("✔ T5 - Aucune trace des anciens noms d'etats (ko_homekit, ko_reseau) "
          "hors documentation")


def test_positive_selection_pattern() -> None:
    """T6 - Le pattern de selection positive §6 est present dans le fichier canonique.

    On verifie la coprésence des trois marqueurs structurels :
      - map('float', default=none)
      - reject('eq', none)
      - count > 0
    Deux occurrences attendues (une par capteur).
    """
    if not CANONICAL_FILE.is_file():
        ERRORS.append("T6 - Saute (T1 a echoue)")
        return
    content = _read(CANONICAL_FILE)
    # Patterns tolerants aux espaces.
    pat_map = re.compile(r"map\(\s*['\"]float['\"]\s*,\s*default\s*=\s*none\s*\)")
    pat_reject = re.compile(r"reject\(\s*['\"]eq['\"]\s*,\s*none\s*\)")
    pat_count = re.compile(r"valides\s*\|\s*count\s*>\s*0")
    n_map = len(pat_map.findall(content))
    n_reject = len(pat_reject.findall(content))
    n_count = len(pat_count.findall(content))
    if n_map < 2 or n_reject < 2 or n_count < 2:
        ERRORS.append(
            "T6 - Selection positive §6 incomplete dans le fichier canonique : "
            f"map('float', default=none)={n_map}, "
            f"reject('eq', none)={n_reject}, "
            f"valides | count > 0={n_count} "
            f"(2 occurrences attendues pour chaque, une par capteur)"
        )
        return
    print("✔ T6 - Selection positive §6 conforme "
          "(float+default=none, reject eq none, count > 0)")


def test_no_negative_selection_antipatterns() -> None:
    """T7 - Aucun anti-pattern §6 dans le fichier canonique.

    Anti-patterns interdits :
      - reject('equalto', 'unavailable')   (exclusion partielle)
      - 'unavailable' not in preuves
      - 'unknown' not in preuves
    """
    if not CANONICAL_FILE.is_file():
        ERRORS.append("T7 - Saute (T1 a echoue)")
        return
    content = _read(CANONICAL_FILE)
    bad_patterns = {
        "reject('equalto', 'unavailable')": re.compile(
            r"reject\(\s*['\"]equalto['\"]\s*,\s*['\"]unavailable['\"]\s*\)"
        ),
        "'unavailable' not in preuves": re.compile(
            r"['\"]unavailable['\"]\s+not\s+in\s+preuves"
        ),
        "'unknown' not in preuves": re.compile(
            r"['\"]unknown['\"]\s+not\s+in\s+preuves"
        ),
    }
    hits = []
    for label, pat in bad_patterns.items():
        if pat.search(content):
            hits.append(label)
    if hits:
        ERRORS.append(
            "T7 - Anti-pattern §6 detecte dans le fichier canonique : "
            + "; ".join(hits)
        )
        return
    print("✔ T7 - Aucun anti-pattern de selection negative (§6)")


def _extract_preuves_blocks(content: str) -> list[str]:
    """Extrait le contenu (entre crochets) de chaque `set preuves = [ ... ]`.

    Retourne la liste des blocs internes, sans les crochets.
    """
    blocks: list[str] = []
    pattern = re.compile(r"set\s+preuves\s*=\s*\[", re.IGNORECASE)
    for m in pattern.finditer(content):
        start = m.end()  # juste apres le [
        depth = 1
        i = start
        while i < len(content) and depth > 0:
            c = content[i]
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    blocks.append(content[start:i])
                    break
            i += 1
    return blocks


def test_preuves_only_sensors() -> None:
    """T8 - Les listes 'preuves' ne contiennent que des entites 'sensor.'.

    Contrainte §7 : interdiction de binary_sensor, input_boolean, et plus
    largement de tout actionneur (switch, light, cover) dans les preuves
    de vie. Le ping (binary_sensor.station_meteo_netatmo_*) est legitime
    en branche `elif`, hors bloc preuves : ce test ne le touche pas.
    """
    if not CANONICAL_FILE.is_file():
        ERRORS.append("T8 - Saute (T1 a echoue)")
        return
    content = _read(CANONICAL_FILE)
    blocks = _extract_preuves_blocks(content)
    if len(blocks) < 2:
        ERRORS.append(
            f"T8 - Bloc(s) 'set preuves = [...]' introuvable(s) : "
            f"trouve {len(blocks)}, 2 attendus"
        )
        return
    # Pattern : on capture toute reference du type states('<domaine>.xxx')
    # et on verifie que le domaine est 'sensor'.
    forbidden_domains = (
        "binary_sensor",
        "input_boolean",
        "switch",
        "light",
        "cover",
        "input_select",
        "input_text",
    )
    violations: list[str] = []
    entity_ref = re.compile(
        r"states\(\s*['\"]([a-z_]+)\.([a-zA-Z0-9_]+)['\"]\s*\)"
    )
    for idx, block in enumerate(blocks, start=1):
        for m in entity_ref.finditer(block):
            domain, name = m.group(1), m.group(2)
            if domain != "sensor":
                violations.append(
                    f"bloc preuves #{idx} : {domain}.{name} "
                    f"(domaine interdit, §7)"
                )
            if domain in forbidden_domains:
                # Garde-fou explicite pour la lisibilite des messages.
                pass
    if violations:
        ERRORS.append(
            "T8 - Entites non-sensor detectees dans les listes preuves "
            f"(§7) : {'; '.join(violations)}"
        )
        return
    print(f"✔ T8 - Les {len(blocks)} listes 'preuves' ne contiennent "
          "que des entites 'sensor.'")


def test_ping_in_elif_branch() -> None:
    """T9 - Le ping intervient en branche elif, apres le test sur les preuves.

    Test structurel minimal §8 : on verifie que dans chaque bloc state,
    on observe la sequence :
        if valides | count > 0
        ...
        elif is_state('binary_sensor.station_meteo_netatmo_<N>', 'on')
    sans `and` qui combinerait preuves et ping dans une meme condition.

    Ce test n'est pas un parseur Jinja. Il verifie une forme observable
    minimale, conformement au §8 du contrat.
    """
    if not CANONICAL_FILE.is_file():
        ERRORS.append("T9 - Saute (T1 a echoue)")
        return
    content = _read(CANONICAL_FILE)

    # Sequence attendue (DOTALL pour traverser les sauts de ligne).
    seq_pattern = re.compile(
        r"if\s+valides\s*\|\s*count\s*>\s*0"
        r".*?"
        r"elif\s+is_state\(\s*['\"]binary_sensor\.station_meteo_netatmo_\d+['\"]\s*,\s*['\"]on['\"]\s*\)",
        re.DOTALL,
    )
    matches = seq_pattern.findall(content)
    if len(matches) < 2:
        ERRORS.append(
            f"T9 - Sequence §8 (if valides... elif is_state(ping...)) "
            f"trouvee {len(matches)} fois, 2 attendues "
            f"(une par capteur)"
        )
        return

    # Garde-fou anti-combinaison : aucune occurrence de
    # `is_state('binary_sensor.station_meteo_netatmo_...` ne doit etre
    # combinee a `valides | count` via un `and` dans la meme expression
    # ouverte par `{% if ... %}`.
    combined_pattern = re.compile(
        r"\{%\s*if\s+[^%]*valides[^%]*\band\b[^%]*is_state\(\s*['\"]binary_sensor\.station_meteo_netatmo",
        re.DOTALL,
    )
    if combined_pattern.search(content):
        ERRORS.append(
            "T9 - Combinaison interdite §8 detectee : `valides ... and "
            "is_state(binary_sensor.station_meteo_netatmo...)` dans un "
            "meme `if`"
        )
        return
    print("✔ T9 - Ordre logique §8 : ping en branche elif, "
          "non combine avec les preuves")


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
TESTS = (
    test_canonical_file_exists,
    test_unique_ids_present_in_canonical_file,
    test_unique_ids_uniqueness_in_template_sensors,
    test_contract_states_present_in_canonical_file,
    test_no_legacy_state_in_repo,
    test_positive_selection_pattern,
    test_no_negative_selection_antipatterns,
    test_preuves_only_sensors,
    test_ping_in_elif_branch,
)


def main() -> int:
    print("Arsenal — Validation contractuelle : Diagnostic Netatmo (v1.1)")
    print(f"ROOT = {ROOT}")
    print()
    for test in TESTS:
        test()
    print()
    if ERRORS:
        print("❌ CONTRAT DIAGNOSTIC_NETATMO NON CONFORME")
        for err in ERRORS:
            print(f"  - {err}")
        return 1
    print("✅ CONTRAT DIAGNOSTIC_NETATMO CONFORME")
    return 0


if __name__ == "__main__":
    sys.exit(main())