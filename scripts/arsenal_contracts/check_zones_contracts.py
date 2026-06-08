#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Zones géographiques
Contrat : CONTRAT_ZONES v1.0.4
Script  : scripts/arsenal_contracts/check_zones_contracts.py
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
DIR_ZONES            = REPO_ROOT / "17_zones"
F_MAISON_SECURITE    = DIR_ZONES / "maison_securite.yaml"
F_APPROCHE_SECURITE  = DIR_ZONES / "approche_securite.yaml"
F_CONFIGURATION      = REPO_ROOT / "configuration.yaml"

# Dossiers à scanner pour les invariants d'usage
DIR_AUTOMATIONS      = REPO_ROOT / "11_automations"
DIR_TEMPLATES        = REPO_ROOT / "12_template_sensors"
DIR_SCRIPTS          = REPO_ROOT / "10_scripts"

# Sous-dossiers sécurité/alarme (I2, I4)
DIRS_SECURITE = [
    REPO_ROOT / "11_automations/alarme",
    REPO_ROOT / "11_automations/securite",
    REPO_ROOT / "12_template_sensors/alarme",
    REPO_ROOT / "12_template_sensors/securite",
]

# Sous-dossiers infrastructure présence (I8)
DIRS_INFRASTRUCTURE = [
    REPO_ROOT / "11_automations/presence",
    REPO_ROOT / "12_template_sensors/presence",
]

# ---------------------------------------------------------------------------
# Paramètres normatifs (§3)
# ---------------------------------------------------------------------------
# I5 (v1.0.4) : les coordonnées GPS du domicile sont externalisées dans
# secrets.yaml. Le checker ne connaît jamais la valeur réelle — il valide
# uniquement la FORME (!secret <clé>), l'unicité de la référence entre les
# deux zones, et l'absence de toute coordonnée littérale (anti-réintroduction).
SECRET_LAT_KEY  = "home_latitude"
SECRET_LON_KEY  = "home_longitude"

# latitude/longitude: !secret <clé>
RE_LAT_SECRET = re.compile(r"latitude\s*:\s*!secret\s+(\S+)", re.IGNORECASE)
RE_LON_SECRET = re.compile(r"longitude\s*:\s*!secret\s+(\S+)", re.IGNORECASE)
# Garde anti-fuite : latitude/longitude suivi d'une valeur décimale littérale.
RE_COORD_LITTERALE = re.compile(
    r"\b(?:latitude|longitude)\s*:\s*[+-]?\d{1,3}\.\d+", re.IGNORECASE
)

RAYON_MAISON  = "40"
RAYON_APPROCHE = "400"
ICON_MAISON   = "mdi:shield-home"
ICON_APPROCHE = "mdi:map-marker-radius"

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


def active_lines(content: str) -> list[str]:
    return [l for l in content.splitlines() if not l.strip().startswith("#")]


# ---------------------------------------------------------------------------
# T1 — Présence des fichiers zones canoniques (§7.1)
# ---------------------------------------------------------------------------

def test_zone_files_present() -> None:
    all_ok = True
    for path in [F_MAISON_SECURITE, F_APPROCHE_SECURITE]:
        if not path.is_file():
            ERRORS.append(f"T1 — Fichier zone manquant : "
                          f"{path.relative_to(REPO_ROOT)} (§7.1)")
            all_ok = False
    if all_ok:
        print("✔ T1 — Fichiers zones canoniques présents "
              "(maison_securite.yaml + approche_securite.yaml)")


# ---------------------------------------------------------------------------
# T2 — Coordonnées GPS externalisées via !secret (I5)
#
# Invariant (I5, v1.0.4) : les deux zones métier déclarent
#   latitude:  !secret home_latitude
#   longitude: !secret home_longitude
# Le checker valide trois propriétés, sans jamais connaître la valeur réelle :
#   (a) FORME       — chaque zone utilise bien !secret sur lat ET lon ;
#   (b) UNICITÉ     — les deux zones référencent les MÊMES clés secret
#                     (garantie « même référence domicile ») ;
#   (c) ANTI-FUITE  — aucune coordonnée décimale littérale ne subsiste.
# ---------------------------------------------------------------------------

def test_gps_coordinates() -> None:
    all_ok = True
    lat_keys: set[str] = set()
    lon_keys: set[str] = set()

    for path in [F_MAISON_SECURITE, F_APPROCHE_SECURITE]:
        content = read(path)
        rel = path.relative_to(REPO_ROOT)
        if not content:
            ERRORS.append(f"T2 — Fichier inaccessible : {rel}")
            all_ok = False
            continue

        # (a) Forme + (b) collecte des clés
        m_lat = RE_LAT_SECRET.search(content)
        m_lon = RE_LON_SECRET.search(content)

        if not m_lat:
            ERRORS.append(f"T2 — latitude doit être externalisée "
                          f"(`latitude: !secret {SECRET_LAT_KEY}`) dans {rel} (I5)")
            all_ok = False
        else:
            lat_keys.add(m_lat.group(1))
            if m_lat.group(1) != SECRET_LAT_KEY:
                ERRORS.append(f"T2 — clé secret latitude inattendue "
                              f"'{m_lat.group(1)}' dans {rel} ; "
                              f"attendu '{SECRET_LAT_KEY}' (I5)")
                all_ok = False

        if not m_lon:
            ERRORS.append(f"T2 — longitude doit être externalisée "
                          f"(`longitude: !secret {SECRET_LON_KEY}`) dans {rel} (I5)")
            all_ok = False
        else:
            lon_keys.add(m_lon.group(1))
            if m_lon.group(1) != SECRET_LON_KEY:
                ERRORS.append(f"T2 — clé secret longitude inattendue "
                              f"'{m_lon.group(1)}' dans {rel} ; "
                              f"attendu '{SECRET_LON_KEY}' (I5)")
                all_ok = False

        # (c) Anti-réintroduction : aucune coordonnée littérale tolérée
        if RE_COORD_LITTERALE.search(content):
            ERRORS.append(f"T2 — coordonnée GPS littérale détectée dans {rel} : "
                          f"doit être externalisée via !secret (I5, anti-fuite)")
            all_ok = False

    # (b) Unicité de la référence domicile entre les deux zones
    if len(lat_keys) > 1 or len(lon_keys) > 1:
        ERRORS.append("T2 — les deux zones métier ne référencent pas la même "
                      "clé secret domicile (référence non unique, I5)")
        all_ok = False

    if all_ok:
        print(f"✔ T2 — Coordonnées GPS externalisées via "
              f"!secret {SECRET_LAT_KEY}/{SECRET_LON_KEY}, référence domicile "
              f"unique, aucune valeur littérale (I5)")


# ---------------------------------------------------------------------------
# T3 — Rayon zone.maison_securite = 40 m (§3.2, I6)
# ---------------------------------------------------------------------------

def test_rayon_maison_securite() -> None:
    content = read(F_MAISON_SECURITE)
    if not content:
        ERRORS.append(f"T3 — Fichier inaccessible : "
                      f"{F_MAISON_SECURITE.relative_to(REPO_ROOT)}")
        return
    pattern = re.compile(rf"radius\s*:\s*{re.escape(RAYON_MAISON)}\b")
    if not pattern.search(content):
        ERRORS.append(f"T3 — Rayon {RAYON_MAISON} m absent de "
                      f"{F_MAISON_SECURITE.relative_to(REPO_ROOT)} (§3.2)")
    else:
        print(f"✔ T3 — Rayon zone.maison_securite = {RAYON_MAISON} m (§3.2)")


# ---------------------------------------------------------------------------
# T4 — Rayon zone.approche_securite = 400 m (§3.3, I6)
# ---------------------------------------------------------------------------

def test_rayon_approche_securite() -> None:
    content = read(F_APPROCHE_SECURITE)
    if not content:
        ERRORS.append(f"T4 — Fichier inaccessible : "
                      f"{F_APPROCHE_SECURITE.relative_to(REPO_ROOT)}")
        return
    pattern = re.compile(rf"radius\s*:\s*{re.escape(RAYON_APPROCHE)}\b")
    if not pattern.search(content):
        ERRORS.append(f"T4 — Rayon {RAYON_APPROCHE} m absent de "
                      f"{F_APPROCHE_SECURITE.relative_to(REPO_ROOT)} (§3.3)")
    else:
        print(f"✔ T4 — Rayon zone.approche_securite = {RAYON_APPROCHE} m (§3.3)")


# ---------------------------------------------------------------------------
# T5 — passive: false dans les deux zones métier (§3.2, §3.3)
# ---------------------------------------------------------------------------

def test_passive_false() -> None:
    all_ok = True
    for path in [F_MAISON_SECURITE, F_APPROCHE_SECURITE]:
        content = read(path)
        if not content:
            ERRORS.append(f"T5 — Fichier inaccessible : "
                          f"{path.relative_to(REPO_ROOT)}")
            all_ok = False
            continue
        if not re.search(r"passive\s*:\s*false", content, re.IGNORECASE):
            ERRORS.append(f"T5 — passive: false absent de "
                          f"{path.relative_to(REPO_ROOT)} (§3.2/3.3)")
            all_ok = False
    if all_ok:
        print("✔ T5 — passive: false confirmé dans les deux zones métier")


# ---------------------------------------------------------------------------
# T6 — Icônes normatives présentes (§3.2, §3.3)
# ---------------------------------------------------------------------------

def test_icons() -> None:
    all_ok = True
    for path, icon in [(F_MAISON_SECURITE, ICON_MAISON),
                       (F_APPROCHE_SECURITE, ICON_APPROCHE)]:
        content = read(path)
        if not content:
            ERRORS.append(f"T6 — Fichier inaccessible : "
                          f"{path.relative_to(REPO_ROOT)}")
            all_ok = False
            continue
        if icon not in content:
            ERRORS.append(f"T6 — Icône '{icon}' absente de "
                          f"{path.relative_to(REPO_ROOT)}")
            all_ok = False
    if all_ok:
        print("✔ T6 — Icônes normatives présentes dans les deux zones")


# ---------------------------------------------------------------------------
# T7 — zone.home absente des automations et templates sécurité/alarme (I2)
#
# Invariant (I2) : aucun composant du domaine sécurité ne consomme zone.home.
# Scope : sous-dossiers alarme et sécurité.
# ---------------------------------------------------------------------------

def test_zone_home_absent_from_securite() -> None:
    violations = []
    for path in yaml_files(*DIRS_SECURITE):
        content = read(path)
        for line in active_lines(content):
            if "zone.home" in line:
                violations.append(f"{path.relative_to(REPO_ROOT)} : "
                                  f"«{line.strip()[:80]}»")
                break
    if violations:
        for v in violations:
            ERRORS.append(f"T7 — zone.home dans domaine sécurité (violation I2) : {v}")
    else:
        print("✔ T7 — zone.home absente des automations/templates sécurité (I2)")


# ---------------------------------------------------------------------------
# T8 — zone.approche_securite absente des domaines sécurité/alarme (I4, §5.1)
#
# Invariant (I4) : zone d'infrastructure uniquement — jamais dans une
# décision métier finale de sécurité.
# ---------------------------------------------------------------------------

def test_approche_absent_from_securite() -> None:
    violations = []
    for path in yaml_files(*DIRS_SECURITE):
        content = read(path)
        for line in active_lines(content):
            if "zone.approche_securite" in line:
                violations.append(f"{path.relative_to(REPO_ROOT)} : "
                                  f"«{line.strip()[:80]}»")
                break
    if violations:
        for v in violations:
            ERRORS.append(
                f"T8 — zone.approche_securite dans domaine sécurité "
                f"(violation I4/§5.1) : {v}"
            )
    else:
        print("✔ T8 — zone.approche_securite absente des domaines sécurité (I4)")


# ---------------------------------------------------------------------------
# T9 — zone.maison_securite absente des domaines infrastructure présence (I8)
#
# Invariant (I8) : zone.maison_securite ne doit jamais être utilisée
# pour des logiques d'anticipation ou d'infrastructure.
# ---------------------------------------------------------------------------

def test_maison_securite_absent_from_infra() -> None:
    # I8 : zone.maison_securite interdite dans les logiques d'infrastructure.
    # I9 autorise explicitement la lecture d'attributs pour des calculs dérivés.
    # On exclut donc les lignes ne contenant que state_attr(zone.maison_securite, ...)
    # sans en faire un trigger ou une condition booléenne.
    violations = []
    for path in yaml_files(*DIRS_INFRASTRUCTURE):
        content = read(path)
        for line in active_lines(content):
            if "zone.maison_securite" not in line:
                continue
            # Lecture d'attribut pour calcul dérivé → autorisé (I9)
            if re.search(r"state_attr\s*\(\s*['\"]zone\.maison_securite['\"]", line):
                continue
            violations.append(f"{path.relative_to(REPO_ROOT)} : "
                              f"«{line.strip()[:80]}»")
            break
    if violations:
        for v in violations:
            ERRORS.append(
                f"T9 — zone.maison_securite dans infrastructure présence "
                f"(violation I8) : {v}"
            )
    else:
        print("✔ T9 — zone.maison_securite absente des domaines "
              "infrastructure présence (I8)")


# ---------------------------------------------------------------------------
# T10 — zone.home absente de 12_template_sensors/ (I2 étendu, §7.3)
#
# Le contrat §7.3 étend I2 à tous les composants Arsenal —
# les template sensors sont particulièrement à risque.
# Scope : 12_template_sensors/ complet.
# ---------------------------------------------------------------------------

def test_zone_home_absent_from_templates() -> None:
    violations = []
    for path in yaml_files(DIR_TEMPLATES):
        content = read(path)
        for line in active_lines(content):
            if "zone.home" in line:
                violations.append(f"{path.relative_to(REPO_ROOT)} : "
                                  f"«{line.strip()[:80]}»")
                break
    if violations:
        for v in violations:
            ERRORS.append(
                f"T10 — zone.home dans template sensors "
                f"(violation I2 / §7.3) : {v}"
            )
    else:
        print("✔ T10 — zone.home absente de 12_template_sensors/ (I2)")


# ---------------------------------------------------------------------------
# T11 — Aucun fichier zone non canonique dans 17_zones/ (I7)
#
# Invariant (I7) : seules maison_securite.yaml et approche_securite.yaml
# sont autorisées. Toute autre zone créée via YAML doit faire l'objet
# d'une section §3.x et d'un incrément de version de ce contrat.
# ---------------------------------------------------------------------------

ZONES_CANONIQUES = {"maison_securite.yaml", "approche_securite.yaml"}

def test_no_extra_zone_files() -> None:
    if not DIR_ZONES.is_dir():
        ERRORS.append(f"T11 — Répertoire 17_zones/ manquant")
        return
    fichiers = {p.name for p in DIR_ZONES.glob("*.yaml") if p.is_file()}
    extras = fichiers - ZONES_CANONIQUES
    if extras:
        for f in sorted(extras):
            ERRORS.append(f"T11 — Zone non canonique dans 17_zones/ : {f} "
                          f"(I7 — doit être documentée dans §3.x)")
    else:
        print(f"✔ T11 — 17_zones/ ne contient que les zones canoniques "
              f"({', '.join(sorted(ZONES_CANONIQUES))})")


# ---------------------------------------------------------------------------
# T12 — 17_zones/ inclus dans configuration.yaml (§7.1)
# ---------------------------------------------------------------------------

def test_zones_included_in_configuration() -> None:
    content = read(F_CONFIGURATION)
    if not content:
        ERRORS.append(f"T12 — configuration.yaml inaccessible : "
                      f"{F_CONFIGURATION.relative_to(REPO_ROOT)}")
        return
    if "17_zones" not in content and "zones/" not in content:
        ERRORS.append(f"T12 — 17_zones/ non inclus dans configuration.yaml (§7.1)")
    else:
        print("✔ T12 — 17_zones/ inclus dans configuration.yaml (§7.1)")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_zone_files_present,
    test_gps_coordinates,
    test_rayon_maison_securite,
    test_rayon_approche_securite,
    test_passive_false,
    test_icons,
    test_zone_home_absent_from_securite,
    test_approche_absent_from_securite,
    test_maison_securite_absent_from_infra,
    test_zone_home_absent_from_templates,
    test_no_extra_zone_files,
    test_zones_included_in_configuration,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : Zones géographiques v1.0.4\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT ZONES NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT ZONES CONFORME")
