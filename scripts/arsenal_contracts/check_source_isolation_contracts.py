#!/usr/bin/env python3
"""
Arsenal — Séparation des périmètres : sources extérieures hors domicile

Sources normatives :
  - 00_documentation_arsenal/architecture/03_doctrines/principes_generaux.md
    §10 « Autorisation de source par périmètre »
  - 00_documentation_arsenal/audits/01_rapports/architecture/
    audit_frontiere_maison_imprimerie_sources_exterieures.md
  - 00_documentation_arsenal/contrats/arrosage/16_canal_demande_climatique.md
    (§1, note « Périmètre des entrées — opposable »)
Script :
  scripts/arsenal_contracts/check_source_isolation_contracts.py

Règle défendue (principe 10)
----------------------------
Une décision Maison ne doit pas consommer directement une source appartenant
au périmètre extérieur du site Imprimerie (source extérieure hors domicile),
même si cette source est valide dans son propre périmètre. Une source canonique
dans un périmètre A n'est pas automatiquement autorisée dans un périmètre B :
une décision Maison portant sur l'extérieur local consomme l'interface
canonique du domicile (axe `_jardin`).

Ce que le checker CONTRÔLE
--------------------------
Il échoue si l'un des `entity_id` de la deny-list exacte ci-dessous est
référencé dans un fichier d'un domaine de décision Maison (périmètre de scan
strict, cf. MAISON_DOMAINS × SCAN_BASES).

Contrainte de correction (faux positif interdit)
------------------------------------------------
Le matching est fait par **frontière de token exacte** (lookarounds), jamais
par sous-chaîne ni motif large « *exterieur* ». C'est indispensable :
`sensor.temperature_exterieur` est un **préfixe** de
`sensor.temperature_exterieure_moyenne_jour`, entité au nom trompeur mais dont
la **source est le jardin** (`13_sensor_platforms/statistics/meteo/
temperature_jardin.yaml`, `entity_id: sensor.temperature_jardin`). Un contrôle
par sous-chaîne la bloquerait à tort et casserait l'ET₀ de l'arrosage.

Les lignes purement commentées (`#` en tête après indentation) sont ignorées :
une mention documentaire n'est pas une consommation.

Ce que le checker NE garantit PAS
---------------------------------
- Il ne distingue pas une référence en `state:` (décision) d'une en
  `attributes:` (affichage) : dans un fichier de décision Maison, toute
  référence à une source hors périmètre est traitée comme interdite
  (conservateur, cf. limites de l'audit §5).
- Il ne couvre pas un futur périmètre tiers mal nommé : la deny-list est une
  liste exacte, pas un invariant sémantique.

Logique Arsenal habituelle : ERROR => exit 1.

Usage :
  python scripts/arsenal_contracts/check_source_isolation_contracts.py
  python scripts/arsenal_contracts/check_source_isolation_contracts.py --selftest
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Périmètre de scan — domaines de décision Maison uniquement
#
# Domaines confirmés présents dans le dépôt (existence vérifiée au runtime ;
# une combinaison base × domaine absente est simplement ignorée).
# Le périmètre EXCLUT volontairement : la documentation et les audits, le
# recorder, les groupes/intégrations, les dashboards Imprimerie, les fichiers
# météo qui définissent légitimement les sources du site Imprimerie, les
# statistiques/dérivés, et le domaine `imprimerie/` (périmètre professionnel
# distant).
# ---------------------------------------------------------------------------
MAISON_DOMAINS = [
    "arrosage",
    "chauffage",
    "climatisation",
    "aeration",
    "deshumidificateur",
    "vmc",
    "ecs",
    "volets",
]

SCAN_BASES = [
    "12_template_sensors",  # perception / décision Maison
    "11_automations",       # actions Maison
    "10_scripts",           # scripts Maison
]

# ---------------------------------------------------------------------------
# Deny-list EXACTE — sources du périmètre extérieur du site Imprimerie
# (source extérieure hors domicile). Aucun motif large.
#
# Provenance vérifiée dans le dépôt (HEAD au moment de la rédaction) :
#   - sources cœur : axe `_exterieur` (mesures + dérivés physiques),
#     agrégats bruts `_1` / `_2` ;
#   - filtrés par période : dérivés des sources cœur `_exterieur`
#     (ex. `temperature_filtre_aube_exterieur` <- `sensor.temperature_exterieur`) ;
#   - seuils dynamiques : cadre de confort de l'extérieur Imprimerie.
#
# Exclusions assumées (NON dans la deny-list) :
#   - `sensor.couleur_*_exterieur` : entités d'affichage (UI), pas des sources
#     de mesure consommables par une décision ;
#   - entités de diagnostic RF des modules extérieurs : diagnostic, et surtout
#     libellées avec des noms d'équipement — non reprises ici (confidentialité).
# ---------------------------------------------------------------------------

# Sources cœur (les 9 de la deny-list initiale)
_DENY_CORE = [
    "sensor.temperature_exterieur",
    "sensor.temperature_exterieur_1",
    "sensor.temperature_exterieur_2",
    "sensor.humidite_relative_exterieur",
    "sensor.humidite_relative_exterieur_1",
    "sensor.humidite_relative_exterieur_2",
    "sensor.humidex_exterieur",
    "sensor.point_de_rosee_exterieur",
    "sensor.humidite_absolue_exterieur",
]

# Dérivés filtrés par période (Imprimerie), 3 grandeurs × 5 périodes solaires
_PERIODES = ["aube", "matin", "jour", "crepuscule", "nuit"]
_DENY_FILTRES = [
    f"sensor.{grandeur}_filtre_{p}_exterieur"
    for grandeur in ("temperature", "humidite_relative", "humidite_absolue")
    for p in _PERIODES
]

# Seuils dynamiques (Imprimerie), 3 grandeurs × 2 bornes
_DENY_SEUILS = [
    f"sensor.{grandeur}_seuil_{borne}_exterieur"
    for grandeur in ("temperature", "humidite_relative", "humidite_absolue")
    for borne in ("bas", "haut")
]

DENY_LIST = _DENY_CORE + _DENY_FILTRES + _DENY_SEUILS

# ---------------------------------------------------------------------------
# Exceptions explicites (fichiers scannés mais tolérant une référence donnée).
# Aucune exception nécessaire à ce jour : le périmètre de scan est déjà propre
# post-#298. Toute exception future s'inscrit ici, sous la forme
# {chemin_relatif: {entity_id, ...}}, avec justification en commentaire.
# ---------------------------------------------------------------------------
EXCEPTIONS: dict[str, set[str]] = {}

# ---------------------------------------------------------------------------
# Compilation — matching par frontière de token exacte.
# `(?<![A-Za-z0-9_.])` en tête et `(?![A-Za-z0-9_])` en fin garantissent que
# `sensor.temperature_exterieur` ne matche PAS `sensor.temperature_exterieure_
# moyenne_jour` (source jardin) ni `sensor.temperature_exterieur_1`.
# ---------------------------------------------------------------------------
_DENY_PATTERNS = {
    ent: re.compile(r"(?<![A-Za-z0-9_.])" + re.escape(ent) + r"(?![A-Za-z0-9_])")
    for ent in DENY_LIST
}

_COMMENT_LINE = re.compile(r"^\s*#")

ERRORS: list[str] = []


def scanned_files() -> list[Path]:
    """Fichiers YAML des domaines Maison réellement présents dans le dépôt."""
    files: list[Path] = []
    for base in SCAN_BASES:
        for domain in MAISON_DOMAINS:
            d = REPO_ROOT / base / domain
            if d.is_dir():
                files.extend(sorted(p for p in d.rglob("*.yaml") if p.is_file()))
    return files


def scan_line(rel: str, lineno: int, line: str) -> None:
    if _COMMENT_LINE.match(line):
        return  # ligne purement commentée : mention, pas consommation
    allowed = EXCEPTIONS.get(rel, set())
    for ent, pat in _DENY_PATTERNS.items():
        if ent in allowed:
            continue
        if pat.search(line):
            ERRORS.append(
                f"ERREUR source isolation: {rel}:{lineno} référence interdite "
                f"{ent} dans un domaine Maison. Utiliser une interface canonique "
                f"autorisée du domaine consommateur."
            )


def run() -> None:
    files = scanned_files()
    for path in files:
        rel = path.relative_to(REPO_ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:  # pragma: no cover - I/O improbable
            ERRORS.append(f"ERREUR source isolation: {rel} illisible ({exc}).")
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            scan_line(rel, i, line)

    print("Arsenal — Séparation des périmètres (sources extérieures hors domicile)\n")
    print(f"  Périmètre scanné : {len(SCAN_BASES)} bases × {len(MAISON_DOMAINS)} domaines Maison")
    print(f"  Fichiers analysés : {len(files)}")
    print(f"  Deny-list exacte : {len(DENY_LIST)} entités "
          f"({len(_DENY_CORE)} sources cœur + {len(_DENY_FILTRES)} filtrés "
          f"+ {len(_DENY_SEUILS)} seuils)")
    if EXCEPTIONS:
        print(f"  Exceptions déclarées : {sum(len(v) for v in EXCEPTIONS.values())}")

    if ERRORS:
        print("\n❌ SÉPARATION DES PÉRIMÈTRES NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    print("\n✅ SÉPARATION DES PÉRIMÈTRES CONFORME "
          "— aucune source extérieure hors domicile dans une décision Maison")


# ---------------------------------------------------------------------------
# Auto-test (on ne défend pas une frontière avec un juge défectueux)
# ---------------------------------------------------------------------------
def selftest() -> None:
    def hits(line: str) -> list[str]:
        found = []
        if _COMMENT_LINE.match(line):
            return found
        for ent, pat in _DENY_PATTERNS.items():
            if pat.search(line):
                found.append(ent)
        return found

    # 1. Une consommation interdite est détectée.
    assert "sensor.temperature_exterieur" in hits(
        "{% set t = states('sensor.temperature_exterieur') %}"
    ), "selftest: source cœur non détectée"

    # 2. Mine inversée — NE DOIT PAS matcher (source jardin).
    assert hits("{% set m = states('sensor.temperature_exterieure_moyenne_jour') %}") == [], \
        "selftest: faux positif sur temperature_exterieure_moyenne_jour"

    # 3. Distinction _1 / _2 vs base (frontière de token).
    h = hits("- sensor.temperature_exterieur_1")
    assert h == ["sensor.temperature_exterieur_1"], f"selftest: token _1 mal isolé ({h})"

    # 4. Ligne commentée ignorée.
    assert hits("#   T : sensor.temperature_exterieur (ancienne source)") == [], \
        "selftest: ligne commentée non ignorée"

    # 5. Entité d'affichage couleur non capturée par une source cœur.
    assert hits("{{ states('sensor.couleur_temperature_exterieur') }}") == [], \
        "selftest: faux positif sur couleur_temperature_exterieur"

    # 6. Un dérivé filtré Imprimerie est détecté.
    assert "sensor.temperature_filtre_aube_exterieur" in hits(
        "{% set f = states('sensor.temperature_filtre_aube_exterieur') %}"
    ), "selftest: dérivé filtré non détecté"

    print("selftest OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        run()
