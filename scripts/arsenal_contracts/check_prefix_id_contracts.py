#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : intégrité de la source de vérité des
préfixes d'ID (helper prefix_id_select) — PID.

Contrat (NORMATIF, opposable) — règles de création de domaine / préfixe :
  00_documentation_arsenal/architecture/03_doctrines/id_automatisations.md
  (§ « Création d'un nouveau domaine fonctionnel » : préfixe numérique unique
   à 4 chiffres, option « NNNN - domaine »).
Structure du helper (source normative de forme) :
  00_documentation_arsenal/architecture/00_structure_includes/06_input_selects.md

Source de vérité contrôlée :
  06_input_selects/system/prefix_id.yaml (input_select.prefix_id_select)

Motivation (C14 — couverture CI de la norme, dette « source de vérité jamais
contrôlée pour elle-même ») : le fichier prefix_id.yaml EST la source de
vérité des identités d'automatisations. Il est CONSOMMÉ par AID
(check_automation_ids_contracts.py) et APD
(check_automation_prefix_domain_contracts.py), mais n'était jamais contrôlé
pour lui-même. Or ces deux consommateurs parsent les options avec une regex
TOLÉRANTE (`\\s*(\\d{4})\\s*-\\s*(.+?)\\s*$`) et ABANDONNENT SILENCIEUSEMENT
toute option malformée : une option corrompue dégrade AID-004/APD-001 sans le
moindre signal. Ce checker ferme ce trou en amont.

Nature de la vérification : STRUCTURELLE (parsing YAML réel), pas lexicale.

Périmètre (borné — proportionnalité D-NE-8) : uniquement l'intégrité du helper
`prefix_id_select` de prefix_id.yaml. La validation structurelle générique des
AUTRES input_select de 06_input_selects/ (patron name/options) est une
extension ultérieure distincte, volontairement hors périmètre ici pour éviter
les faux positifs sur une famille hétérogène.

Règles :
  PID-000  Fichier illisible, `prefix_id_select` absent, ou `options`
           absente / non-liste / vide (ERROR).
  PID-001  Option non conforme au format canonique « NNNN - domaine »
           (préfixe = exactement 4 chiffres, séparateur « ` - ` » à espace
           unique, domaine non vide) — c'est précisément l'option qu'AID/APD
           abandonnent en silence (ERROR).
  PID-002  Nom de domaine non canonique : doit être un identifiant
           `^[a-z][a-z0-9_]*$` (minuscules, chiffres, underscore). Garde la
           comparaison préfixe→domaine↔dossier racine d'APD (dossiers en
           minuscules) — proxy déclaré (ERROR).
  PID-003  Préfixe dupliqué : deux options partagent le même préfixe 4 chiffres
           → le mapping préfixe→domaine consommé par AID/APD est écrasé
           silencieusement (ERROR).
  PID-004  Domaine dupliqué : deux options nomment le même domaine → identité
           ambiguë (deux préfixes pour un domaine) (ERROR).

Aucun faux positif connu sur le corpus aligné : exit 0 attendu sur main.
Logique Arsenal habituelle : ERROR => exit 1 ; régression du checker
lui-même (`--selftest`) => exit 2.

Usage :
  python scripts/arsenal_contracts/check_prefix_id_contracts.py
  python scripts/arsenal_contracts/check_prefix_id_contracts.py --selftest
  Option (tests uniquement — le défaut est le chemin du dépôt) :
    --prefix-file FILE
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PREFIX_FILE = ROOT / "06_input_selects" / "system" / "prefix_id.yaml"

HELPER_KEY = "prefix_id_select"

# Format canonique d'une option : « NNNN - domaine » (espace unique de part et
# d'autre du tiret ; préfixe = exactement 4 chiffres ; domaine non vide).
CANONICAL_OPTION_RE = re.compile(r"^(\d{4}) - (.+)$")
# Identifiant de domaine canonique (comparé aux dossiers racine par APD).
DOMAIN_RE = re.compile(r"^[a-z][a-z0-9_]*$")


# ---------------------------------------------------------------------------
# Chargement YAML tolérant aux tags HA (!secret, !include, ...) — cohérent
# avec les consommateurs AID/APD.
# ---------------------------------------------------------------------------
class _Loader(yaml.SafeLoader):
    pass


_Loader.add_multi_constructor("!", lambda loader, suffix, node: None)


def load_yaml(path: Path):
    return yaml.load(path.read_text(encoding="utf-8", errors="ignore"), Loader=_Loader)


# ---------------------------------------------------------------------------
# Cœur de validation — pur (str brut du fichier -> liste d'erreurs).
# Séparé du I/O pour être exerçable en --selftest sans écrire de fichier.
# ---------------------------------------------------------------------------
def validate_options(options) -> list[str]:
    """Valide la liste d'options du helper. `options` est ce que le YAML a
    produit (liste attendue). Retourne la liste des ERROR (PID-001..004)."""
    errors: list[str] = []

    if not isinstance(options, list) or not options:
        errors.append(
            "PID-000 — `prefix_id_select.options` absente, non-liste ou vide "
            f"(trouvé {type(options).__name__})."
        )
        return errors

    valid_prefixes: list[str] = []
    valid_domains: list[str] = []

    for opt in options:
        text = str(opt)
        m = CANONICAL_OPTION_RE.match(text)
        if not m:
            errors.append(
                f"PID-001 — option non conforme au format « NNNN - domaine » : "
                f"« {text} » (abandonnée en silence par AID/APD)."
            )
            continue
        prefix, domain = m.group(1), m.group(2)
        if not DOMAIN_RE.match(domain):
            errors.append(
                f"PID-002 — nom de domaine non canonique « {domain} » "
                f"(attendu ^[a-z][a-z0-9_]*$) dans l'option « {text} »."
            )
            # Préfixe tout de même retenu pour la détection de doublon : une
            # collision de préfixe reste une collision.
            valid_prefixes.append(prefix)
            continue
        valid_prefixes.append(prefix)
        valid_domains.append(domain)

    for prefix, n in sorted(Counter(valid_prefixes).items()):
        if n > 1:
            errors.append(
                f"PID-003 — préfixe dupliqué « {prefix} » ({n} occurrences) : "
                f"le mapping préfixe→domaine consommé par AID/APD est ambigu."
            )
    for domain, n in sorted(Counter(valid_domains).items()):
        if n > 1:
            errors.append(
                f"PID-004 — domaine dupliqué « {domain} » ({n} occurrences) : "
                f"identité ambiguë (plusieurs préfixes pour un même domaine)."
            )

    return errors


def check_file(prefix_file: Path) -> list[str]:
    if not prefix_file.is_file():
        return [f"PID-000 — fichier introuvable : {prefix_file}"]
    try:
        data = load_yaml(prefix_file)
    except yaml.YAMLError as exc:
        return [f"PID-000 — YAML illisible : {prefix_file} ({exc})"]

    if not isinstance(data, dict) or HELPER_KEY not in data:
        return [
            f"PID-000 — helper « {HELPER_KEY} » absent de {prefix_file.name} "
            "(structure racine invalide)."
        ]
    helper = data.get(HELPER_KEY)
    if not isinstance(helper, dict):
        return [
            f"PID-000 — « {HELPER_KEY} » n'est pas un mapping "
            f"(trouvé {type(helper).__name__})."
        ]
    return validate_options(helper.get("options"))


# ---------------------------------------------------------------------------
# Auto-test du juge (on ne juge pas avec un juge défectueux). Synthétique, en
# mémoire, n'écrit aucun fichier. Échec => exit 2.
# ---------------------------------------------------------------------------
def _selftest() -> int:
    failures: list[str] = []

    def expect(cond: bool, label: str) -> None:
        if not cond:
            failures.append(label)

    def codes(errs: list[str]) -> set[str]:
        return {e.split(" ", 1)[0] for e in errs}

    # Corpus conforme -> 0 erreur
    ok = ["1001 - aeration", "1002 - alarme", "1005 - cumulus_studio"]
    expect(validate_options(ok) == [], "conforme-0-erreur")

    # PID-000 : options absente / vide / non-liste
    expect("PID-000" in codes(validate_options(None)), "pid000-none")
    expect("PID-000" in codes(validate_options([])), "pid000-vide")
    expect("PID-000" in codes(validate_options("x")), "pid000-non-liste")

    # PID-001 : préfixe pas 4 chiffres, séparateur absent, domaine vide,
    # espacement non canonique
    expect("PID-001" in codes(validate_options(["999 - x"])), "pid001-3-chiffres")
    expect("PID-001" in codes(validate_options(["10012 - x"])), "pid001-5-chiffres")
    expect("PID-001" in codes(validate_options(["1001 aeration"])), "pid001-sans-sep")
    expect("PID-001" in codes(validate_options(["1001 - "])), "pid001-domaine-vide")
    expect("PID-001" in codes(validate_options(["1001  - x"])), "pid001-double-espace")

    # PID-002 : domaine non canonique (majuscule, espace)
    expect("PID-002" in codes(validate_options(["1001 - Aeration"])), "pid002-majuscule")
    expect("PID-002" in codes(validate_options(["1001 - aer ation"])), "pid002-espace")

    # PID-003 : préfixe dupliqué (y compris si l'un a un domaine non canonique)
    expect("PID-003" in codes(validate_options(["1001 - a", "1001 - b"])), "pid003-prefixe")
    expect("PID-003" in codes(validate_options(["1001 - a", "1001 - B"])), "pid003-prefixe-mixte")

    # PID-004 : domaine dupliqué
    expect("PID-004" in codes(validate_options(["1001 - x", "1002 - x"])), "pid004-domaine")

    # Faux positif à éviter : domaine snake_case avec chiffres -> conforme
    expect(validate_options(["1018 - imprimerie", "1005 - cumulus_studio"]) == [],
           "fp-snake-case-chiffres")

    if failures:
        print("❌ AUTO-TESTS CHECKER PRÉFIXE ID EN ÉCHEC")
        for f in failures:
            print(f"  • {f}")
        return 2
    print("✅ AUTO-TESTS CHECKER PRÉFIXE ID OK")
    return 0


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefix-file", type=Path, default=DEFAULT_PREFIX_FILE)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    if args.selftest:
        return _selftest()

    print("Arsenal — Contrat intégrité prefix_id_select (PID) — source de vérité des identités\n")

    errors = check_file(args.prefix_file)

    print(f"Périmètre : {args.prefix_file}")
    print(f"Synthèse : {len(errors)} ERROR.")

    if errors:
        print("\n❌ SOURCE DE VÉRITÉ DES PRÉFIXES NON CONFORME\n")
        for err in errors:
            print(f"  • {err}")
        return 1

    print("\n✅ SOURCE DE VÉRITÉ DES PRÉFIXES CONFORME")
    return 0


if __name__ == "__main__":
    sys.exit(main())
