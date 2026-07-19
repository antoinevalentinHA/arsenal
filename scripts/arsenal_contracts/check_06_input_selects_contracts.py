#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Structure 06_input_selects — ISS.

Contrat (source normative de forme) :
  00_documentation_arsenal/architecture/00_structure_includes/06_input_selects.md
  (§ Structure : « <nom_helper>: { name, icon, options: [...] } » ; § Include :
   « input_select: !include_dir_merge_named 06_input_selects/ »).

Périmètre contrôlé :
  06_input_selects/**/*.yaml (tous les helpers input_select) + la présence de
  l'include dans configuration.yaml.

Motivation (C14 — couverture CI de la norme, §6 ligne P1 « CI structure
06_input_selects ») : la brique 06_input_selects n'avait AUCUN checker de
structure. `check_prefix_id_contracts.py` (PID) ne contrôle QUE l'intégrité du
helper `prefix_id_select` (source de vérité des identités) et a explicitement
différé « la validation structurelle générique des AUTRES input_select […]
patron name/options ». Ce checker ferme ce trou, sur le patron des 9 checkers
de structure existants (01, 02, 03, 04, 05, 07, 08, 09, 19).

Nature de la vérification : STRUCTURELLE (parsing YAML réel), pas lexicale.
Proportionnalité (D-NE-8) : seuls des invariants UNIVERSELS et falsifiables du
patron sont contrôlés (name/options load-bearing, intégrité `entity_id`,
`initial` cohérent). Les interdits doctrinaux sémantiques (« pas de logique
métier », « pas de décision ») sont de la prose non falsifiable — hors
périmètre, volontairement.

Règles (toutes ERROR ; logique Arsenal : ERROR => exit 1) :
  ISS-000  Fichier illisible / YAML invalide, ou racine non-mapping ou vide.
  ISS-001  Définition de helper non-mapping (`<clé>:` ne porte pas un mapping).
  ISS-002  `options` absente / non-liste / vide, ou option non-scalaire / vide.
  ISS-003  Option dupliquée au sein d'un même helper.
  ISS-004  `initial` présent mais absent de `options` (HA rejette / avertit).
  ISS-005  Clé de helper hors slug `object_id` `^[a-z][a-z0-9_]*$`.
  ISS-006  `name` absent ou vide (patron « name/options » de la doctrine).
  ISS-007  Include `!include_dir_merge_named 06_input_selects/` absent de
           configuration.yaml (§ Include).

Aucun faux positif connu sur le corpus aligné : exit 0 attendu sur main.
Régression du checker lui-même (`--selftest`) => exit 2.

Usage :
  python scripts/arsenal_contracts/check_06_input_selects_contracts.py
  python scripts/arsenal_contracts/check_06_input_selects_contracts.py --selftest
  Options (tests uniquement — les défauts sont les chemins du dépôt) :
    --dir DIR --config FILE
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIR = ROOT / "06_input_selects"
DEFAULT_CONFIG = ROOT / "configuration.yaml"

# Slug object_id Home Assistant (minuscules, chiffres, underscore ; commence
# par une lettre). Garde l'intégrité de l'entity_id input_select.<clé>.
SLUG_RE = re.compile(r"^[a-z][a-z0-9_]*$")
# Include déclaré par la doctrine (§ Include).
INCLUDE_RE = re.compile(r"!include_dir_merge_named\s+06_input_selects/?")


# ---------------------------------------------------------------------------
# Chargement YAML tolérant aux tags HA (!secret, !include, ...) — cohérent
# avec les checkers de structure et PID/AID/APD.
# ---------------------------------------------------------------------------
class _Loader(yaml.SafeLoader):
    pass


_Loader.add_multi_constructor("!", lambda loader, suffix, node: None)


def load_yaml(path: Path):
    return yaml.load(path.read_text(encoding="utf-8", errors="ignore"), Loader=_Loader)


# ---------------------------------------------------------------------------
# Cœur de validation — pur (données déjà parsées -> liste d'erreurs).
# Séparé du I/O pour être exerçable en --selftest sans écrire de fichier.
# ---------------------------------------------------------------------------
def _is_scalar(value) -> bool:
    """Une option valide est un scalaire non vide (str/int/float/bool)."""
    return isinstance(value, (str, int, float)) and str(value).strip() != ""


def validate_helper(key: str, helper, where: str = "") -> list[str]:
    """Valide un helper input_select (ISS-001..006). `helper` est la valeur du
    mapping racine associée à `key`."""
    loc = f"{where} : " if where else ""
    errors: list[str] = []

    if not isinstance(helper, dict):
        return [
            f"ISS-001 — {loc}helper « {key} » n'est pas un mapping "
            f"(trouvé {type(helper).__name__})."
        ]

    # ISS-002 — options
    options = helper.get("options")
    options_ok = isinstance(options, list) and len(options) > 0
    if not options_ok:
        errors.append(
            f"ISS-002 — {loc}helper « {key} » : `options` absente, non-liste "
            f"ou vide (trouvé {type(options).__name__})."
        )
    else:
        bad = [o for o in options if not _is_scalar(o)]
        if bad:
            errors.append(
                f"ISS-002 — {loc}helper « {key} » : option(s) non-scalaire(s) "
                f"ou vide(s) : {bad!r}."
            )
        # ISS-003 — doublon d'option (comparaison sur forme stringifiée)
        keys = [str(o) for o in options if _is_scalar(o)]
        for opt, n in sorted(Counter(keys).items()):
            if n > 1:
                errors.append(
                    f"ISS-003 — {loc}helper « {key} » : option dupliquée "
                    f"« {opt} » ({n} occurrences)."
                )

    # ISS-004 — initial ∈ options (si présent)
    if "initial" in helper and helper["initial"] is not None and options_ok:
        valid = {str(o) for o in options if _is_scalar(o)}
        if str(helper["initial"]) not in valid:
            errors.append(
                f"ISS-004 — {loc}helper « {key} » : `initial` "
                f"« {helper['initial']} » absent de `options`."
            )

    # ISS-005 — clé = slug object_id
    if not SLUG_RE.match(str(key)):
        errors.append(
            f"ISS-005 — {loc}clé de helper « {key} » hors slug object_id "
            f"(attendu ^[a-z][a-z0-9_]*$)."
        )

    # ISS-006 — name présent et non vide (patron « name/options »)
    name = helper.get("name")
    if name is None or str(name).strip() == "":
        errors.append(
            f"ISS-006 — {loc}helper « {key} » : `name` absent ou vide "
            "(patron name/options de la doctrine)."
        )

    return errors


def validate_file_data(where: str, data) -> list[str]:
    """Valide le contenu parsé d'un fichier 06_input_selects (ISS-000 racine +
    ISS-001..006 par helper)."""
    if not isinstance(data, dict) or not data:
        return [
            f"ISS-000 — {where} : racine non-mapping ou vide "
            f"(trouvé {type(data).__name__})."
        ]
    errors: list[str] = []
    for key, helper in data.items():
        errors += validate_helper(str(key), helper, where)
    return errors


def check_include(config_text: str) -> list[str]:
    """ISS-007 — include déclaré dans configuration.yaml."""
    if not INCLUDE_RE.search(config_text or ""):
        return [
            "ISS-007 — include `!include_dir_merge_named 06_input_selects/` "
            "absent de configuration.yaml (§ Include)."
        ]
    return []


# ---------------------------------------------------------------------------
# Scan du dépôt (I/O).
# ---------------------------------------------------------------------------
def scan(directory: Path, config_file: Path) -> list[str]:
    errors: list[str] = []

    if not directory.is_dir():
        return [f"ISS-000 — dossier introuvable : {directory}"]

    files = sorted(p for p in directory.rglob("*.yaml") if p.is_file())
    if not files:
        errors.append(f"ISS-000 — aucun fichier .yaml dans {directory}.")

    for path in files:
        rel = path.relative_to(ROOT) if ROOT in path.parents else path
        try:
            data = load_yaml(path)
        except yaml.YAMLError as exc:
            errors.append(f"ISS-000 — {rel} : YAML illisible ({exc}).")
            continue
        errors += validate_file_data(str(rel), data)

    config_text = config_file.read_text(encoding="utf-8", errors="ignore") \
        if config_file.is_file() else ""
    errors += check_include(config_text)

    return errors


# ---------------------------------------------------------------------------
# Auto-test du juge (on ne juge pas avec un juge défectueux). En mémoire.
# ---------------------------------------------------------------------------
def _selftest() -> int:
    failures: list[str] = []

    def expect(cond: bool, label: str) -> None:
        if not cond:
            failures.append(label)

    def codes(errs: list[str]) -> set[str]:
        return {e.split(" ", 1)[0] for e in errs}

    # Corpus conforme -> 0 erreur (name+options, icon optionnel, initial ∈ opts)
    ok = {
        "mode_x": {"name": "Mode X", "icon": "mdi:x", "options": ["a", "b"]},
        "mode_y": {"name": "Mode Y", "options": ["a", "b"], "initial": "b"},
    }
    expect(validate_file_data("ok.yaml", ok) == [], "conforme-0-erreur")

    # ISS-000 : racine None / non-mapping / vide
    expect("ISS-000" in codes(validate_file_data("f", None)), "iss000-none")
    expect("ISS-000" in codes(validate_file_data("f", "x")), "iss000-non-map")
    expect("ISS-000" in codes(validate_file_data("f", {})), "iss000-vide")

    # ISS-001 : helper non-mapping
    expect("ISS-001" in codes(validate_file_data("f", {"k": ["a"]})), "iss001")

    # ISS-002 : options absente / non-liste / vide / non-scalaire / vide
    expect("ISS-002" in codes(validate_helper("k", {"name": "n"})), "iss002-absente")
    expect("ISS-002" in codes(validate_helper("k", {"name": "n", "options": "a"})), "iss002-str")
    expect("ISS-002" in codes(validate_helper("k", {"name": "n", "options": []})), "iss002-vide")
    expect("ISS-002" in codes(validate_helper("k", {"name": "n", "options": [{"x": 1}]})), "iss002-nonscalaire")
    expect("ISS-002" in codes(validate_helper("k", {"name": "n", "options": ["a", "  "]})), "iss002-scalaire-vide")

    # ISS-003 : option dupliquée
    expect("ISS-003" in codes(validate_helper("k", {"name": "n", "options": ["a", "a"]})), "iss003")

    # ISS-004 : initial ∉ options
    expect("ISS-004" in codes(validate_helper("k", {"name": "n", "options": ["a"], "initial": "z"})), "iss004")

    # ISS-005 : clé hors slug
    expect("ISS-005" in codes(validate_helper("Mode X", {"name": "n", "options": ["a"]})), "iss005-espace-maj")
    expect("ISS-005" in codes(validate_helper("1mode", {"name": "n", "options": ["a"]})), "iss005-chiffre-tete")

    # ISS-006 : name absent / vide
    expect("ISS-006" in codes(validate_helper("k", {"options": ["a"]})), "iss006-absent")
    expect("ISS-006" in codes(validate_helper("k", {"name": "   ", "options": ["a"]})), "iss006-vide")

    # ISS-007 : include
    expect(check_include("input_select: !include_dir_merge_named 06_input_selects/") == [], "iss007-present")
    expect("ISS-007" in codes(check_include("")), "iss007-absent")

    # Faux positifs à éviter :
    #  - options numériques (YAML parse en int/float) -> conforme
    expect(validate_helper("k", {"name": "n", "options": [1, 2, 3]}) == [], "fp-options-num")
    #  - initial numérique matchant une option numérique -> conforme
    expect(validate_helper("k", {"name": "n", "options": [0, 1], "initial": 0}) == [], "fp-initial-num")
    #  - clé snake_case avec chiffres -> conforme
    expect(validate_helper("bot_tx_2", {"name": "n", "options": ["a"]}) == [], "fp-snake-chiffres")
    #  - icon absent -> conforme (icon non requis)
    expect(validate_helper("k", {"name": "n", "options": ["a"]}) == [], "fp-sans-icon")

    if failures:
        print("❌ AUTO-TESTS CHECKER 06_INPUT_SELECTS EN ÉCHEC")
        for f in failures:
            print(f"  • {f}")
        return 2
    print("✅ AUTO-TESTS CHECKER 06_INPUT_SELECTS OK")
    return 0


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    if args.selftest:
        return _selftest()

    print("Arsenal — Validation contractuelle : Structure 06_input_selects (ISS)\n")

    errors = scan(args.dir, args.config)

    print(f"Périmètre : {args.dir}")
    print(f"Synthèse : {len(errors)} ERROR.")

    if errors:
        print("\n❌ STRUCTURE 06_INPUT_SELECTS NON CONFORME\n")
        for err in errors:
            print(f"  • {err}")
        return 1

    print("\n✅ STRUCTURE 06_INPUT_SELECTS CONFORME")
    return 0


if __name__ == "__main__":
    sys.exit(main())
